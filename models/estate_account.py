from odoo import fields, models, Command


class EstateAccount(models.Model):
    _inherit = "estate_property"

    def set_state_sold(self):
        (
            self.env["account.move"]
            .sudo()
            .with_context(default_move_type="out_invoice")
            .create(
                {
                    "partner_id": self.buyer_id.id,
                    "move_type": "out_invoice",
                    "line_ids": [
                        Command.create(
                            {
                                "product_id": self.env.ref("product.expense_hotel").id,
                                "name": self.name,
                                "quantity": "1",
                                "price_unit": (self.selling_price * 6) / 100,
                            }
                        ),
                        Command.create(
                            {"name": "Admin fees", "quantity": "1", "price_unit": "100"}
                        ),
                    ],
                }
            )
        )

        super().set_state_sold()
