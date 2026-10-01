# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class RentalBooking(models.Model):
    _name = 'rental.booking'
    _description = 'Rental Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'check_in desc'

    name = fields.Char(
        string='Booking Reference', required=True, copy=False,
        readonly=True, default=lambda self: _('New')
    )

    property_id = fields.Many2one(
        'rental.property', string='Property', required=True, tracking=True
    )
    customer_id = fields.Many2one(
        'res.partner', string='Customer', required=True, tracking=True
    )

    check_in = fields.Date(string='Check-In Date', required=True, tracking=True)
    check_out = fields.Date(string='Check-Out Date', required=True, tracking=True)

    nights = fields.Integer(string='Nights', compute='_compute_nights', store=True)
    price_per_night = fields.Float(
        string='Price per Night', related='property_id.price_per_night',
        store=True, readonly=True
    )
    total_amount = fields.Float(
        string='Total Amount', compute='_compute_total_amount', store=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('check_dates', 'CHECK(check_out > check_in)',
         'Check-out date must be after the check-in date.'),
    ]

    @api.depends('check_in', 'check_out')
    def _compute_nights(self):
        for rec in self:
            if rec.check_in and rec.check_out and rec.check_out > rec.check_in:
                rec.nights = (rec.check_out - rec.check_in).days
            else:
                rec.nights = 0

    @api.depends('nights', 'price_per_night')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.nights * rec.price_per_night

    @api.constrains('check_in', 'check_out', 'property_id', 'state')
    def _check_overlapping_bookings(self):
        for rec in self:
            if rec.state in ('cancelled',):
                continue
            overlapping = self.search([
                ('id', '!=', rec.id),
                ('property_id', '=', rec.property_id.id),
                ('state', 'not in', ['cancelled']),
                ('check_in', '<', rec.check_out),
                ('check_out', '>', rec.check_in),
            ])
            if overlapping:
                raise ValidationError(_(
                    'This property is already booked for overlapping dates '
                    '(Booking: %s).'
                ) % overlapping[0].name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'rental.booking'
                ) or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if rec.property_id.status == 'maintenance':
                raise UserError(_(
                    'Cannot confirm a booking for a property under maintenance.'
                ))
            rec.state = 'confirmed'
            rec.property_id.status = 'booked'

    def action_check_in(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_('Only confirmed bookings can be checked in.'))
            rec.state = 'checked_in'

    def action_check_out(self):
        for rec in self:
            if rec.state != 'checked_in':
                raise UserError(_('Only checked-in bookings can be checked out.'))
            rec.state = 'checked_out'
            rec.property_id.status = 'available'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'
            if rec.property_id.status == 'booked':
                rec.property_id.status = 'available'

    def action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'
