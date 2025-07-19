from job.executors.bizcommands.run_report import RunReportCommand
from job.executors.bizcommands.generate_invoice import GenerateInvoiceCommand

command_registry = {
    "run_report": RunReportCommand,
    "generate_invoice": GenerateInvoiceCommand
}
