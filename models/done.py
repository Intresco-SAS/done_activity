from odoo import api, fields, models,_
from odoo.exceptions import except_orm, ValidationError ,UserError
from collections import defaultdict
import re


class done_activity(models.Model):
    _name = "done.activity"

    name = fields.Char('Summary')
    state = fields.Char('State')
    type = fields.Char('Type')
    user = fields.Char('Done By')
    contact = fields.Char('Contacto')
    date_mod = fields.Date('Fecha')


class mail_activity2(models.Model):
    _inherit = "mail.activity"

    def _action_done(self, feedback=False, attachment_ids=None):
        messages, next_activities = super(mail_activity2, self)._action_done(feedback=feedback, attachment_ids=attachment_ids)
        obj = self.env['done.activity']
        for message in messages:
            activity = message.description
            name = activity.split('\n', 1)[0]
            name = name.replace(' hecho', '')
            match = re.search(r'\n:(.*?)\n', activity)
            if match:
                description = match.group(1).strip()
            else:
                description = ''

            obj.create({
                'name': description,
                'contact': message.display_name,
                'type':name,
                'state':'Finalizado',
                'user':message.author_id.name,
            })
        return messages, next_activities