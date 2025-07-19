from job.executors.bizcommands.command_base import Command


class RunReportCommand(Command):
    def run(self):
        org_id = self.payload.get("org_id")
        if not org_id:
            raise ValueError("Missing 'org_id' in payload")

        print(f"[run_report] Generating report for org_id: {org_id}")

        return {
            "message": f"Report generated for org_id {org_id}",
            "report_id": "rpt-1234",
            "timestamp": "2025-07-19T10:00:00Z"
        }
