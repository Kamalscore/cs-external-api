# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from definitions.script_definitions import ScriptURLDefinitions
from models.script_models import script_response_list, \
    script_data_model_list, script_delete_response, script_data_model_view, script_data_model_create, \
    script_info_model, script_minimum_requirements_model, script_create_update_response_model, \
    script_execute_response_model, script_execute_request, script_execute_job_input_model, script_data_model_scan, \
    script_scan_response_model
from models.swagger_models import error, wild_card_model
from utils.HelperUtils import getClassName, invoke_api

wildcardModel = api.model('Dict', wild_card_model())
script_name_space = api.namespace(name='Scripts', path="/", description='Manage Scripts')
scriptDataModelList = api.model('ScriptDataList', script_data_model_list())
scriptDataModelView = api.model('ScriptDataView', script_data_model_view(wildcardModel))
scriptInfoDataModel = api.model('ScriptInfo', script_info_model())
minimumReqDataModel = api.model('ScriptMinimumRequirements', script_minimum_requirements_model())
scanScriptReqModel = api.model('ScriptScanRequest', script_data_model_scan(scriptInfoDataModel))
scanResponseModel = api.model('ScanScriptResponse', script_scan_response_model(wildcardModel))
createScriptReqModel = api.model('CreateScriptRequest',
                                 script_data_model_create(scriptInfoDataModel, wildcardModel, minimumReqDataModel))
updateScriptReqModel = api.model('UpdateScriptRequest', script_data_model_create(scriptInfoDataModel, wildcardModel,
                                                                                 minimumReqDataModel))
createUpdateResponseModel = api.model('CreateScriptResponse', script_create_update_response_model())
executeScriptJobReqModel = api.model('ExecuteScriptJobData', script_execute_job_input_model(wildcardModel))
executeScriptReqModel = api.model('ExecuteScriptRequest', script_execute_request(executeScriptJobReqModel))
executeResponseModel = api.model('ExecuteResponse', script_execute_response_model())
scriptRemovalResModel = api.model('ScriptDeleteResponse', script_delete_response())
scriptResponseModelList = api.model('ScriptListResponse', script_response_list(scriptDataModelList))
errorModel = api.model('Error', error())
script_api_definition = ScriptURLDefinitions.URLInfo


@script_name_space.route("/v1/<string:tenant_id>/scripts")
class Scripts(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(Scripts))

    @api.doc(id='ListScripts', name="ListScripts Request",
             description='List all the scripts. '
                         'Global Scripts - All user will have access to Corestack\'s Marketplace Scripts'
                         ' (Can view and execute). Account - All users under that account will have access '
                         '(Can view and execute). Only Account admins can update/delete. Tenant - Users with access to'
                         ' the specific tenant will have access scripts (Can view and execute). Tenant admins can '
                         'update/delete. Private - User who created will only have access.',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'types': {'description': 'Script types to filter', 'in': 'query', 'type': 'str',
                           'enum': ['chef', 'ansible', 'puppet', 'shell']},
                 'category': {'description': 'Script types to filter', 'in': 'query', 'type': 'str',
                              'enum': ["Application", "Languages", "Database", "Security", "System", "Web Server",
                                       "Others"]},
                 'limit': {'description': 'Number of records to display', 'type': 'integer',
                           'enum': [10, 25, 50, 100]},
                 'page': {'description': 'Page number', 'type': 'integer'}
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
                return marshal(response.json(), errorModel), response.status_code

        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id='CreateScript',
             name="CreateScript Request",
             description='Creates a new script under the tenant. '
                         'However the script will be accessible based on its scope. '
                         'Global Scripts - All user will have access to Corestack\'s Marketplace Scripts'
                         ' (Can view and execute). Account - All users under that account will have access '
                         '(Can view and execute). Only Account admins can update/delete. Tenant - Users with access to'
                         ' the specific tenant will have access scripts (Can view and execute). Tenant admins can '
                         'update/delete. Private - User who created will only have access.',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'}
             })
    @api.expect(createScriptReqModel, validate=True)
    @script_name_space.response(model=createUpdateResponseModel, code=201, description='Created')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, createScriptReqModel, ordered=True, skip_none=True)
            req_body['file_authentication'] = False
            req_body['input_source'] = 'Script'
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


@script_name_space.route("/v1/<string:tenant_id>/scripts/<script_id>")
class ScriptByID(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptByID))

    @api.doc(id='DescribeScript', name="DescribeScript Request",
             description='This API will provide detailed information about the script.',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'script_id': {'description': 'ID of the script. This can be fetched from listScripts API'}
             }
             )
    @script_name_space.response(model=scriptDataModelView, code=200, description='Success')
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
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id='UpdateScript', name="UpdateScript Request", description='Updates script details such as name, '
                                                                         'script path, dependencies etc.,',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'script_id': {'description': 'ID of the script. This can be fetched from listScripts API'}
             }
             )
    @api.expect(createScriptReqModel, validate=True)
    @script_name_space.response(model=createUpdateResponseModel, code=200, description='Updated')
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

    @api.doc(id='DeleteScript', name="DeleteScript Request", description='Deletes a script. Cannot undo this action, '
                                                                         'so be cautious when performing this operation.'
                                                                         ' Use updateScript to make the script as '
                                                                         'inactive if required',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'script_id': {'description': 'ID of the script. This can be fetched from listScripts API'}
             })
    @script_name_space.response(model=scriptRemovalResModel, code=200, description='Deleted')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def delete(self, tenant_id, script_id):
        try:
            format_params = {
                'tenant_id': tenant_id,
                'script_id': script_id
            }
            args = request.args
            headers = request.headers
            response = invoke_api(script_api_definition, 'delete', format_params, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), scriptRemovalResModel, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@script_name_space.route("/v1/<string:tenant_id>/scripts/scan")
class ScanScript(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScanScript))

    @api.doc(id='ScanScript', name="ScanScript Request",
             description='Scans a script to check if all dependencies(if any) are '
                         'satisfied. This API will also return '
                         'parameters available in script for chef and '
                         'parameter & hosts available in the script for ansible',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'script_id': {'description': 'ID of the script. This can be fetched from listScripts API'}
             }
             )
    @api.expect(scanScriptReqModel, validate=True)
    @script_name_space.response(model=scanResponseModel, code=201, description='Scanned successfully')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, scanScriptReqModel, ordered=True, skip_none=True)
            req_body['file_authentication'] = False
            format_params = {
                'tenant_id': tenant_id
            }
            args = request.args
            headers = request.headers
            response = invoke_api(script_api_definition, 'scan', format_params, req_body, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), scanResponseModel, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@script_name_space.route("/v1/<string:tenant_id>/scripts/execute")
class ExecuteScript(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ExecuteScript))

    @api.doc(id='ExecuteScript',
             name="Execute Script Request", description='Execute scripts. Ansible script supports executing single '
                                                        'script in multiple machines. Chef/Puppet/Shell executing '
                                                        'multiple scripts against multiple target machines.',
             security=['auth_user', 'auth_token'],
             params={
                 'tenant_id': {'description': 'ID of the tenant. This can be fetched from listTenants API'},
                 'script_id': {'description': 'ID of the script. This can be fetched from listScripts API'}
             }
             )
    @api.expect(executeScriptReqModel, validate=True)
    @script_name_space.response(model=executeResponseModel, code=200, description='Execution Initiated')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, executeScriptReqModel, ordered=True, skip_none=True)
            req_body['job_details'] = req_body.pop('host_details', None)
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
