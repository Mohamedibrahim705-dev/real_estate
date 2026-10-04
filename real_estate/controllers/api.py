from odoo import http,fields
from odoo.http import request
import json


class RealEstateAPI(http.Controller):

    @http.route('/api/properties/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_property(self, **kwargs):
        TOKEN = 'cacb064fd72c08b445959765'
        authorization_token = request.httprequest.headers.get('Authorization', '')
        if authorization_token != f'Bearer {TOKEN}':
            return request.make_json_response({'status': 'error', 'message': 'Unauthorized'}, status=401)
        try:
            params = kwargs
            if not params.get('name') or not params.get('price'):
                return {
                    'status': 'error',
                    'message': 'Name and price are required'
                }

            property_obj = request.env['real_estate.property'].sudo().create({
                'name': params.get('name'),
                'price': params.get('price'),
                'bedrooms': params.get('bedrooms', 0),
                'property_type': params.get('property_type', 'house'),
                'external_id': params.get('external_id'),
            })

            return {
                'status': 'success',
                'message': 'Property created successfully',
                'data': {
                    'property_id': property_obj.id,
                    'name': property_obj.name,
                    'external_id': property_obj.external_id,
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    @http.route('/api/crm/leads/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_crm_lead(self, **kwargs):
        try:
            params = kwargs
            if not params.get('name'):
                return {
                    'status': 'error',
                    'message': 'Name is required'
                }

            if not params.get('phone'):
                return {
                    'status': 'error',
                    'message': 'Phone is required'
                }

            if not params.get('email'):
                return {
                    'status': 'error',
                    'message': 'Email is required'
                }

            if not params.get('property_type'):
                return {
                    'status': 'error',
                    'message': 'Property is required'
                }

            lead_type = params.get('type')
            if lead_type and lead_type not in ('lead', 'opportunity'):
                return {
                    'status': 'error',
                    'message': "Type must be 'lead' or 'opportunity'"
                }

            lead_values = {
                'name': params.get('name'),
                'contact_name': params.get('contact_name'),
                'email_from': params.get('email'),
                'phone': params.get('phone'),
                'mobile': params.get('mobile'),
                'property_type': params.get('property_type'),
            }
            if lead_type:
                lead_values['type'] = lead_type

            lead = request.env['crm.lead'].sudo().create(lead_values)

            return {
                'status': 'success',
                'message': 'CRM lead created successfully',
                'data': {
                    'lead_id': lead.id,
                    'name': lead.name,
                    'email': lead.email_from,
                    'phone': lead.phone,
                    'type': lead.type,
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    @http.route('/api/tenant/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_tenant(self, **kwargs):
        try:
            
            params = kwargs
            if not params.get('name') or not params.get('email'):
                return {
                    'status': 'error',
                    'message': 'Name and email are required'
                }
            
            tenant = request.env['real_estate.tenant'].sudo().create({
                'name': params.get('name'),
                'email': params.get('email'),
                'description': params.get('description'),
                'phone': params.get('phone'),
                'mobile': params.get('mobile'),
                'city': params.get('city'),
                'date_of_birth': params.get('date_of_birth'),
                'notes': params.get('notes'),
                'website': params.get('website'),
                'age_category': params.get('age_category'),
                'created_by_api': True,
            })
            
            return {
                'status': 'success',
                'message': 'Tenant created successfully',
                'data': {
                    'tenant_id': tenant.id,
                    'name': tenant.name,
                    'email': tenant.email,
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


    @http.route('/api/tenant/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_tenant_phone(self, **kwargs):
        try:
            
            params = kwargs
            if not params.get('id') or not params.get('phone'):
                return {
                    'status': 'error',
                    'message': 'Tenant ID and phone are required'
                }

            tenant = request.env['real_estate.tenant'].sudo().search([
                ('id', '=', params.get('id')),
                ('active', '=', True),
            ], limit=1)
            if not tenant:
                return {
                    'status': 'error',
                    'message': 'Tenant not found'
                }

            tenant.write({'phone': params.get('phone')})

            return {
                'status': 'success',
                'message': 'Tenant phone updated successfully',
                'data': {
                    'tenant_id': tenant.id,
                    'name': tenant.name,
                    'phone': tenant.phone,
                }
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


    @http.route('/api/tenants/<int:tenant_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def update_tenant(self, tenant_id):
        tenant_obj = request.env['real_estate.tenant'].sudo().browse(tenant_id)
        # print(tenant_obj.name)
        if not tenant_obj.exists():
            return request.make_json_response(
                {'status': 'error', 
                 'message': 'Tenant not found'}, 
                 status=404
                 )
        
        params = request.httprequest.get_json(silent=True)

        tenant_obj.write(params)
        return request.make_json_response({'status': 'success', 
                                           'tenant_id': tenant_obj.id}
                                           )

    @http.route('/api/property/<int:property_id>', type='http', auth='public', methods=['POST'], csrf=False)
    def update_property(self, property_id):
        property_obj = request.env['real_estate.property'].sudo().browse(property_id)
        if not property_obj.exists():
            return request.make_json_response(
                {'status': 'error', 'message': 'Property not found'},
                status=404,
            )

        params = request.httprequest.get_json(silent=True)
        property_obj.write(params)
        return request.make_json_response({
            'status': 'success',
            'property_id': property_obj.id,
        })

    @http.route('/api/list_leases', type='http', auth='public', methods=['GET'], csrf=False)
    def list_leases(self):
        date_from = request.httprequest.args.get('date_from')
        date_to = request.httprequest.args.get('date_to')
        if not date_from or not date_to:
            return request.make_json_response(
                {'status': 'error', 
                 'message': 'date_from and date_to are required'}, 
                 status=400
            )

        try:
            print('date_from 1:', date_from)
            date_from = fields.Date.to_date(date_from)
            date_to = fields.Date.to_date(date_to)
            print('date_from 2:', date_from)

        except Exception as e:
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers={'Content-Type': 'application/json'}
            )

        if date_from > date_to:
            return request.make_response(
                json.dumps({'status': 'error', 
                            'message': 'date_from must be before date_to'}),
                headers={'Content-Type': 'application/json'}
            )

        leases = request.env['real_estate.lease'].sudo().search([
            ('start_date', '<=', date_to),
            ('end_date', '>=', date_from),
        ])
        return request.make_response(
            json.dumps({
                'status': 'success',
                'data': [{
                    'id': lease.id,
                    'name': lease.name,
                    'tenant': lease.tenant_id.name,
                    'property': lease.property_id.name,
                    'start_date': fields.Date.to_string(lease.start_date),
                    'end_date': fields.Date.to_string(lease.end_date),
                    'monthly_rent': lease.monthly_rent,
                    'state': lease.state,
                } for lease in leases],
            }),
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/api/list_tenant_leases', type='http', auth='public', methods=['GET'], csrf=False)
    def list_leases(self):
        tenant_id = request.httprequest.args.get('tenant_id')
        if not tenant_id:
            return request.make_json_response(
                {'status': 'error', 'message': 'tenant_id is required'},
                 status=400
            )

        try:
            tenant_id = int(tenant_id)
        except (TypeError, ValueError):
            return request.make_json_response(
                {'status': 'error', 'message': 'tenant_id must be an integer'},
                status=400,
            )

        tenant = request.env['real_estate.tenant'].sudo().browse(tenant_id).exists()
        if not tenant:
            return request.make_json_response(
                {'status': 'error', 'message': 'Tenant not found'},
                status=404,
            )

        leases = request.env['real_estate.lease'].sudo().search([
            ('tenant_id', '=', tenant_id),
        ])
        return request.make_response(
            json.dumps({
                'status': 'success',
                'count': len(leases),
                'data': [{
                    'id': lease.id,
                    'name': lease.name,
                    'tenant': lease.tenant_id.name,
                    'property': lease.property_id.name,
                    'start_date': fields.Date.to_string(lease.start_date),
                    'end_date': fields.Date.to_string(lease.end_date),
                    'monthly_rent': lease.monthly_rent,
                    'state': lease.state,
                } for lease in leases],
            }),
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/api/tenant_leases/<int:tenant_id>', type='http', auth='none', methods=['GET'], csrf=False)
    def tenant_leases(self, tenant_id):

        TOKEN = 'cacb064fd72c08b445959765'
        authorization_token = request.httprequest.headers.get('Authorization', '')
        if authorization_token != f'Bearer {TOKEN}':
            return request.make_json_response({'status': 'error', 'message': 'Unauthorized'}, status=401)
        if not tenant_id:
            return request.make_json_response(
                {'status': 'error', 
                 'message': 'tenant_id is required'}, 
                 status=400
            )
       
        leases = request.env['real_estate.lease'].sudo().search([
            ('tenant_id', '=', tenant_id),
        ])
        leases_count = len(leases)
        return request.make_response(
            json.dumps({
                'status': 'success',
                'count': leases_count,
                'data': [{
                    'id': lease.id,
                    'name': lease.name,
                    'start_date': fields.Date.to_string(lease.start_date),
                    'end_date': fields.Date.to_string(lease.end_date),
                    'state': lease.state,
                } for lease in leases],
            }),
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/api/lease/create', type='json', auth='none', methods=['POST'], csrf=False)
    def create_lease(self, **kwargs):
        authorization_token = request.httprequest.headers.get('Authorization', '')
        if authorization_token != f'Bearer {TOKEN}':
            return request.make_json_response({'status': 'error', 'message': 'Unauthorized'}, status=401)
        try:
            params = kwargs
            print(request.env.user.name)
            # Validate required fields
            if not params.get('property_id') or not params.get('start_date') or not params.get('name') or not params.get('email'):
                return {
                    'status': 'error',
                    'message': 'Name and email for Tenant are required'
                }

            tenant_obj = request.env['real_estate.tenant'].sudo().create({
                            'name': params.get('name'),
                            'email': params.get('email'),
                            'phone': "43534",
                            'created_by_api': True,  # Mark the tenant as created via API
                            'external_id': "fdfd90943",
                        })
            if tenant_obj:
                # Create lease
                lease_obj = request.env['real_estate.lease'].sudo().create({
                    'property_id': params.get('property_id'),
                    'tenant_id': tenant_obj.id,
                    'start_date': params.get('start_date'),
                    'end_date': params.get('end_date'),
                })
                
                return {
                    'status': 'success',
                    'message': 'Tenant created successfully',
                    'data': {
                        'name of lease': lease_obj.name,
                        'name of tenant': tenant_obj.name,
                        'email of tenant': tenant_obj.email,

                    }
                }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }