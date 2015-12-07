# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging
import random

from openerp import api, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @property
    def active_companies_domain(self):
        """Return the domain that should be used to filter for active companies.

        :return: list
        """
        return [
            ('active', '=', True),
            ('is_company', '=', True),
        ]

    @api.model
    def get_active_companies(self):
        """Return recordsets of all the active companies.

        :return: recordset.
        """
        return self.search(self.active_companies_domain)

    @api.model
    def get_number_active_companies(self):
        """Return the number of active companies.

        :return: int
        """
        return len(self.get_active_companies())

    @api.model
    def get_closed_commpanies(self):
        """Return recordsets of all the companies under the closed status.

        :return: recordset.
        """
        return self.search(
            self.active_companies_domain + [('state', '=', 'closed')]
        )

    @api.model
    def get_open_commpanies(self):
        """Return recordsets of all the companies under the open status.

        :return: recordset.
        """
        return self.search(
            self.active_companies_domain + [('state', '=', 'open')]
        )

    @api.model
    def get_most_popular_studios(self, sample_):
        """Return a list of partners that have a logo.

        The list is filtered to just returns partner that match:
        - is active
        - is a company
        - is not the partner related to cgstudiomap
        - has an image.
        :return: list of partner records.
        """
        company_pool = self.env['res.company']
        # #294
        # Looking for cgstudiomap to avoid to have it displayed.
        # cgstudiomap is actually the partner linked to the res.company
        # of the instance.
        # looking for the first (and only so far) res.company
        company = company_pool.browse(1)

        # https://github.com/cgstudiomap/cgstudiomap/issues/177
        # search return a recordset and we cannot do len() on it.
        partners = [
            partner for partner in self.search(
                self.active_companies_domain +
                [
                    ('id', '!=', company.partner_id.id),
                    ('image', '!=', False)
                ]
            )
            ]

        # doing kind of unittest in here as I do not know how to
        # do unittest with request :(
        assert company.partner_id.id not in [p.id for p in partners], (
            'cgstudiomap is in the most popular studio list'
        )
        return random.sample(partners, min(len(partners), sample_))
