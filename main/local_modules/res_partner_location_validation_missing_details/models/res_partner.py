# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging

from openerp import models, api
from openerp.exceptions import except_orm

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add a validation of the email address of the partner."""
    _inherit = 'res.partner'

    @api.model
    def get_missing_details(self):
        missing_details = super(ResPartner, self).get_missing_details()
        ir_model_data_pool = self.env['ir.model.data']
        try:
            vals = {
                'street': self.street,
                'city': self.city,
                'country_id': self.country_id.id,
                'zip': self.zip
            }
            self._clean_location_data(vals)
        except (except_orm, AttributeError):
            missing_details.append(
                ir_model_data_pool.get_object(
                    'res_partner_location_validation_missing_details',
                    'missing_detail_cannot_geocode_address'
                ).id
            )

        return missing_details
