# Real Estate Management for Odoo 17

An Odoo add-on project for managing property listings and the day-to-day work around renting them. It brings property, tenant, lease, payment, and maintenance workflows together with CRM and portal access.

## Modules

| Module | Purpose |
| --- | --- |
| `real_estate` | Property and tenant records, leases, payment tracking, maintenance requests, portal pages, API controllers, and operational reports. |
| `sequence_opportunity_crm` | Optional CRM extension that assigns configurable sequence codes to opportunities. |

## Features

- Maintain property details, availability, and property types.
- Manage tenants and connect them with CRM opportunities.
- Create leases that link tenants to properties and track rental terms.
- Record lease payments and monitor maintenance requests.
- Give portal users access to property, lease, and maintenance pages.
- Generate property, lease, maintenance, and rent-roll reports, including spreadsheet exports.
- Integrate selected workflows through HTTP/JSON API controllers.
- Optionally assign sequence numbers to CRM opportunities.

## Requirements

- Odoo 17.0
- PostgreSQL, configured for your Odoo installation
- The Python dependencies required by Odoo 17.0

The main module declares dependencies on Odoo's `base`, `crm`, `portal`, and `website` modules. The opportunity sequence module depends on `crm`.

## Installation

1. Place this repository in a directory accessible to your Odoo server.
2. Add the repository directory to the Odoo `addons_path`. For example:

   ```ini
   addons_path = /path/to/odoo/addons,/path/to/real_state
   ```

3. Restart Odoo and refresh the Apps list.
4. Install **real_estate** from the Apps screen. Install **Unique Sequence Number In CRM Opportunity** if you also want the opportunity sequence feature.

You can also install modules from the command line, replacing the database and configuration values for your environment:

```bash
./odoo-bin -c /path/to/odoo.conf -d my_database -i real_estate
```

To install both modules together:

```bash
./odoo-bin -c /path/to/odoo.conf -d my_database -i real_estate,sequence_opportunity_crm
```

## Repository layout

```text
real_state/
├── real_estate/
│   ├── controllers/   # Portal and API controllers
│   ├── data/          # Sequences and module data
│   ├── demo/          # Demo records
│   ├── models/        # Business models
│   ├── report/        # Report actions and templates
│   ├── security/      # Access rights and record rules
│   ├── views/         # Odoo and portal views
│   └── wizard/        # Lease, tenant, and reporting wizards
└── sequence_opportunity_crm/
    ├── data/          # Opportunity sequence data
    ├── models/        # CRM extension and settings
    └── views/         # CRM and settings views
```

## Configuration and security

Review access rights and record rules for your user groups before deploying. API controllers expose integration endpoints; configure authentication and access controls to match your environment, and keep credentials out of source control. Use HTTPS for traffic to a deployed Odoo instance.

## Development

Make changes in the relevant add-on directory, then upgrade the affected module in a development database:

```bash
./odoo-bin -c /path/to/odoo.conf -d my_database -u real_estate
```

For changes to the opportunity sequence module, use `-u sequence_opportunity_crm`.

## License

The `real_estate` module's manifest does not currently declare a license. The included `sequence_opportunity_crm` module declares **AGPL-3**. Confirm the applicable licensing and attribution requirements before redistributing this repository.
