import logging

from flask import request
from flask_restplus import Api, Resource, fields

from app import api
from utils.HelperUtils import getClassName
from models.swagger_models import tenant_request, error, tenant_response, tenant_update_request, tenant_metadata_model, \
    tenant_data_model, tenant_delete_response

tenant_name_space = api.namespace(name='Tenants', path="/", description='Manage Tenants')
tenantMetadataModel = api.model('TenantMetadata', tenant_metadata_model())
tenantDataModel = api.model('TenantData', tenant_data_model())
createTenantReqModel = api.model('CreateTenantRequest', tenant_request(tenantMetadataModel))
updateTenantReqModel = api.model('UpdateTenantRequest', tenant_update_request(tenantMetadataModel))
tenantRemovalResModel = api.model('TenantRemovalResponse', tenant_delete_response())
responseModel = api.model('TenantResponse', tenant_response(tenantDataModel))
errorModel = api.model('Error', error())


@tenant_name_space.route("/v1/tenants")
class TenantResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(TenantResource))

    @api.doc(name="CreateTenant Request", description='Creates a new tenant.')
    @api.expect(createTenantReqModel, validate=True)
    @api.marshal_with(responseModel, code=201, description='Created')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            print(request.json)
            return {
                "message": "New tenant created",
            }
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="ListTenants Request", description='List all the tenants.')
    @api.marshal_with(responseModel, code=200, description='Success')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def get(self):
        try:
            return [{
                "name": "T1"
            }]
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@tenant_name_space.route("/v1/tenants/<string:tenant_id>")
class TenantResourceById(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(TenantResourceById))

    @api.doc(name="GetTenant Request", description='Gets the tenant with the provided id.', params={'tenant_id': 'Specify the tenant Id associated with the tenant'})
    @api.marshal_with(responseModel, code=200, description='Success')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def get(self, tenantId):
        try:
            print(tenantId)
            return {
                "name": "T1"
            }
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="PutTenant Request", description='Updates the tenant with the provided id.', params={'tenant_id': 'Specify the tenant Id associated with the tenant'})
    @api.expect(updateTenantReqModel, validate=True)
    @api.marshal_with(responseModel, code=200, description='Success')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def put(self, tenantId):
        try:
            print(tenantId)
            return {
                "message": "Tenant is updated"
            }
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="DeleteTenant Request", description='Deletes the tenant with the provided id.', params={'tenant_id': 'Specify the tenant Id associated with the tenant'})
    @api.marshal_with(tenantRemovalResModel, code=200, description='Success')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def delete(self, tenant_id):
        try:
            print(tenant_id)
            return {
                "message": "Tenant is deleted.",
            }, 200
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")