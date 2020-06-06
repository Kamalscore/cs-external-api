import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from client import get_tenants, create_tenant, get_tenant, delete_tenant, update_tenant
from models.swagger_models import tenant_request, error, tenant_response, tenant_update_request, tenant_data_model, \
    tenant_delete_response, wild_card_model, tenant_create_response, tenant_update_response
from utils.HelperUtils import getClassName

tenant_name_space = api.namespace(name='Tenants', path="/", description='Manage Tenants')
wildcardModel = api.model('TenantMetadata', wild_card_model())
tenantDataModel = api.model('TenantData', tenant_data_model())
createTenantReqModel = api.model('CreateTenantRequest', tenant_request(wildcardModel))
updateTenantReqModel = api.model('UpdateTenantRequest', tenant_update_request(wildcardModel))
tenantRemovalResModel = api.model('TenantRemovalResponse', tenant_delete_response())
responseModel = api.model('TenantResponse', tenant_response(wildcardModel))
createResponseModel = api.model('TenantCreateResponse', tenant_create_response())
updateResponseModel = api.model('TenantUpdateResponse', tenant_update_response())
errorModel = api.model('Error', error())


@tenant_name_space.route("/v1/tenants")
class TenantResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(TenantResource))

    @api.doc(name="CreateTenant Request", description='Creates a new tenant.', security='apiKey')
    @api.expect(createTenantReqModel, validate=True)
    @tenant_name_space.response(model=createResponseModel, code=201, description='Created')
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            accessToken = request.headers.get("X-Auth-User")
            requestBody = request.json
            requestBody["status"] = "active" if bool(requestBody.get("status")) else "inactive"
            requestBody["project_master_id"] = requestBody.get("account_id", None)
            response = create_tenant(accessToken, requestBody)
            if response.status_code == 200:
                return marshal(response.json(), createResponseModel), 201
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="ListTenants Request", description='List all the tenants.', security='apiKey')
    @tenant_name_space.response(model=responseModel, code=200, description='Success', as_list=True)
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self):
        try:
            accessToken = request.headers.get("X-Auth-User")
            response = get_tenants(accessToken)
            if response.status_code == 200:
                responseJson = marshal(response.json(), responseModel)
                for t in responseJson.get('tenants'):
                    t['account_name'] = t.pop('project_master_name', None)
                    t['account_id'] = t.pop('project_master_id', None)
                    t.pop('preferences', None)
                return responseJson, 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@tenant_name_space.route("/v1/tenants/<string:tenant_id>")
class TenantResourceById(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(TenantResourceById))

    @api.doc(name="GetTenant Request", description='Gets the tenant with the provided id.', params={'tenant_id': 'Specify the tenant Id associated with the tenant'}, security='apiKey')
    @tenant_name_space.response(model=responseModel, code=200, description='Success')
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            accessToken = request.headers.get("X-Auth-User")
            response = get_tenant(accessToken, tenant_id)
            if response.status_code == 200:
                t = response.json()
                t = t.pop('data', {})
                t.pop('status', None)
                t.pop('message', None)
                t.pop('claas_metadata', None)
                t['account_name'] = t.pop('project_master_name', None)
                t['account_id'] = t.pop('project_master_id', None)
                return t, 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="PutTenant Request", description='Updates the tenant with the provided id.', params={'tenant_id': 'Specify the tenant Id associated with the tenant'}, security='apiKey')
    @api.expect(updateTenantReqModel, validate=True)
    @tenant_name_space.response(model=updateResponseModel, code=200, description='Success')
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, tenant_id):
        try:
            accessToken = request.headers.get("X-Auth-User")
            requestBody = request.json
            requestBody["status"] = "active" if bool(requestBody.get("status")) else "inactive"
            requestBody["project_master_id"] = requestBody.get("account_id", None)
            requestBody.pop("account_id", None)
            response = update_tenant(accessToken, tenant_id, requestBody)
            if response.status_code == 200:
                t = response.json()
                return {'id': t.get('data', {}).get('project_id', None)}, 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="DeleteTenant Request", description='Deletes the tenant with the provided id.', params={'tenant_id': 'Specify the tenant Id associated with the tenant'}, security='apiKey')
    @tenant_name_space.response(model=tenantRemovalResModel, code=200, description='Success')
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def delete(self, tenant_id):
        try:
            accessToken = request.headers.get("X-Auth-User")
            response = delete_tenant(accessToken, tenant_id)
            if response.status_code == 200:
                t = response.json()
                t.pop('status', None)
                return t, 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")