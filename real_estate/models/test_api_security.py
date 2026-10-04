import xmlrpc.client

url = 'http://localhost:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
print(f"Logged in as user Name: {username} and User ID: {uid}")
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

property_ids = models.execute_kw(
    db, uid, password,
    'real_estate.property', 'search',
    [[]], {'limit': 1}
)
print(f"Found property: {property_ids}")

property_data = models.execute_kw(
    db, uid, password,
    'real_estate.property', 'read',
    [property_ids, ['name', 'price']]
)

tenant_ids = models.execute_kw(
    db, uid, password,
    'real_estate.tenant', 'search',
    [[]], {'limit': 1}
)

print(f"Found tenant: {tenant_ids}")
models.execute_kw(
    db, uid, password,
    'res.partner', 'write',
    [[tenant_ids], {'phone': '+1234567890'}]
)
