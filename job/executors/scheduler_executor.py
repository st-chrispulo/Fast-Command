import time
from datetime import datetime
from croniter import croniter
from job.models.scheduled_jobs import ScheduledJob
from job.models.job_runs import JobRun
from job.executors.base_executor import execute_job
from sqlalchemy.orm import Session
from logger import logger

POLL_INTERVAL_SECONDS = 10


def scheduler_executor_loop(db_session_factory):
    logger.info("[SchedulerExecutor] Started scheduler polling loop")
    while True:
        try:
            with db_session_factory() as session:
                job = fetch_next_scheduled_job(session)
                if job:
                    logger.info(f"[SchedulerExecutor] Executing job {job.id} -> {job.command}")
                    run_id = process_scheduled_job(job, session)
                    logger.info(f"[SchedulerExecutor] Finished job {job.id}, logged run {run_id}")
                else:
                    time.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            logger.info(f"[SchedulerExecutor] Error in loop: {str(e)}")
            time.sleep(POLL_INTERVAL_SECONDS)


def fetch_next_scheduled_job(session: Session):
    now = datetime.utcnow()
    return session.query(ScheduledJob).filter(
        ScheduledJob.enabled == True,
        ScheduledJob.next_run_at <= now
    ).order_by(ScheduledJob.next_run_at.asc()).first()


def process_scheduled_job(job: ScheduledJob, session: Session):
    run = JobRun(
        job_id=job.id,
        job_type='scheduled',
        command=job.command,
        payload=job.payload,
        output_directory=job.output_directory,
        status='processing',
        started_at=datetime.utcnow()
    )
    session.add(run)
    session.commit()

    try:
        result = execute_job(job.command, job.payload)
        run.status = 'done'
        run.result = result
    except Exception as e:
        run.status = 'failed'
        run.error_message = str(e)
    finally:
        run.finished_at = datetime.utcnow()
        job.last_run_at = datetime.utcnow()
        job.next_run_at = croniter(job.cron_expression, job.last_run_at).get_next(datetime)
        session.commit()

    return run.id
