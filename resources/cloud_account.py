# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging

from flask import request
from flask_restplus import marshal, Resource

from app import api
from definitions.service_account_definitions import ServiceAccountUrlDefinitions
from models.service_account_models import aws_cloud_account_auth_values_model, cloud_account_request_model, \
    cloud_account_create_response_model, cloud_account_dependency_response_model, cloud_account_delete_response_model, \
    wild_card_model, azure_cloud_account_auth_values_model, cloud_account_response_model_list, \
    cloud_account_data_model_list, cloud_account_response_model_view, cloud_account_rediscover_response
from models.swagger_models import error
from utils.HelperUtils import getClassName
from utils.HelperUtils import invoke_api

cloud_account_name_space = api.namespace(name='CloudAccounts', path="/",
                                         description='Manage Cloud Accounts')
CloudAccountList = api.model('CloudAccountList', cloud_account_data_model_list())
CloudAccountListResponse = api.model('CloudAccountListResponse',
                                     cloud_account_response_model_list(CloudAccountList))
WildCardModel = api.model('WildCardModel', wild_card_model())
CloudAccountDescribeResponse = api.model('CloudAccountDescribeResponse',
                                         cloud_account_response_model_view(WildCardModel))
errorModel = api.model('Error', error())

AWSCloudAccountAuthValues = api.model('AWSCloudAccountAuthValues', aws_cloud_account_auth_values_model())
CloudAccountCreateRequest = api.model('CloudAccountCreateRequest',
                                      cloud_account_request_model(AWSCloudAccountAuthValues), for_doc_alone=True)
AWSCloudAccountUpdateRequest = api.model('CloudAccountUpdateRequest',
                                         cloud_account_request_model(AWSCloudAccountAuthValues))
AzureCloudAccountAuthValues = api.model('AzureCloudAccountAuthValues',
                                        azure_cloud_account_auth_values_model(), for_doc_alone=True)
CloudAccountCreateResponse = api.model('CloudAccountCreateResponse', cloud_account_create_response_model())
CloudAccountUpdateResponse = api.model('CloudAccountUpdateResponse', cloud_account_create_response_model())
CloudAccountDeleteResponse = api.model('CloudAccountDeleteResponse', cloud_account_delete_response_model())
CloudAccountDependencyResponse = api.inherit('CloudAccountDependencyResponse',
                                             CloudAccountDeleteResponse,
                                             cloud_account_dependency_response_model(WildCardModel))
CloudAccountRediscoverResponse = api.model('CloudAccountRediscoverResponse',
                                           cloud_account_rediscover_response())
service_account_api_defn = ServiceAccountUrlDefinitions.URLInfo


@cloud_account_name_space.route("/v1/<string:tenant_id>/cloud_accounts")
class CloudAccountResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(CloudAccountResource))

    @api.doc(id="CreateCloudAccount", name="CreateCloudAccount",
             description="Create a cloud account for a specific service for a given tenant. \
                         Service implies any Cloud platform that is integrated with CoreStack.The specified auth values\
                         should be passed based on the cloud service.Below\
                         mentioned auth_values in the request model is to create AWS Cloud account."
                         "Refer <u>AzureCloudAccountAuthValues</u> to replace auth_values for Azure cloud account.",
             security=['auth_user', 'auth_token'],
             params={"service": {"description": "Available cloud services", "in": "query", "type": "str",
                                 "enum": ["AWS", "Azure"]}
                     })
    @api.expect(CloudAccountCreateRequest, validate=False)
    @cloud_account_name_space.response(model=CloudAccountCreateResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            format_params = {
                'tenant_id': tenant_id
            }
            service = request.args.get("service")
            if not service:
                return marshal({"message": "Service is mandatory."}, errorModel), 400
            req_body = request.json
            if not req_body:
                return marshal({"message": "Missing request payload."}, errorModel), 400
            req_body.update(service=service, service_type="Cloud", settings="none")
            auth_values = req_body.get("auth_values")
            # Service AWS
            if service == "AWS":
                if auth_values.get("account_type") == "master_account" and not auth_values.get("bucket_name"):
                    return marshal({"message": "bucket_name is mandatory for account_type 'master_account'"},
                                   errorModel), 400
                if auth_values.get("account_type") == "linked_account" and not auth_values.get("master_account"):
                    return marshal({"message": "master_account is mandatory for account_type 'linked_account'"},
                                   errorModel), 400
            # Service Azure
            if service == "Azure":
                req_body.update(cloud_type="Azure_Global")
            response = invoke_api(service_account_api_defn, 'create', args=request.args, headers=request.headers,
                                  format_params=format_params, req_body=req_body)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountCreateResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e or e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="ListCloudAccounts", name="ListCloudAccounts",
             description='List all cloud accounts for a given tenant.',
             security=['auth_user', 'auth_token'],
             params={"services": {"description": "Available cloud services", "in": "query", "type": "str",
                                  "enum": ["AWS", "Azure"], "default": ""}
                     })
    @cloud_account_name_space.response(model=CloudAccountListResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            args = request.args
            if not args.get("services"):
                args = {"service_type": "Cloud"}
            format_params = {
                'tenant_id': tenant_id
            }
            response = invoke_api(service_account_api_defn, 'list', args=args, headers=request.headers,
                                  format_params=format_params)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountListResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@cloud_account_name_space.route("/v1/<string:tenant_id>/cloud_accounts/<string:cloud_account_id>")
class CloudAccountResourceById(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(CloudAccountResourceById))

    @api.doc(id="DescribeCloudAccount", name="DescribeCloudAccount",
             description="Get details of a specific cloud account within a given tenant.",
             security=['auth_user', 'auth_token'])
    @cloud_account_name_space.response(model=CloudAccountDescribeResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, cloud_account_id):
        try:
            format_params = {
                'tenant_id': tenant_id,
                'service_account_id': cloud_account_id
            }
            response = invoke_api(service_account_api_defn, 'view', headers=request.headers,
                                  format_params=format_params)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountDescribeResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="UpdateCloudAccount", name="UpdateCloudAccount",
             description="Update cloud account with specified value for the service for a given tenant.The specified auth values\
                         should be passed based on the cloud service.Below\
                         mentioned auth_values in the request model is for AWS Cloud account."
                         "Refer <u>AzureCloudAccountAuthValues</u> to replace auth_values for Azure.",
             security=['auth_user', 'auth_token'],
             params={"service": {"description": "Available cloud services", "in": "query", "type": "str",
                                 "enum": ["AWS", "Azure"]}
                     })
    @api.expect(AWSCloudAccountUpdateRequest, validate=True)
    @cloud_account_name_space.response(model=CloudAccountUpdateResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def put(self, tenant_id, cloud_account_id):
        try:
            format_params = {
                'tenant_id': tenant_id,
                'service_account_id': cloud_account_id
            }
            service = request.args.get("service")
            if not service:
                return marshal({"message": "Service is mandatory."}, errorModel), 400
            req_body = request.json
            if not req_body:
                return marshal({"message": "Missing request payload."}, errorModel), 400
            req_body.update(service=service, service_type="Cloud", settings="none")
            auth_values = req_body.get("auth_values")
            # Service AWS
            if service == "AWS":
                if auth_values.get("account_type") == "master_account" and not auth_values.get("bucket_name"):
                    return marshal({"message": "bucket_name is mandatory for account_type 'master_account'"},
                                   errorModel), 400
                if auth_values.get("account_type") == "linked_account" and not auth_values.get("master_account"):
                    return marshal({"message": "master_account is mandatory for account_type 'linked_account'"},
                                   errorModel), 400
            # Service Azure
            if service == "Azure":
                req_body.update(cloud_type="Azure_Global")
            response = invoke_api(service_account_api_defn, 'update', args=request.args, headers=request.headers,
                                  format_params=format_params, req_body=req_body)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountUpdateResponse), 201
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="DeleteCloudAccount", name="DeleteCloudAccount",
             description="Delete a specific cloud account for a given tenant.",
             security=['auth_user', 'auth_token'],
             params={"action": {"description": "<u><b>Action to delete a Cloud account</b></u>: Below "
                                               "mentioned Response model is obtained when the "
                                               "<i><b>action</b></i> "
                                               "is <i>list</i> to get the dependencies of a Cloud account. Please find "
                                               "the model: <b>CloudAccountDeleteResponse</b>, when the "
                                               "<i><b>action</b></i> is <i>delete</i>.", "in": "query", "type": "str",
                                "enum": ["list", "delete"]}
                     })
    @cloud_account_name_space.response(model=CloudAccountDependencyResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=CloudAccountDeleteResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def delete(self, tenant_id, cloud_account_id):
        try:
            format_params = {
                'tenant_id': tenant_id,
                'service_account_id': cloud_account_id
            }
            action = request.args.get("action")
            if not action:
                return marshal({"message": "Action is mandatory."}, errorModel), 400
            response = invoke_api(service_account_api_defn, 'delete', headers=request.headers,
                                  format_params=format_params, args=request.args)
            if response.status_code == 200:
                return marshal(response.json(),
                               CloudAccountDependencyResponse if action == "list" else CloudAccountDeleteResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@cloud_account_name_space.route("/v1/<string:tenant_id>/cloud_accounts/<string:cloud_account_id>/rediscover")
class CloudAccountRediscover(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(CloudAccountRediscover))

    @api.doc(id="Re-discoverResources", name="Re-discoverResources",
             description="Initiate resource discovery of the cloud account.",
             security=['auth_user', 'auth_token'])
    @cloud_account_name_space.response(model=CloudAccountRediscoverResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, cloud_account_id):
        try:
            format_params = {
                'tenant_id': tenant_id
            }
            args = {"account_id": cloud_account_id}
            response = invoke_api(service_account_api_defn, 'rediscover', headers=request.headers,
                                  format_params=format_params, args=args)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountRediscoverResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
