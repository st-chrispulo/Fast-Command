import time
from datetime import datetime, timedelta, timezone
from croniter import croniter
from sqlalchemy.orm import Session

from logger import logger
from job.models.scheduled_jobs import ScheduledJob
from job.models.job_runs import JobRun
from job.executors.base_executor import BaseExecutor

POLL_INTERVAL_SECONDS = 10
SCHEDULE_REFRESH_INTERVAL_SECONDS = 60


def execute_job(command_name: str, payload: dict):
    command_cls = BaseExecutor(command_name, payload)._get_command_class()
    command_instance = command_cls(payload)
    return command_instance.run()


def scheduler_executor_loop(db_session_factory):
    logger.info("[SchedulerExecutor] Scheduler loop started.")
    last_schedule_check = datetime.now(timezone.utc) - timedelta(seconds=SCHEDULE_REFRESH_INTERVAL_SECONDS)

    while True:
        try:
            now = datetime.now(timezone.utc)

            if (now - last_schedule_check).total_seconds() >= SCHEDULE_REFRESH_INTERVAL_SECONDS:
                with db_session_factory() as session:
                    refresh_next_run_times(session)
                last_schedule_check = now

            with db_session_factory() as session:
                due_jobs = get_all_due_jobs(session, now)

                if due_jobs:
                    logger.info(f"[SchedulerExecutor] Found {len(due_jobs)} job(s) due for execution.")
                    for job in due_jobs:
                        logger.info(f"[SchedulerExecutor] Running job {job.id} → {job.command}")
                        run_id = run_scheduled_job(job, session)
                        logger.info(f"[SchedulerExecutor] Job {job.id} completed, run ID: {run_id}")
                else:
                    time.sleep(POLL_INTERVAL_SECONDS)

        except Exception as e:
            logger.error(f"[SchedulerExecutor] Loop error: {e}", exc_info=True)
            time.sleep(POLL_INTERVAL_SECONDS)


def get_all_due_jobs(session: Session, now: datetime):
    return (
        session.query(ScheduledJob)
        .filter(
            ScheduledJob.enabled == True,
            ScheduledJob.next_run_at <= now
        )
        .order_by(ScheduledJob.next_run_at.asc())
        .with_for_update(skip_locked=True)
        .all()
    )


def refresh_next_run_times(session: Session):
    now = datetime.now(timezone.utc)
    jobs = (
        session.query(ScheduledJob)
        .filter(ScheduledJob.enabled == True)
        .all()
    )

    if not jobs:
        logger.info("[SchedulerExecutor] No enabled scheduled jobs found.")
        return

    logger.info(f"[SchedulerExecutor] Checking {len(jobs)} scheduled job(s) for next run time...")

    for job in jobs:
        old_next_run = job.next_run_at
        base_time = job.last_run_at or now
        new_next_run = croniter(job.cron_expression, base_time).get_next(datetime)

        if not old_next_run or old_next_run < now:
            logger.info(
                f"[SchedulerExecutor] Scheduling job {job.id} ({job.command}) → Next run at {new_next_run.isoformat()}"
            )
            job.next_run_at = new_next_run

    session.commit()


def run_scheduled_job(job: ScheduledJob, session: Session):
    started_at = datetime.now(timezone.utc)

    run = JobRun(
        job_id=job.id,
        job_type="scheduled",
        command=job.command,
        payload=job.payload,
        output_directory=job.output_directory,
        status="processing",
        started_at=started_at
    )
    session.add(run)
    session.commit()

    try:
        result = execute_job(job.command, job.payload)
        run.status = "done"
        run.result = result
    except Exception as e:
        run.status = "failed"
        run.error_message = str(e)
        logger.error(f"[SchedulerExecutor] Job {job.id} failed: {e}", exc_info=True)
    finally:
        finished_at = datetime.now(timezone.utc)
        run.finished_at = finished_at
        job.last_run_at = finished_at
        job.next_run_at = croniter(job.cron_expression, finished_at).get_next(datetime)
        session.commit()

    return run.id
