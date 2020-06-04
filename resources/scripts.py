# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

import logging

from flask import request, abort
from flask_restplus import Resource, marshal

from app import api
from definitions.script_definitions import ScriptURLDefinitions
from models.script_models import script_request, script_response, script_metadata_model, \
    script_data_model_list, script_delete_response
from models.swagger_models import error
from utils.HelperUtils import getClassName, invoke_api

script_name_space = api.namespace(name='Scripts', path="/", description='Manage Scripts')
scriptMetadataModel = api.model('ScriptMetadata', script_metadata_model())
scriptDataModelList = api.model('ScriptData', script_data_model_list())
createScriptReqModel = api.model('CreateScriptRequest', script_request(scriptMetadataModel))
updateScriptReqModel = api.model('UpdateScriptRequest', script_request(scriptMetadataModel))
scriptRemovalResModel = api.model('ScriptRemovalResponse', script_delete_response())
scriptResponseModelList = api.model('ScriptResponse', script_response(scriptDataModelList))
errorModel = api.model('Error', error())
script_api_definition = ScriptURLDefinitions.URLInfo


@script_name_space.route("/v1/<string:tenant_id>/scripts")
class ScriptResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptResource))

    @api.doc(name="CreateScript Request", description='Creates a new script.')
    @api.expect(createScriptReqModel, validate=True)
    @script_name_space.response(model=scriptResponseModelList, code=201, description='Created')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            return {
                "message": "New script created",
            }
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="ListScripts Request",
             description='List all the scripts.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'},
                 'types': {'description': 'Script types to filter', 'in': 'query', 'type': 'str',
                           'enum': ['chef', 'ansible', 'puppet', 'shell']},
                 # 'script': {'description': 'Script types to filter', 'in': 'path', 'type': 'str',
                 #  'enum': ['chef', 'ansible', 'puppet', 'shell']}
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
                raise abort(response.text.encode('utf8'))
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@script_name_space.route("/v1/<string:tenant_id>/scripts/<script_id>")
class ScriptResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptResource))

    @api.doc(name="UpdateScript Request", description='Updates a new script.')
    @api.expect(createScriptReqModel, validate=True)
    @script_name_space.response(model=scriptResponseModelList, code=201, description='Updated')
    @script_name_space.response(model=errorModel, code=400, description='Bad Request')
    @script_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @script_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id, script_id):
        try:
            return {
                "message": "Script updated",
            }
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(name="UpdateScript Request",
             description='Update a script.',
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
    def get(self, tenant_id, script_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id, 'script_id': script_id}
            response = invoke_api(script_api_definition, 'view', format_params, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), scriptDataModelList, ordered=True), 200
            else:
                # TODO Need to raise the proper errors by checking the status like 400, 401, 403 etc...
                raise abort(response.text.encode('utf8'))
        except Exception as e:
            script_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
