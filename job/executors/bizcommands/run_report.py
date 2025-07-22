from job.executors.bizcommands.command_base import Command


class RunReportCommand(Command):
    def run(self):
        client_id = self.payload.get("client_id")
        if not client_id:
            raise ValueError("Missing 'client_id' in payload")

        return {
            "message": f"Report generated for client_id {client_id}",
            "report_id": "rpt-1234",
            "timestamp": "2025-07-19T10:00:00Z"
        }
