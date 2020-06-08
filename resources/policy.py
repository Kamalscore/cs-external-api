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
policyDataModelList = api.model('PolicyDataList', policy_data_model_list())
policyMetadataModel = api.model('PolicyMetadata', policy_metadata_model())
createPolicyReqModel = api.model('CreatePolicyRequest', policy_create_model())
updatePolicyReqModel = api.model('UpdatePolicyRequestModel', policy_update_model(policyMetadataModel))
create_policy_data_model = api.model('PolicyData', create_policy_data_model())
policyUpdateResponse = api.model('UpdatePolicyRequest', policy_update_response())
PolicyRemovalResModel = api.model('PolicyRemovalResponse', policy_delete_response())
PolicyViewResponse = api.model("PolicyViewResponse", policy_view_response())
PolicyResponseModelList = api.model('PolicyListResponse', policy_response_list(policyDataModelList))
executePolicyReqModel = api.model('PolicyExecuteRequestModel', policy_execute_model(wildcardModel,
                                                                                    service_account_details))
executePolicyResponseModel = api.model("PolicyExecuteResponseModel", policy_execute_response())
jobDetailsResponseModel = api.model("JobExecutionDetailsResponseModel", policy_job_response())
errorModel = api.model('Error', error())
policy_api_definition = PolicyURLDefinitions.URLInfo


@policy_name_space.route("/v1/<string:tenant_id>/policies")
class PolicyResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(PolicyResource))

    @api.doc(id="CreatePolicy", name="CreatePolicy Request",
             description='Creates a new policy under the tenant which will generate a unique policy id in the response'
                         'this is can be used to describe details about the policy, update policy, execute or delete '
                         'policy. However the policy will be accessible based on its  '
                         'scope  Account scope - All users under that account will have access to describe and '
                         'execute. Only Account admins can update/delete. Tenant - Users with access to the specific '
                         'tenant will have access scripts to describe and execute. Tenant admins can update/delete. '
                         'Private - User who created will only have access.',
             params={"tenant_id": "Specify the tenant Id to create policy which is a unique id "
                                  "can be retrieved using the list tenant api"},
             security=['auth_user', 'auth_token'])
    @api.expect(createPolicyReqModel, validate=True)
    @policy_name_space.response(model=create_policy_data_model, code=201, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            t = request.json
            services = t.pop("cloud")
            t["services"] = services
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id}
            response = invoke_api(policy_api_definition, 'create', format_params, args=args, headers=headers,
                                  req_body=t)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), create_policy_data_model)
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)

    @api.doc(id="ListPolicies", name="ListPolicies Request",
             description='List all the policies. Global Policies Scope- All '
                         'user will have access to Corestack Marketplace Policies these policies cannot '
                         'be updated and deleted can be only describe and executed. Account Scope:- All users under '
                         'that account will have access to view and execute Only Account admins can '
                         'update/delete the policies.Tenant Scope - Users with access to the specific tenant will have '
                         'access to policies who can describe or execute policies. Tenant admins can  only '
                         'update/delete. Private Scope - User who created will only have access',
             params={"tenant_id": "Specify the tenant Id to list policies which is a unique id can be obtained using "
                                  " the list tenant api",
                     "engine_type": {'description': 'Engine types filter', 'in': 'query', 'type': 'str',
                                     'enum': ["azure_policy", "aws_config", "chef_inspec", "congress", ]},
                     'limit': {'description': 'Number of records to display', 'type': 'integer',
                               'enum': [10, 25, 50, 100]},
                     'page': {'description': 'Page number', 'type': 'integer'}
                     },
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
            response = invoke_api(policy_api_definition, 'list', format_params, args=args, headers=headers)
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

    @api.doc(id="DescribePolicy", name="Describe Policy Request", description="Describe the already created Polices",
             params={"tenant_id": "Specify the tenant Id to get policy which is a unique id can be obtained using "
                                  "the list tenant api",
                     "policy_id": "specify the policy id to retrieve which is a unique id can be obtained using list "
                                  "policy api"},
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
            response = invoke_api(policy_api_definition, 'view', format_params, args=args, headers=headers)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), PolicyViewResponse), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)

    @api.doc(id="UpdatePolicy", name="Update Policy Request",
             description='Update Policy details if required after creation using the api, the update by a user '
                         'depends on the scope of the policy created check create policy docs for more details on the '
                         'scope',
             params={"tenant_id": "Specify the tenant Id to update policy which is a unique id can be retrieved using "
                                  "the list tenant api",
                     "policy_id": "specify the policy id to update which is a unique id can be retrieved using list "
                                  "policy api"},
             security=['auth_user', 'auth_token'])
    @api.expect(updatePolicyReqModel, validate=True)
    @policy_name_space.response(model=policyUpdateResponse, code=200, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, tenant_id, policy_id):
        try:
            t = request.json
            services = t.pop("cloud")
            t["services"] = services
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, "policy_id": policy_id}
            response = invoke_api(policy_api_definition, 'update', format_params, args=args, headers=headers,
                                  req_body=t)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), policyUpdateResponse), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)

    @api.doc(id="DeletePolicy", name="Delete Policy Request", description='Delete a policy which is no more required',
             params={"tenant_id": "Specify the tenant Id to delete policy which is a unique id can be retrieved from "
                                  "the list tenant api",
                     "policy_id": "specify the policy id of the policy to delete, policy id is unique can be obtained "
                                  "from the list policy api"},
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
            response = invoke_api(policy_api_definition, 'delete', format_params, args=args, headers=headers)
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

    @api.doc(id="ExecutePolicy", name="Execute Policy Request",
             description='Execute policy will return a unique job id the status of the policy can be checked using the '
                         'Job details api where you can pass the unique id generated to get the details or errors if '
                         'any on execution',
             params={"tenant_id": "Specify the tenant Id of the policy to be executed, this can be obtained using the "
                                  "list tenant api",
                     "policy_id": "specify the policy id to execute, policy id can be obtained from the list policy "
                                  "api"}, security=['auth_user', 'auth_token'])
    @api.expect(executePolicyReqModel, validate=True)
    @policy_name_space.response(model=executePolicyResponseModel, code=201, description='Success')
    @policy_name_space.response(model=errorModel, code=400, description='Bad Request')
    @policy_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @policy_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id, policy_id):
        try:
            t = request.json
            cloud_accounts = t.pop("cloud_accounts")
            cloud_account_list = list()
            cloud_account = dict()
            for cloud in cloud_accounts:
                cloud_account["service_type"] = "Cloud"
                cloud_account["service_name"] = cloud["cloud"]
                cloud_account["id"] = cloud["cloud_account_id"]
                cloud_account_list.append(cloud_account)
            t["service_accounts"] = cloud_account_list
            headers = request.headers
            args = request.args
            format_params = {'project_id': tenant_id, 'policy_id': policy_id}
            response = invoke_api(policy_api_definition, 'execute', format_params, args=args, headers=headers,
                                  req_body=t)
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

    @api.doc(id="JobDetails", name="Policy Job details request",
             description='Retrieve policy job details using the unique job id, this can be used to check the status'
                         'of the policy execution or any failure',
             params={"tenant_id": "Specify the tenant Id for the policy which is a unique value can be obtained from "
                                  "the list tenant api",
                     "job_id": "specify the job id to retrieve details of policy execution, job id is unique can be "
                               "obtained from the execute policy response"},
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
            response = invoke_api(policy_api_definition, 'job_details', format_params, args=args, headers=headers)
            value = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
                return marshal(response.json(), jobDetailsResponseModel), 200
            else:
                raise Exception(value.get("message"))
        except Exception as e:
            policy_name_space.abort(response.status_code, message=value.get("message"),
                                    status=value.get("status"), statusCode=response.status_code)
