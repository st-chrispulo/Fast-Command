from job.executors.bizcommands.run_report import RunReportCommand
from job.executors.bizcommands.generate_invoice import GenerateInvoiceCommand
from job.executors.bizcommands.socket_event_checkpoint import SocketEventCheckpointCommand


command_registry = {
    "run_report": RunReportCommand,
    "generate_invoice": GenerateInvoiceCommand,
    "socket_event_checkpoint": SocketEventCheckpointCommand,
}
