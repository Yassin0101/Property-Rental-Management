# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RentalProperty(models.Model):
    _name = 'rental.property'
    _description = 'Rental Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Property Name', required=True, tracking=True)
    code = fields.Char(string='Reference Code', copy=False)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('studio', 'Studio'),
        ('office', 'Office'),
    ], string='Property Type', default='apartment', required=True, tracking=True)

    address = fields.Char(string='Address')
    city = fields.Char(string='City')

    price_per_night = fields.Float(string='Price per Night', required=True, tracking=True)
    capacity = fields.Integer(string='Guest Capacity', default=1)

    status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Under Maintenance'),
    ], string='Status', default='available', tracking=True, copy=False)

    description = fields.Text(string='Description')
    image = fields.Binary(string='Image', attachment=True)
    active = fields.Boolean(default=True)

    booking_ids = fields.One2many('rental.booking', 'property_id', string='Bookings')
    booking_count = fields.Integer(string='Booking Count', compute='_compute_booking_count')

    @api.depends('booking_ids')
    def _compute_booking_count(self):
        for rec in self:
            rec.booking_count = len(rec.booking_ids)

    def action_set_maintenance(self):
        self.write({'status': 'maintenance'})

    def action_set_available(self):
        self.write({'status': 'available'})

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'name': 'Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'rental.booking',
            'view_mode': 'tree,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }
