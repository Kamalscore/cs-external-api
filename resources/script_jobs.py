# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from definitions.script_definitions import ScripJobtURLDefinitions
from models.script_job_models import script_job_job_info_model, script_job_script_info_data_model, script_job_view_model
from models.swagger_models import error, wild_card_model
from utils.HelperUtils import getClassName, invoke_api

wildcardModel = api.model('Dict', wild_card_model())
script_job_name_space = api.namespace(name='ScriptJobs', path="/", description='Manage Script Jobs')
scriptJobScriptInfoDataModel = api.model('ScriptJobScriptInfo', script_job_script_info_data_model(wildcardModel))
scriptJobInfoDataModel = api.model('ScriptJobInfo', script_job_job_info_model(scriptJobScriptInfoDataModel))
scriptJobDataModelView = api.model('ScriptJobDataView', script_job_view_model(scriptJobInfoDataModel))
errorModel = api.model('Error', error())
script_job_api_definition = ScripJobtURLDefinitions.URLInfo


@script_job_name_space.route("/v1/<string:tenant_id>/scriptjobs/<script_job_id>")
class ScriptResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(ScriptResource))

    @api.doc(name="ViewScriptJob Request",
             description='View script job details.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'}
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
            response = invoke_api(script_job_api_definition, 'view', format_params, args=args, headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), scriptJobDataModelView, ordered=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            script_job_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
