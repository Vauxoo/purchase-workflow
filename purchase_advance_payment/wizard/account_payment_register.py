from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _create_payments(self):
        """Inherited method to relate payments automatically when
        generate payments from an account.move
        """
        payments = super()._create_payments()
        active_ids = self.env.context.get("active_ids", [])
        if (
            self.env.context.get("active_model") == "account.move"
            and len(active_ids) > 0
        ):
            for move in self.env["account.move"].browse(active_ids).exists():
                orders = self.env["purchase.order"].search(
                    [("invoice_ids", "in", move.ids)]
                )
                orders.account_payment_ids |= payments.filtered(
                    lambda p: move in (p.reconciled_bill_ids | p.reconciled_invoice_ids)
                )
        return payments
