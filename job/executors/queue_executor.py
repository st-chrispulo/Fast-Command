import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from logger import logger

from job.models.queued_jobs import QueuedJob
from job.models.job_runs import JobRun
from job.executors.retrying_executor import RetryingExecutor

POLL_INTERVAL_SECONDS = 5


def queue_executor_loop(db_session_factory):
    logger.info("[QueueExecutor] Started queue polling loop")
    while True:
        try:
            with db_session_factory() as session:
                job = fetch_next_queued_job(session)
                if job:
                    logger.info(f"[QueueExecutor] Executing job {job.id} -> {job.command}")
                    run_id = process_job(job, session)
                    logger.info(f"[QueueExecutor] Finished job {job.id}, logged run {run_id}")
                else:
                    time.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            logger.error(f"[QueueExecutor] Error in loop: {str(e)}", exc_info=True)
            time.sleep(POLL_INTERVAL_SECONDS)


def fetch_next_queued_job(session: Session):
    return (
        session.query(QueuedJob)
        .filter(QueuedJob.status == "queued")
        .order_by(QueuedJob.created_at.asc())
        .with_for_update(skip_locked=True)
        .first()
    )


def process_job(job: QueuedJob, session: Session) -> str:
    now = datetime.now(timezone.utc)

    job.status = "processing"
    job.updated_at = now
    session.commit()

    run = JobRun(
        job_id=job.id,
        job_type="queued",
        command=job.command,
        payload=job.payload,
        output_directory=job.output_directory,
        status="processing",
        started_at=now,
    )
    session.add(run)
    session.commit()

    try:
        executor = RetryingExecutor(job.command, job.payload)
        result = executor.run()

        job.status = "done"
        run.status = "done"
        run.result = result

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        run.status = "failed"
        run.error_message = str(e)
        logger.error(f"[QueueExecutor] Job {job.id} failed: {str(e)}", exc_info=True)

    finally:
        finished_at = datetime.now(timezone.utc)
        job.updated_at = finished_at
        run.finished_at = finished_at
        session.commit()

    return str(run.id)
