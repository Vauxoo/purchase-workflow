from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env["ir.actions.act_window"]._for_xml_id("base.action_attachment")
        res["domain"] = [
            ("res_model", "=", "account.payment"),
            ("res_id", "in", self.ids),
        ]
        res["context"] = {
            "default_res_model": "account.payment",
            "default_res_id": self.id,
        }
        return res
