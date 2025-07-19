from job_module.executors.bizcommands.command_base import Command

class GenerateInvoiceCommand(Command):
    def run(self):
        client_id = self.payload.get("client_id")
        amount = self.payload.get("amount")

        if not client_id or not amount:
            raise ValueError("Missing 'client_id' or 'amount' in payload")

        print(f"[generate_invoice] Generating invoice for client: {client_id} with amount: {amount}")

        return {
            "message": f"Invoice of ${amount} generated for client {client_id}",
            "invoice_id": "inv-5678",
            "timestamp": "2025-07-19T10:00:00Z"
        }
