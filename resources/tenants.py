import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from client import get_tenants, create_tenant, get_tenant, delete_tenant, update_tenant
from config.marshalling import custom_marshal
from models.swagger_models import tenant_request, error, tenant_response, tenant_update_request, tenant_data_model, \
    tenant_delete_response, wild_card_model, tenant_create_response, tenant_update_response, list_tenant, \
    get_tenant_model
from utils.HelperUtils import getClassName

get_id_attribute = 'id'
tenant_name_space = api.namespace(name='Tenants', path="/", description='Manage Tenants')
wildcardModel = api.model('TenantMetadata', wild_card_model(), for_doc_alone=True)
listTenantModel = api.model('ListTenantHolder', list_tenant(), for_doc_alone=True)
getTenantModel = api.model('GetTenantModel', list_tenant(get_id_attribute))
# tenantDataModel = api.model('TenantData', tenant_data_model())
createTenantReqModel = api.model('createTenantRequest', tenant_request(wildcardModel), description="Creates a new "
                                                                                                   "tenant under a "
                                                                                                   "CoreStack "
                                                                                                   "account. There "
                                                                                                   "can be multiple "
                                                                                                   "tenants within a "
                                                                                                   "CoreStack "
                                                                                                   "account.")
updateTenantReqModel = api.model('UpdateTenantRequest', tenant_update_request(wildcardModel))
tenantRemovalResModel = api.model('TenantRemovalResponse', tenant_delete_response())
listResponseModel = api.model('ListTenantResponse', tenant_response(listTenantModel))
# getTenantModel = api.model('GetTenantModel', get_tenant_model())
getResponseModel = api.inherit('GetTenantResponse', getTenantModel, get_tenant_model(wildcardModel))
createResponseModel = api.model('TenantCreateResponse', tenant_create_response())
updateResponseModel = api.model('TenantUpdateResponse', tenant_update_response())
errorModel = api.model('Error', error())


@tenant_name_space.route("/v1/tenants")
class TenantResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(TenantResource))

    @api.doc(id='createTenant', name="CreateTenant Request", description='Creates a new tenant under a CoreStack '
                                                                         'account. There can be '
                                                                         'multiple tenants within a CoreStack account.',
             security=['auth_user', 'auth_token'])
    @api.expect(createTenantReqModel, validate=True)
    @tenant_name_space.response(model=createResponseModel, code=201, description='Created')
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            accessToken = request.headers.get("X-Auth-User")
            requestBody = request.json
            # requestBody["status"] = "active" if bool(requestBody.get("status")) else "suspended"
            requestBody["status"] = "active"
            requestBody["project_master_id"] = requestBody.get("account_id", None)
            response = create_tenant(accessToken, requestBody)
            if response.status_code == 200:
                return marshal(response.json(), createResponseModel), 201
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id='listTenant', name="ListTenant",
             description="There can be multiple tenants within a CoreStack account. List "
                         "all tenants the user is mapped under a CoreStack account. If "
                         "there are 3 tenants and user performing this operation has "
                         "access to only 2 tenants then only those 2 tenants will be "
                         "returned.",
             security=['auth_user', 'auth_token'])
    @tenant_name_space.response(model=listResponseModel, code=200, description='Success', as_list=True)
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self):
        try:
            accessToken = request.headers.get("X-Auth-User")
            response = get_tenants(accessToken)
            if response.status_code == 200:
                responseJson = marshal(response.json(), listResponseModel)
                # for t in responseJson.get('tenants'):
                    # t['account_name'] = t.pop('project_master_name', None)
                    # t['account_id'] = t.pop('project_master_id', None)
                    # t.pop('preferences', None)
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

    @api.doc(id='getTenant', name="GetTenant Request", description="Retreive a tenant by its Id.  If you're unsure of the tenant_id, "
                                                   "use listTenant operation to list all tenants under a CoreStack "
                                                   "account and fetch the needed tenant_id.",
             params={'tenant_id': 'Id of the tenant ot be retrieved.'}, security=['auth_user', 'auth_token'])
    @tenant_name_space.response(model=getResponseModel, code=200, description='Success')
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
                rJson = marshal(t, getResponseModel, ordered=True)
                rJson['metadata'] = t['metadata']
                return rJson, 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id='updateTenant', name="PutTenant Request", description="Update a tenant's status, description & "
                                                                      "metadata using its id. No operation can be "
                                                                      "performed when a tenant is made suspended.",
             params={'tenant_id': 'Id of the CoreStack account under which the tenant to be updated.'},
             security=['auth_user', 'auth_token'])
    @api.expect(updateTenantReqModel, validate=True)
    @tenant_name_space.response(model=updateResponseModel, code=200, description='Success')
    @tenant_name_space.response(model=errorModel, code=400, description='Bad Request')
    @tenant_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @tenant_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, tenant_id):
        try:
            accessToken = request.headers.get("X-Auth-User")
            requestBody = request.json
            # requestBody["status"] = "active" if bool(requestBody.get("status")) else "suspended"
            requestBody["project_master_id"] = requestBody.pop("account_id", None)
            response = update_tenant(accessToken, tenant_id, requestBody)
            if response.status_code == 200:
                return marshal(response.json(), updateResponseModel), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            tenant_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id='deleteTenant', name="DeleteTenant Request", description='Delete a tenant by its Id. Cannot undo this '
                                                                         'action, so be cautious when performing this '
                                                                         'operation. Use updateTenant to make the '
                                                                         'tenant as suspended if required.',
             params={'tenant_id': 'Id of the tenant to be deleted.'},
             security=['auth_user', 'auth_token'])
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
