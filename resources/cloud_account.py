# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging
from flask import request
from flask_restplus import marshal, Resource

from app import api
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION, CS_ENDPOINT_URL_DEFAULT_VALUE, \
    CS_ENDPOINT_URL_PROPERTY_NAME
from definitions.service_account_definitions import ServiceAccountUrlDefinitions
from models.service_account_models import aws_cloud_account_auth_values_model, cloud_account_request_model, \
    cloud_account_create_response_model, cloud_account_dependency_response_model, cloud_account_delete_response_model, \
    wild_card_model, azure_cloud_account_auth_values_model, cloud_account_response_model_list, \
    cloud_account_data_model_list, cloud_account_response_model_view, cloud_account_rediscover_response, \
    aws_cloud_account_assume_role_auth_values_model, aws_assume_role_model
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
AWSAssumeRoleValues = api.model('AWSAssumeRoleValues', aws_assume_role_model())
AWSCloudAccountAssumeRoleAuthValues = api.model('AWSCloudAccountAssumeRoleAuthValues',
                                                aws_cloud_account_assume_role_auth_values_model(AWSAssumeRoleValues))
AWSCloudAccountAssumeRoleCreateRequest = api.model('CloudAccountAssumeRoleCreateRequest',
                                                   cloud_account_request_model(AWSCloudAccountAssumeRoleAuthValues))
AWSCloudAccountAssumeRoleUpdateRequest = api.model('CloudAccountAssumeRoleUpdateRequest',
                                                   cloud_account_request_model(AWSCloudAccountAssumeRoleAuthValues))
CloudAccountCreateRequest = api.model('CloudAccountCreateRequest',
                                      cloud_account_request_model(AWSCloudAccountAuthValues), for_doc_alone=True)
AWSCloudAccountUpdateRequest = api.model('CloudAccountUpdateRequest',
                                         cloud_account_request_model(AWSCloudAccountAuthValues))
AzureCloudAccountAuthValues = api.model('AzureCloudAccountAuthValues',
                                        azure_cloud_account_auth_values_model())
CloudAccountCreateResponse = api.model('CloudAccountCreateResponse', cloud_account_create_response_model())
CloudAccountUpdateResponse = api.model('CloudAccountUpdateResponse', cloud_account_create_response_model())
CloudAccountDeleteResponse = api.model('CloudAccountDeleteResponse', cloud_account_delete_response_model())
CloudAccountDependencyResponse = api.model('CloudAccountDependencyResponse',
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
             description="Creates an AWS cloud account with access key authentication for a given tenant. In case of "
                         "cloud account creation with assume role authentication, you should make use of "
                         "'createCloudAccountAssumeRole' API method with appropriate request body. Please refer the "
                         "link to know about AWS access_key authentication - "
                         "https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html",
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api."},
             security=['auth_user', 'auth_token']
             )
    @api.expect(CloudAccountCreateRequest, validate=False)
    @cloud_account_name_space.response(model=CloudAccountCreateResponse, code=201, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            format_params = {
                'tenant_id': tenant_id
            }
            req_body = request.json
            # FIXME Currently supporting AWS cloud account
            service = "AWS"
            if not req_body:
                return marshal({"message": "Missing request payload."}, errorModel), 400
            req_body.update(service=service, service_type="Cloud", settings="none")
            auth_values = req_body.get("auth_values")
            # Service AWS
            if service == "AWS":
                auth_values.update(protocol="access_key")
                if auth_values.get("account_type") == "master_account" and not auth_values.get("bucket_name"):
                    return marshal({"message": "bucket_name is mandatory for account_type 'master_account'"},
                                   errorModel), 400
                if auth_values.get("account_type") == "linked_account" and not auth_values.get("master_account"):
                    return marshal({"message": "master_account is mandatory for account_type 'linked_account'"},
                                   errorModel), 400
            # Service Azure
            if service == "Azure":
                req_body.update(cloud_type="Azure_Global")
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'create', args=request.args, headers=request.headers,
                                  format_params=format_params, base_url=base_url, req_body=req_body)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountCreateResponse), 201
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e or e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="ListCloudAccounts", name="ListCloudAccounts",
             description='List all cloud accounts for a given tenant.',
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api."},
             security=['auth_user', 'auth_token']
             )
    @cloud_account_name_space.response(model=CloudAccountListResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            # FIXME Currently supporting only AWS cloud account
            args = {"service_type": "Cloud",
                    "services": "AWS"}
            format_params = {
                'tenant_id': tenant_id
            }
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'list', args=args, headers=request.headers,
                                  format_params=format_params, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountListResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@cloud_account_name_space.route("/v1/<string:tenant_id>/cloud_accounts/assume_role")
class CloudAccountResourceAssumeRole(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(CloudAccountResourceAssumeRole))

    @api.doc(id="CreateCloudAccountAssumeRole", name="CreateCloudAccountAssumeRole",
             description="Creates an AWS cloud account with assume role authentication for a given tenant. In case of "
                         "cloud account creation with access key authentication, you should make use of "
                         "'createCloudAccount' API method with appropriate request body. Please refer the link to know "
                         "about AWS assume_role authentication - "
                         "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html",
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api."},
             security=['auth_user', 'auth_token']
             )
    @api.expect(AWSCloudAccountAssumeRoleCreateRequest, validate=False)
    @cloud_account_name_space.response(model=CloudAccountCreateResponse, code=201, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            format_params = {
                'tenant_id': tenant_id
            }
            req_body = request.json
            # FIXME Currently supporting AWS cloud account
            service = "AWS"
            if not req_body:
                return marshal({"message": "Missing request payload."}, errorModel), 400
            req_body.update(service=service, service_type="Cloud", settings="none")
            auth_values = req_body.get("auth_values")
            # Service AWS
            if service == "AWS":
                assume_role_values = auth_values.pop("assume_role")
                auth_values.update(protocol="assume_role",
                                   assume_role_mfa_enabled=assume_role_values.get("mfa_enabled"),
                                   assume_role_arn=assume_role_values.get("role_arn"),
                                   assume_role_external_id=assume_role_values.get("external_id"))
                if auth_values.get("account_type") == "master_account" and not auth_values.get("bucket_name"):
                    return marshal({"message": "bucket_name is mandatory for account_type 'master_account'"},
                                   errorModel), 400
                if auth_values.get("account_type") == "linked_account" and not auth_values.get("master_account"):
                    return marshal({"message": "master_account is mandatory for account_type 'linked_account'"},
                                   errorModel), 400
            # Service Azure
            if service == "Azure":
                req_body.update(cloud_type="Azure_Global")
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'create', args=request.args, headers=request.headers,
                                  format_params=format_params, base_url=base_url, req_body=req_body)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountCreateResponse), 201
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e or e.__doc__, status="Internal Server Error", statusCode="500")


@cloud_account_name_space.route("/v1/<string:tenant_id>/cloud_accounts/<string:cloud_account_id>/assume_role")
class CloudAccountResourceAssumeRoleById(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(CloudAccountResourceAssumeRoleById))

    @api.doc(id="UpdateCloudAccountAssumeRole", name="UpdateCloudAccountAssumeRole",
             description="Updates the existing AWS cloud account created with assume_role authentication for a given "
                         "tenant. Since authentication protocol can also be updated with cloud_account edit, you should"
                         " make use of 'updateCloudAccount' API method to update the cloud_account with access_key "
                         "authentication with appropriate request body.",
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api.",
                     "cloud_account_id": "Specify the cloud account id to update, cloud account id is unique can be "
                                         "obtained from the list cloud account api."},
             security=['auth_user', 'auth_token']
             )
    @api.expect(AWSCloudAccountAssumeRoleUpdateRequest, validate=True)
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
            # FIXME Currently supporting only AWS cloud account
            service = "AWS"
            req_body = request.json
            if not req_body:
                return marshal({"message": "Missing request payload."}, errorModel), 400
            req_body.update(service=service, service_type="Cloud", settings="none")
            auth_values = req_body.get("auth_values")
            # Service AWS
            if service == "AWS":
                assume_role_values = auth_values.pop("assume_role")
                auth_values.update(protocol="assume_role",
                                   assume_role_mfa_enabled=assume_role_values.get("mfa_enabled"),
                                   assume_role_arn=assume_role_values.get("role_arn"),
                                   assume_role_external_id=assume_role_values.get("external_id"))
                if auth_values.get("account_type") == "master_account" and not auth_values.get("bucket_name"):
                    return marshal({"message": "bucket_name is mandatory for account_type 'master_account'"},
                                   errorModel), 400
                if auth_values.get("account_type") == "linked_account" and not auth_values.get("master_account"):
                    return marshal({"message": "master_account is mandatory for account_type 'linked_account'"},
                                   errorModel), 400
            # Service Azure
            if service == "Azure":
                req_body.update(cloud_type="Azure_Global")
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'update', args=request.args, headers=request.headers,
                                  format_params=format_params, base_url=base_url, req_body=req_body)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountUpdateResponse), 200
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
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api.",
                     "cloud_account_id": "Specify the cloud account id to update, cloud account id is unique can be "
                                         "obtained from the list cloud account api."},
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
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'view', headers=request.headers,
                                  format_params=format_params, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountDescribeResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="UpdateCloudAccount", name="UpdateCloudAccount",
             description="Update the existing AWS cloud account with access_key authentication for a given tenant. "
                         "Since authentication protocol can also be updated with cloud_account edit, you should make "
                         "use of 'updateCloudAccount/AssumeRole' API method to update the cloud_account with "
                         "assume_role authentication with appropriate request body.",
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api.",
                     "cloud_account_id": "Specify the cloud account id to update, cloud account id is unique can be "
                                         "obtained from the list cloud account api."},
             security=['auth_user', 'auth_token']
             )
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
            # FIXME Currently supporting only AWS cloud account
            service = "AWS"
            req_body = request.json
            if not req_body:
                return marshal({"message": "Missing request payload."}, errorModel), 400
            req_body.update(service=service, service_type="Cloud", settings="none")
            auth_values = req_body.get("auth_values")
            # Service AWS
            if service == "AWS":
                auth_values.update(protocol="access_key")
                if auth_values.get("account_type") == "master_account" and not auth_values.get("bucket_name"):
                    return marshal({"message": "bucket_name is mandatory for account_type 'master_account'"},
                                   errorModel), 400
                if auth_values.get("account_type") == "linked_account" and not auth_values.get("master_account"):
                    return marshal({"message": "master_account is mandatory for account_type 'linked_account'"},
                                   errorModel), 400
            # Service Azure
            if service == "Azure":
                req_body.update(cloud_type="Azure_Global")
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'update', args=request.args, headers=request.headers,
                                  format_params=format_params, base_url=base_url, req_body=req_body)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountUpdateResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")

    @api.doc(id="DeleteCloudAccount", name="DeleteCloudAccount",
             description="Delete a specific cloud account.In order to delete, CoreStack enforces you to list all the "
                         "transactional data(Refer: CheckDependency API) associated with this cloud account."
                         "This is done to ensure that you do not loose any data that is critical for your business "
                         "needs.",
             params={"tenant_id": "Specify the tenant id to create cloud account which is a unique id "
                                  "can be retrieved using the list tenant api.",
                     "cloud_account_id": "Specify the cloud account id to update, cloud account id is unique can be "
                                         "obtained from the list cloud account api."},
             security=['auth_user', 'auth_token'])
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
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'delete', headers=request.headers,
                                  format_params=format_params, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountDeleteResponse), 200
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
             description="Triggering Rediscover action will synch all the resources(Created/Deleted/Modified) of the "
                         "target Cloud account with CoreStack Inventory. Based on the number of resources available in "
                         "the Subscription and the number of regions managed through CoreStack, rediscovery might take "
                         "sometime couple of hours.",
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
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'rediscover', headers=request.headers,
                                  format_params=format_params, base_url=base_url, args=args)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountRediscoverResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@cloud_account_name_space.route("/v1/<string:tenant_id>/cloud_accounts/<string:cloud_account_id>/check_dependency")
class CloudAccountTransaction(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(CloudAccountTransaction))

    @api.doc(id="CheckDependency", name="CheckDependency",
             description="To get all the transactional data associated with the cloud account.",
             security=['auth_user', 'auth_token'])
    @cloud_account_name_space.response(model=CloudAccountDependencyResponse, code=200, description='Success')
    @cloud_account_name_space.response(model=errorModel, code=400, description='Bad Request')
    @cloud_account_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @cloud_account_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id, cloud_account_id):
        try:
            format_params = {
                'tenant_id': tenant_id,
                'service_account_id': cloud_account_id
            }
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(service_account_api_defn, 'list_dependency', headers=request.headers,
                                  format_params=format_params, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), CloudAccountDependencyResponse), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            cloud_account_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
