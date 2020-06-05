# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from definitions.script_definitions import ScriptURLDefinitions
from models.script_models import script_response_list, script_metadata_model, \
    script_data_model_list, script_delete_response, script_data_model_view, script_data_model_create, \
    script_info_model, script_minimum_requirements_model, script_create_update_response_model, \
    script_execute_response_model, script_execute_request, script_execute_job_input_model
from models.swagger_models import error, wild_card_model
from utils.HelperUtils import getClassName, invoke_api

wildcardModel = api.model('Dict', wild_card_model())
script_name_space = api.namespace(name='Scripts', path="/", description='Manage Scripts')
scriptMetadataModel = api.model('ScriptMetadata', script_metadata_model())
scriptDataModelList = api.model('ScriptDataList', script_data_model_list())
scriptDataModelView = api.model('ScriptDataView', script_data_model_view(wildcardModel))
scriptInfoDataModel = api.model('ScriptInfo', script_info_model())
minimumReqDataModel = api.model('ScriptMinimumRequirements', script_minimum_requirements_model())
createScriptReqModel = api.model('CreateScriptRequest',
                                 script_data_model_create(scriptInfoDataModel, wildcardModel, minimumReqDataModel))
updateScriptReqModel = api.model('UpdateScriptRequest', script_data_model_create(scriptInfoDataModel, wildcardModel,
                                                                                 minimumReqDataModel))
createUpdateResponseModel = api.model('CreateScriptResponse', script_create_update_response_model())
executeScriptJobReqModel = api.model('ExecuteScriptJobData', script_execute_job_input_model(wildcardModel))
executeScriptReqModel = api.model('ExecuteScriptRequest', script_execute_request(script_execute_request))
executeResponseModel = api.model('ExecuteResponse', script_execute_response_model())
scriptRemovalResModel = api.model('ScriptDeleteResponse', script_delete_response())
scriptResponseModelList = api.model('ScriptListResponse', script_response_list(scriptDataModelList))
errorModel = api.model('Error', error())
script_api_definition = ScriptURLDefinitions.URLInfo


@script_name_space.route("/v1/<string:tenant_id>/scripts")
class ScriptResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptResource))

    @api.doc(name="CreateScript Request", description='Creates a new script.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'}})
    @api.expect(createScriptReqModel, validate=True)
    @script_name_space.response(model=scriptResponseModelList, code=201, description='Created')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, createScriptReqModel, ordered=True, skip_none=True)
            format_params = {
                'tenant_id': tenant_id
            }
            args = request.args
            headers = request.headers
            response = invoke_api(script_api_definition, 'create', format_params, req_body, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), createUpdateResponseModel, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="ListScripts Request",
             description='List all the scripts.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'},
                 'types': {'description': 'Script types to filter', 'in': 'query', 'type': 'str',
                           'enum': ['chef', 'ansible', 'puppet', 'shell']}
             })
    @script_name_space.response(model=scriptResponseModelList, code=200, description='Success')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id}
            response = invoke_api(script_api_definition, 'list', format_params, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), scriptResponseModelList, ordered=True), 200
            else:
                # TODO Need to raise the proper errors by checking the status like 400, 401, 403 etc...
                return marshal(response.json(), errorModel), response.status_code

        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@script_name_space.route("/v1/<string:tenant_id>/scripts/execute")
class ScriptResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptResource))

    @api.doc(name="Execute Script Request", description='Execute a script.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'}})
    @api.expect(executeScriptReqModel, validate=True)
    @script_name_space.response(model=scriptResponseModelList, code=201, description='Created')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, createScriptReqModel, ordered=True, skip_none=True)
            format_params = {
                'tenant_id': tenant_id
            }
            args = request.args
            headers = request.headers
            response = invoke_api(script_api_definition, 'execute', format_params, req_body, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), executeResponseModel, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@script_name_space.route("/v1/<string:tenant_id>/scripts/<script_id>")
class ScriptResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptResource))

    @api.doc(name="UpdateScript Request", description='Updates a new script.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'},
                 'types': {'description': 'Script types to filter', 'in': 'query', 'type': 'str',
                           'enum': ['chef', 'ansible', 'puppet', 'shell']}
             })
    @api.expect(createScriptReqModel, validate=True)
    @script_name_space.response(model=createUpdateResponseModel, code=201, description='Updated')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, tenant_id, script_id):
        try:
            req_body = marshal(request.json, createScriptReqModel, ordered=True, skip_none=True)
            format_params = {
                'tenant_id': tenant_id,
                'script_id': script_id
            }
            args = request.args
            headers = request.headers
            response = invoke_api(script_api_definition, 'update', format_params, req_body, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), createUpdateResponseModel, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="UpdateScript Request",
             description='Update a script.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'}
             })
    @script_name_space.response(model=createUpdateResponseModel, code=200, description='Success')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, script_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id, 'script_id': script_id}
            response = invoke_api(script_api_definition, 'view', format_params, args=args, headers=headers)
            if response.status_code == 200:
                marshalled_resp = marshal(response.json(), scriptDataModelView, ordered=True, skip_none=True)
                SCRIPT_TECHNICAL_NAME = dict(chef='cookbook', puppet='module',
                                             shell='shell_script', ansible='playbook')
                marshalled_resp['script_info'] = {
                    'name': marshalled_resp.get('%s_name' % SCRIPT_TECHNICAL_NAME[marshalled_resp['type']]),
                    'path': marshalled_resp.get('%s_path' % SCRIPT_TECHNICAL_NAME[marshalled_resp['type']]),
                    'path_type': marshalled_resp.get('path_type')
                }
                marshalled_resp.pop('%s_name' % SCRIPT_TECHNICAL_NAME[marshalled_resp['type']], None)
                marshalled_resp.pop('%s_path' % SCRIPT_TECHNICAL_NAME[marshalled_resp['type']], None)
                marshalled_resp.pop('path_type', None)
                return marshalled_resp, 200
            else:
                # TODO Need to raise the proper errors by checking the status like 400, 401, 403 etc...
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
