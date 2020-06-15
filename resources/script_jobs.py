# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION, CS_ENDPOINT_URL_DEFAULT_VALUE, \
    CS_ENDPOINT_URL_PROPERTY_NAME
from definitions.script_job_definitions import ScripJobURLDefinitions
from models.script_job_models import script_job_job_info_model, script_job_script_info_data_model, \
    script_job_view_model, script_job_list_model, script_job_list_response
from models.swagger_models import error, wild_card_model
from utils.HelperUtils import getClassName, invoke_api

wildcardModel = api.model('Dict', wild_card_model())
script_job_name_space = api.namespace(name='ScriptJobs', path="/", description='Manage Script Jobs')
scriptJobDataModelList = api.model('ScriptJobListModel', script_job_list_model())
scriptJobResponseModelList = api.model('ScriptJobListResponse', script_job_list_response(scriptJobDataModelList))
scriptJobScriptInfoDataModel = api.model('ScriptJobScriptInfo', script_job_script_info_data_model(wildcardModel))
scriptJobInfoDataModel = api.model('ScriptJobInfo', script_job_job_info_model(scriptJobScriptInfoDataModel))
scriptJobDataModelView = api.model('ScriptJobDataView', script_job_view_model(scriptJobInfoDataModel))
errorModel = api.model('Error', error())
script_job_api_definition = ScripJobURLDefinitions.URLInfo


@script_job_name_space.route("/v1/<string:tenant_id>/scriptjobs")
class DescribeScriptJob(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(DescribeScriptJob))

    @api.doc(id='ListScriptJobs', name="ListScriptJobs Request",
             description='This API will list all script jobs initiated by the logged in user.',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'limit': {'description': 'Number of records to display', 'type': 'integer',
                           'enum': [10, 25, 50, 100]},
                 'page': {'description': 'Page number', 'type': 'integer'}
             })
    @script_job_name_space.response(model=scriptJobResponseModelList, code=200, description='Success')
    @script_job_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_job_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_job_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id}
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(script_job_api_definition, 'list', format_params, args=args, headers=headers,
                                  base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), scriptJobResponseModelList, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_job_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@script_job_name_space.route("/v1/<string:tenant_id>/scriptjobs/<script_job_id>")
class DescribeScriptJob(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(DescribeScriptJob))

    @api.doc(id='DescribeScriptJob', name="ViewScriptJob Request",
             description='View script job details.',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'script_job_id': {'description': 'ID of the script_job. This can be fetched from listScriptJobs API/'
                                                  'scriptExecute response'}
             })
    @script_job_name_space.response(model=scriptJobDataModelView, code=200, description='Success')
    @script_job_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_job_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_job_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, script_job_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id, 'script_job_id': script_job_id}
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(script_job_api_definition, 'view', format_params, args=args, headers=headers,
                                  base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), scriptJobDataModelView, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_job_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
