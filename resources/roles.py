# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging

from flask import request
from flask_restplus import marshal, Resource

from app import api
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION, CS_ENDPOINT_URL_DEFAULT_VALUE, \
    CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME
from definitions.role_definitions import RoleUrlDefinitions
from models.role_models import role_list_response, role_list_data
from models.swagger_models import error
from utils.HelperUtils import getClassName
from utils.HelperUtils import invoke_api

role_name_space = api.namespace(name='Roles', path="/",
                                description='Role Management')
RoleListData = api.model('RoleListData', role_list_data())
RoleListResponse = api.model('RoleListResponse', role_list_response(RoleListData))

errorModel = api.model('Error', error())

role_api_defn = RoleUrlDefinitions.URLInfo


@role_name_space.route("/v1/<string:tenant_id>/roles")
class RoleResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(RoleResource))

    @api.doc(id="ListRoles", name="ListRoles",
             description="This GET method is used to fetch the list of Roles available within a specific tenant.",
             security=['auth_user', 'auth_token']
             )
    @role_name_space.response(model=RoleListResponse, code=200, description='Success')
    @role_name_space.response(model=errorModel, code=400, description='Bad Request')
    @role_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @role_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            base_url = getProperty(WEB_CONFIG_SECTION, CS_IDENTITY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            format_params = {"tenant_id": tenant_id}
            response = invoke_api(role_api_defn, 'list', headers=request.headers,
                                  base_url=base_url, format_params=format_params
                                  )
            if response.status_code == 200:
                return marshal(response.json(), RoleListResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            role_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
