import asyncio
from job.executors.bizcommands.command_base import Command
from job.utils.progress_emitter import ProgressEmitterMixin


class LongRunningBusinessCaseCommand(Command, ProgressEmitterMixin):
    def run(self):
        job_id = self.payload.get("job_id")

        async def _run():
            for i in range(1, 101):
                await self.emit_progress(
                    job_id=job_id,
                    status="processing",
                    message=f"Step {i}/100 in progress...",
                    percent=i
                )
                await asyncio.sleep(0.1)

            await self.emit_progress(
                job_id=job_id,
                status="done",
                message="Business case completed",
                percent=100
            )

        asyncio.run(_run())

        return {"message": f"Job {job_id} completed successfully"}
