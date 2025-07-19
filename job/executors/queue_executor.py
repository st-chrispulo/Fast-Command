import time
from datetime import datetime
from job.models.queued_jobs import QueuedJob
from job.models.job_runs import JobRun
from job.executors.bizcommands import command_registry
from sqlalchemy.orm import Session


POLL_INTERVAL_SECONDS = 5


def queue_executor_loop(db_session_factory):
    print("[QueueExecutor] Started queue polling loop")
    while True:
        try:
            with db_session_factory() as session:
                job = fetch_next_queued_job(session)
                if job:
                    print(f"[QueueExecutor] Executing job {job.id} -> {job.command}")
                    run_id = process_job(job, session)
                    print(f"[QueueExecutor] Finished job {job.id}, logged run {run_id}")
                else:
                    time.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            print(f"[QueueExecutor] Error in loop: {str(e)}")
            time.sleep(POLL_INTERVAL_SECONDS)


def fetch_next_queued_job(session: Session):
    return session.query(QueuedJob).filter_by(status='queued').order_by(QueuedJob.created_at.asc()).first()


def process_job(job: QueuedJob, session: Session):
    job.status = 'processing'
    job.updated_at = datetime.utcnow()
    session.commit()

    run = JobRun(
        job_id=job.id,
        job_type='queued',
        command=job.command,
        payload=job.payload,
        output_directory=job.output_directory,
        status='processing',
        started_at=datetime.utcnow()
    )
    session.add(run)
    session.commit()

    try:
        if job.command not in command_registry:
            raise Exception(f"Command '{job.command}' not implemented")

        result = command_registry[job.command](job.payload)

        job.status = 'done'
        run.status = 'done'
        run.result = result
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        run.status = 'failed'
        run.error_message = str(e)
    finally:
        job.updated_at = datetime.utcnow()
        run.finished_at = datetime.utcnow()
        session.commit()

    return run.id
