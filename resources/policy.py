# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import json
import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from definitions.policy_definitions import PolicyURLDefinitions
from models.policy_models import policy_delete_response, policy_create_model, create_policy_data_model, \
    policy_view_response, policy_metadata_model, policy_update_response, policy_update_model, policy_data_model_list, \
    policy_response_list, policy_execute_model, service_account_details, policy_execute_response, policy_job_response
from models.swagger_models import error, wild_card_model
from utils.HelperUtils import getClassName, invoke_api

policy_name_space = api.namespace(name='Policy', path="/", description='Manage Policy')
wildcardModel = api.model('Dict', wild_card_model())
service_account_details = api.model("", service_account_details())
scriptDataModelList = api.model('PolicyDataList', policy_data_model_list())
policyMetadataModel = api.model('PolicyMetadata', policy_metadata_model())
createPolicyReqModel = api.model('CreatePolicyRequest', policy_create_model())
updatePolicyReqModel = api.model('UpdatePolicyRequestModel', policy_update_model(policyMetadataModel))
create_policy_data_model = api.model('PolicyData', create_policy_data_model())
policyUpdateResponse = api.model('UpdatePolicyRequest', policy_update_response())
PolicyRemovalResModel = api.model('PolicyRemovalResponse', policy_delete_response())
PolicyViewResponse = api.model("PolicyViewResponse", policy_view_response())
PolicyResponseModelList = api.model('PolicyListResponse', policy_response_list(scriptDataModelList))
executePolicyReqModel = api.model('PolicyExecuteRequestModel', policy_execute_model(wildcardModel,
                                                                                    service_account_details))
executePolicyResponseModel = api.model("PolicyExecuteResponseModel", policy_execute_response())
jobDetailsResponseModel = api.model("JobExecutionDetailsResponseModel", policy_job_response())
errorModel = api.model('Error', error())
script_api_definition = PolicyURLDefinitions.URLInfo


@policy_name_space.route("/v1/<string:tenant_id>/policies")
class PolicyResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(PolicyResource))

    @api.doc(name="CreatePolicy Request", description='Creates a new Policy.',
             params={"tenant_id": "Specify the tenant Id for the policy"},
             security=['auth_user', 'auth_token'])
    @api.expect(createPolicyReqModel, validate=True)
    @policy_name_space.response(model=create_policy_data_model, code=201, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id}
            response = invoke_api(script_api_definition, 'create', format_params, args=args, headers=headers,
                                  req_body=request.json)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), create_policy_data_model)
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)

    @api.doc(name="ListPolicy Request", description='List all the Policies',
             params={"tenant_id": "Specify the tenant Id for the policy"},
             security=['auth_user', 'auth_token'])
    @policy_name_space.response(model=PolicyResponseModelList, code=200, description='Success', as_list=True)
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id}
            response = invoke_api(script_api_definition, 'list', format_params, args=args, headers=headers)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), PolicyResponseModelList)
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)


@policy_name_space.route("/v1/<string:tenant_id>/policies/<string:policy_id>")
class PolicyResourceById(Resource):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(PolicyResourceById))

    @api.doc(name="View Policy Request", description='view the created policy with policy id and tenant id',
             params={"tenant_id": "Specify the tenant Id for the policy",
                     "policy_id": "specify the policy id to retrieve"},
             security=['auth_user', 'auth_token'])
    @policy_name_space.response(model=PolicyViewResponse, code=200, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, policy_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, "policy_id": policy_id}
            response = invoke_api(script_api_definition, 'view', format_params, args=args, headers=headers)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), PolicyViewResponse), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)

    @api.doc(name="Update Policy Request", description='update policy with policy id and tenant id',
             params={"tenant_id": "Specify the tenant Id for the policy",
                     "policy_id": "specify the policy id to update"},
             security=['auth_user', 'auth_token'])
    @api.expect(updatePolicyReqModel, validate=True)
    @policy_name_space.response(model=policyUpdateResponse, code=200, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, tenant_id, policy_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, "policy_id": policy_id}
            response = invoke_api(script_api_definition, 'update', format_params, args=args, headers=headers,
                                  req_body=request.json)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), policyUpdateResponse), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)

    @api.doc(name="Delete Policy Request", description='delete policy with policy id and tenant id',
             params={"tenant_id": "Specify the tenant Id for the policy",
                     "policy_id": "specify the policy id to delete"},
             security=['auth_user', 'auth_token'])
    @policy_name_space.response(model=PolicyRemovalResModel, code=200, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def delete(self, tenant_id, policy_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, "policy_id": policy_id}
            response = invoke_api(script_api_definition, 'delete', format_params, args=args, headers=headers)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), PolicyRemovalResModel), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)


@policy_name_space.route("/v1/<string:tenant_id>/policies/<string:policy_id>/execute")
class PolicyActionsByName(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(PolicyActionsByName))

    @api.doc(name="Execute Policy Request", description='Execute a Policy',
             params={"tenant_id": "Specify the tenant Id for the policy",
                     "policy_id": "specify the policy id to retrieve"}, security=['auth_user', 'auth_token'])
    @api.expect(executePolicyReqModel, validate=True)
    @policy_name_space.response(model=executePolicyResponseModel, code=201, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id, policy_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, 'policy_id': policy_id}
            response = invoke_api(script_api_definition, 'execute', format_params, args=args, headers=headers,
                                  req_body=request.json)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), executePolicyResponseModel)
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)


@policy_name_space.route("/v1/<string:tenant_id>/policy_jobs/<string:job_id>")
class PolicyJobs(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(PolicyJobs))

    @api.doc(name="Policy Job details request", description='Retrieve policy job details using the job id',
             params={"tenant_id": "Specify the tenant Id for the policy",
                     "job_id": "specify the job id to retrieve details of policy execution"},
             security=['auth_user', 'auth_token'])
    @policy_name_space.response(model=jobDetailsResponseModel, code=200, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, job_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, "job_id": job_id}
            response = invoke_api(script_api_definition, 'job_details', format_params, args=args, headers=headers)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), jobDetailsResponseModel), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)
