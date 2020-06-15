# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging

from flask import request
from flask_restplus import marshal, Resource

from app import api
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION, CS_ENDPOINT_URL_DEFAULT_VALUE, \
    CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME
from definitions.common_definitions import RequestMapping
from definitions.role_definitions import RoleUrlDefinitions
from definitions.user_definitions import UserUrlDefinitions
from models.swagger_models import error
from models.user_models import list_user_response_model, list_user_data, list_roles, list_role_assignment, \
    describe_user_response_model, user_delete_response_model, user_create_response_model, user_create_request_model, \
    add_role_assignment, user_update_request_model, change_password_request_model, change_timezone_request_model, \
    change_timezone_response_model, update_role_assignment, user_update_response_model, change_password_response_model,\
    change_timezone_data_model
from utils.HelperUtils import getClassName
from utils.HelperUtils import invoke_api
from utils.HelperUtils import request_marshal

user_name_space = api.namespace(name='Users', path="/",
                                description='User Management')
RoleList = api.model('RoleList', list_roles())
RoleAssignmentList = api.model('RoleAssignmentList', list_role_assignment(RoleList))
UserList = api.model('UserList', list_user_data(RoleAssignmentList))
UserListResponse = api.model('UserResponseList', list_user_response_model(UserList))
UserDescribeResponse = api.model('UserDescribeResponse', describe_user_response_model(RoleAssignmentList))
UserDeleteResponse = api.model('UserDeleteResponse', user_delete_response_model())
AddRoleAssignment = api.model('AddRoleAssignment', add_role_assignment())
UserCreateRequest = api.model('UserCreateRequest', user_create_request_model(AddRoleAssignment))
UserCreateResponse = api.model('UserCreateResponse', user_create_response_model())
UpdateRoleAssignment = api.model('UpdateRoleAssignment', update_role_assignment())
UserUpdateResponse = api.model('UserUpdateResponse', user_update_response_model())
UserUpdateRequest = api.model('UserUpdateRequest', user_update_request_model(UpdateRoleAssignment))
ChangePasswordRequest = api.model('ChangePasswordRequest', change_password_request_model())
ChangePasswordResponse = api.model('ChangePasswordResponse', change_password_response_model())
ChangeTimezoneRequest = api.model('ChangeTimezoneRequest', change_timezone_request_model())
ChangeTimezoneData = api.model('ChangeTimezoneData', change_timezone_data_model())
ChangeTimezoneResponse = api.model('ChangeTimezoneResponse', change_timezone_response_model(ChangeTimezoneData))

errorModel = api.model('Error', error())

user_api_defn = UserUrlDefinitions.URLInfo
role_api_defn = RoleUrlDefinitions.URLInfo
user_request_mapping = RequestMapping.create_user
change_timezone_mapping = RequestMapping.change_timezone


@user_name_space.route("/v1/users")
class UserResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(UserResource))

    @api.doc(id="CreateUser", name="CreateUser",
             description="Creates an user within a CoreStack account and assign different roles for different tenants. "
                         "There can be multiple tenants within a CoreStack account. User will be created at the account"
                         " level and mapped to multiple tenants as needed.",
             security=['auth_user', 'auth_token']
             )
    @api.expect(UserCreateRequest, validate=True)
    @user_name_space.response(model=UserCreateResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            req_body = request.json
            request_marshal(req_body, user_request_mapping)
            for item in req_body["roles"]:
                # To marshal tenant_id
                if "tenant_id" in item:
                    item["project_id"] = item.pop("tenant_id", "")
                # To marshal role_names
                if "role_names" in item:
                    format_params = {"tenant_id": item["project_id"]}
                    get_role_req = {"role_names": item["role_names"]}
                    response = invoke_api(role_api_defn, 'get_roleid', headers=request.headers, base_url=base_url,
                                          req_body=get_role_req, format_params=format_params)
                    if response.status_code == 200:
                        role_id_res = response.json()
                        item["roles"] = role_id_res["data"]["role_ids"]
                        item.pop("role_names", "")
                    else:
                        return marshal(response.json(), errorModel), response.status_code
            response = invoke_api(user_api_defn, 'create', headers=request.headers,
                                  base_url=base_url, req_body=req_body
                                  )
            if response.status_code == 200:
                return marshal(response.json(), UserCreateResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="ListUser", name="ListUser",
             description="List all users within a CoreStack account. ",
             security=['auth_user', 'auth_token']
             )
    @user_name_space.response(model=UserListResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(user_api_defn, 'list', headers=request.headers,
                                  base_url=base_url
                                  )
            if response.status_code == 200:
                return marshal(response.json(), UserListResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@user_name_space.route("/v1/users/<string:user_id>")
class UserResourceById(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(UserResource))

    @api.doc(id="DescribeUser", name="DescribeUser",
             description="Describes an User by ID. This provides detailed information about a user",
             security=['auth_user', 'auth_token']
             )
    @user_name_space.response(model=UserDescribeResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, user_id):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            format_params = {"user_id": user_id}
            response = invoke_api(user_api_defn, 'view', headers=request.headers,
                                  base_url=base_url, format_params=format_params
                                  )
            if response.status_code == 200:
                actual_response = response.json()
                response = (marshal(response.json(), UserDescribeResponse))
                if response.get("is_accesskey_available"):
                    response["access_key"] = actual_response["data"]["access_key"]
                return response, 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="UpdateUser", name="UpdateUser",
             description="Updates a user and their role assignment in multiple tenants.",
             security=['auth_user', 'auth_token']
             )
    @api.expect(UserUpdateRequest, validate=True)
    @user_name_space.response(model=UserUpdateResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, user_id):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            req_body = request.json
            request_marshal(req_body, user_request_mapping)
            # To marshal tenant_id
            for item in req_body.get("roles", []):
                # To marshal tenant_id
                if "tenant_id" in item:
                    item["project_id"] = item.pop("tenant_id", "")
                # To marshal role_names
                if "role_names" in item:
                    format_params = {"tenant_id": item["project_id"]}
                    get_role_req = {"role_names": item["role_names"]}
                    response = invoke_api(role_api_defn, 'get_roleid', headers=request.headers, base_url=base_url,
                                          req_body=get_role_req, format_params=format_params)
                    if response.status_code == 200:
                        role_id_res = response.json()
                        item["roles"] = role_id_res["data"]["role_ids"]
                        item.pop("role_names", "")
                    else:
                        return marshal(response.json(), errorModel), response.status_code
            format_params = {"user_id": user_id}
            response = invoke_api(user_api_defn, 'update', headers=request.headers,
                                  base_url=base_url, req_body=req_body, format_params=format_params
                                  )
            if response.status_code == 200:
                return marshal(response.json(), UserUpdateResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="DeleteUser", name="DeleteUser",
             description="Deletes the User from CoreStack system. This operation cannot be undone.",
             security=['auth_user', 'auth_token']
             )
    @user_name_space.response(model=UserDeleteResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def delete(self, user_id):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            format_params = {"user_id": user_id}
            response = invoke_api(user_api_defn, 'delete', headers=request.headers,
                                  base_url=base_url, format_params=format_params
                                  )
            if response.status_code == 200:
                return (marshal(response.json(), UserDeleteResponse)), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@user_name_space.route("/v1/users/<string:user_id>/changepassword")
class UserPasswordChange(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(UserPasswordChange))

    @api.doc(id="ChangePassword", name="ChangePassword",
             description="Update the password of the user. This password will be used for login to portal and it will "
                         "not affect the Access Key / Secret Key associated with the user. Cannot update password of"
                         " another user within the same CoreStack account. Can be updated for the user associated with"
                         " Access Key / Secret Key",
             security=['auth_user', 'auth_token']
             )
    @api.expect(ChangePasswordRequest, validate=True)
    @user_name_space.response(model=ChangePasswordResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, user_id):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            req_body = request.json
            format_params = {"user_id": user_id}
            response = invoke_api(user_api_defn, 'update_password', headers=request.headers,
                                  base_url=base_url, req_body=req_body, format_params=format_params
                                  )
            if response.status_code == 200:
                return marshal(response.json(), ChangePasswordResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@user_name_space.route("/v1/users/<string:user_id>/changetimezone")
class UserTimezoneChange(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(UserTimezoneChange))

    @api.doc(id="ChangeTimezone", name="ChangeTimezone",
             description="Update the timezone settings of the user. In CoreStack portal, wherever the datatime is shown"
                         " it is converted to the timezone set to the user. Cannot update timezone of another user "
                         "within the same CoreStack account. Can be updated for the user associated with Access Key /"
                         " Secret Key",
             security=['auth_user', 'auth_token']
             )
    @api.expect(ChangeTimezoneRequest, validate=True)
    @user_name_space.response(model=ChangeTimezoneResponse, code=200, description='Success')
    @user_name_space.response(model=errorModel, code=400, description='Bad Request')
    @user_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @user_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, user_id):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            format_params = {"user_id": user_id}
            req_body = request.json
            request_marshal(req_body, change_timezone_mapping)
            response = invoke_api(user_api_defn, 'update_timezone', headers=request.headers,
                                  base_url=base_url, req_body=req_body, format_params=format_params
                                  )
            if response.status_code == 200:
                return marshal(response.json(), ChangeTimezoneResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            user_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
