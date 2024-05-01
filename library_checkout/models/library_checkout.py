from odoo import api, fields, models, exceptions


class Checkout(models.Model):

    _name = "library.checkout"
    _description = "Checkout Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    member_id = fields.Many2one(
        "library.member",
        required=True,
    )

    user_id = fields.Many2one(
        "res.users",
        "Librarian",
        default=lambda s: s.env.user,
    )

    request_date = fields.Date(
        default=lambda s: fields.Date.today(),
        compute="_compute_request_date_onchange",
        store=True,
        readonly=False,
    )

    line_ids = fields.One2many(
        "library.checkout.line",
        "checkout_id",
        string="Borrowed Books",
    )

    @api.model
    def _default_stage_id(self):
        Stage = self.env["library.checkout.stage"]
        return Stage.search([("state", "=", "new")], limit=1)

    @api.model
    def _group_expand_stage_id(self, stages, _, order):
        # change _ to be domain and [] in next line to be (domain or [])
        return stages.search([], order=order)

    stage_id = fields.Many2one("library.checkout.stage",
                               default=_default_stage_id,
                               group_expand="_group_expand_stage_id")

    state = fields.Selection(related="stage_id.state")

    # using @api.model_create_multi decorator to avoid this WARNING message:
    # "The model odoo.addons.library_checkout.models.library_checkout is not overriding the create method in batch"
    @api.model_create_multi
    def create(self, vals):
        # Code before create: should use the 'vals' dict
        new_record = super().create(vals)
        # Code after create: can use the 'new_record' created
        if new_record.stage_id.state in ("open", "done"):
            raise exceptions.UserError("State not allowed for new checkouts.")
        return new_record

    checkout_date = fields.Date(readonly=True)

    close_date = fields.Date(readonly=True)

    def write(self, vals):
        if "stage_id" in vals and "kanban_state" not in vals:
            vals["kanban_state"] = "normal"

        old_state = self.stage_id.state

        super().write(vals)

        new_state = self.stage_id.state
        if not self.env.context.get("_checkout_write"):
            if new_state != old_state and new_state == "open":
                self.with_context(_checkout_write=True).write(
                    {"checkout_date": fields.Date.today()})
            if new_state != old_state and new_state == "done":
                self.with_context(_checkout_write=True).write(
                    {"close_date": fields.Date.today()})
        return True

    # @api.onchange("member_id")
    # def onchange_member_id(self):

    #     today_date = fields.Date.today()

    #     if self.request_date != today_date:
    #         self.request_date = today_date

    #         return {
    #             "warning": {
    #                 "title": "Changed Request Date",
    #                 "message": "Request date changed to today!",
    #             }
    #         }

    @api.depends("member_id")
    def _compute_request_date_onchange(self):
        today_date = fields.Date.today()
        if self.request_date != today_date:
            self.request_date = today_date
            return {
                "warning": {
                    "title": "Changed Request Date",
                    "message": "Request date changed to today!",
                }
            }

    def button_done(self):
        self.ensure_one()
        Stage = self.env["library.checkout.stage"]
        done_stage = Stage.search([("state", "=", "done")], limit=1)
        self.stage_id = done_stage

        return True

    name = fields.Char(string="Title")

    member_image = fields.Binary(related="member_id.image_128")

    count_checkouts = fields.Integer(compute="_compute_count_checkouts")

    @api.depends("member_id", "state")
    def _compute_count_checkouts(self):
        # try:
        members = self.mapped("member_id")
        domain = [
            ("member_id", "in", members.ids),
            ("state", "not in", ["done", "cancel"]),
        ]
        raw = self.read_group(domain, ["id:count"], ["member_id"])
        data = { x["member_id"][0]: x["member_id_count"] for x in raw }
        for checkout in self:
            checkout.count_checkouts = data.get(checkout.member_id.id, 0)
        # except Exception as e:
        #     print("Custom Error", e)

    # @api.depends("member_id", "state")
    # def _compute_count_checkouts(self):
    #     for checkout in self:
    #         domain = [
    #             ("member_id", "=", checkout.member_id.id),
    #             ("state", "not in", ["done", "cancel"]),
    #         ]
    #         checkout.count_checkouts = self.search_count(domain)

    num_books = fields.Integer(compute="_compute_num_books", store=True)

    @api.depends("line_ids")
    def _compute_num_books(self):
        for checkout in self:
            checkout.num_books = len(checkout.line_ids)

    kanban_state = fields.Selection([("normal", "In Progress"),
                                     ("blocked", "Blocked"),
                                     ("done", "Ready for next stage")],
                                    "Kanban State",
                                    default="normal")

    color = fields.Integer()

    priority = fields.Selection([("0", "High"), ("1", "Very High"),
                                 ("2", "Critical")],
                                default="0")
