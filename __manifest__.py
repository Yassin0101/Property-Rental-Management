# -*- coding: utf-8 -*-
{
    'name': 'Property Rental Management',
    'version': '17.0.1.0.0',
    'category': 'Real Estate',
    'summary': 'Manage short-term property rentals, bookings, and availability',
    'description': """
Property Rental Management
===========================
A lightweight property rental & booking management system for Odoo.

Features
--------
* Manage a catalog of rentable properties (apartments, villas, studios, offices)
* Create bookings linked to customers (res.partner) with automatic price calculation
* Booking workflow: Draft -> Confirmed -> Checked In -> Checked Out / Cancelled
* Automatic property availability status based on active bookings
* Prevents double-booking of the same property for overlapping dates
* Printable QWeb booking confirmation report
* Role-based access via Rental User / Rental Manager security groups
* Kanban view for visually browsing available properties
    """,
    'author': 'Yassin Hany Ramadan',
    'website': 'https://www.linkedin.com/in/yassinramadan',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/rental_security.xml',
        'security/ir.model.access.csv',
        'data/rental_sequence.xml',
        'views/property_rental_views.xml',
        'views/rental_booking_views.xml',
        'views/menu_views.xml',
        'report/booking_report.xml',
        'report/booking_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
