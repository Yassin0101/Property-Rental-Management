# Property Rental Management — Odoo Module

A custom Odoo module that manages short-term property rentals end-to-end: a property catalog, a booking workflow with automatic pricing, double-booking prevention, and a printable QWeb booking confirmation report.

Built to demonstrate core Odoo development skills: ORM models, computed & related fields, business logic with state workflows, SQL/Python constraints, security groups & access rights, backend views (tree/form/kanban/search), and QWeb PDF reporting.

## ✨ Features

- **Property catalog** — manage apartments, villas, studios, and offices with price, capacity, and status
- **Booking workflow** — `Draft → Confirmed → Checked In → Checked Out` (or `Cancelled`), with action buttons enforcing valid transitions
- **Automatic pricing** — nights and total amount are computed automatically from check-in/check-out dates and the property's nightly rate
- **Double-booking prevention** — a model constraint blocks overlapping bookings for the same property
- **Auto-numbered bookings** — sequence-based references (e.g. `BK/2026/0001`)
- **Role-based access** — `Rental User` (own bookings) vs `Rental Manager` (full access) security groups
- **QWeb PDF report** — printable booking confirmation available directly from the booking form
- **Chatter / activity tracking** — full audit trail via `mail.thread` on both models

## 🗂 Module Structure

```
property_rental_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── rental_property.py      # rental.property model
│   └── rental_booking.py       # rental.booking model + business logic
├── views/
│   ├── property_rental_views.xml   # tree, form, kanban, search, action
│   ├── rental_booking_views.xml    # tree, form, search, action
│   └── menu_views.xml
├── security/
│   ├── rental_security.xml     # Rental User / Rental Manager groups
│   └── ir.model.access.csv     # model-level access rights
├── data/
│   └── rental_sequence.xml     # booking reference sequence
├── report/
│   ├── booking_report.xml          # report action
│   └── booking_report_template.xml # QWeb report template
└── README.md
```

## 🧩 Data Model

**`rental.property`**
| Field | Type | Notes |
|---|---|---|
| `name` | Char | Required |
| `property_type` | Selection | apartment / villa / studio / office |
| `price_per_night` | Float | |
| `status` | Selection | available / booked / maintenance |
| `booking_ids` | One2many | Linked bookings |

**`rental.booking`**
| Field | Type | Notes |
|---|---|---|
| `name` | Char | Auto-generated via sequence |
| `property_id` | Many2one → `rental.property` | |
| `customer_id` | Many2one → `res.partner` | |
| `check_in` / `check_out` | Date | |
| `nights` | Integer | Computed, stored |
| `total_amount` | Float | Computed, stored |
| `state` | Selection | draft / confirmed / checked_in / checked_out / cancelled |

## ⚙️ Business Logic Highlights

- **Overlap prevention**: `_check_overlapping_bookings` raises a `ValidationError` if a new/edited booking's date range overlaps an existing active booking for the same property.
- **Status sync**: confirming a booking sets the property to `booked`; checking out or cancelling frees it back to `available`.
- **Workflow guards**: `action_check_in` / `action_check_out` raise a `UserError` if called out of sequence (e.g. trying to check in a draft booking).
- **SQL constraint**: `check_out > check_in` is enforced at the database level as a safety net.

## 🚀 Installation

1. Copy the `property_rental_management` folder into your Odoo `addons` path.
2. Restart the Odoo server.
3. Go to **Apps**, click **Update Apps List**, then search for **Property Rental Management** and click **Install**.
4. Assign users to the **Rental User** or **Rental Manager** group under **Settings → Users & Companies → Users**.

Tested against **Odoo 17** (uses the new-style `invisible="..."` view attributes and `@api.model_create_multi`); should also work on Odoo 18 with minimal changes.

## 🛣 Possible Extensions

- Calendar/Gantt view for visualizing booking occupancy over time
- Automated email confirmation on booking confirm (via `mail.template`)
- Website frontend / portal for customers to request bookings
- Payment integration (deposit on confirm, balance on checkout)

## 👤 Author

**Yassin Hany Ramadan**
Odoo Developer | Python & Full-Stack
[LinkedIn](https://www.linkedin.com/in/yassinramadan)

## 📄 License

LGPL-3
# Property-Rental-Management
