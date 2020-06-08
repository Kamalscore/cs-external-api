# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from flask_restplus import fields


def cloud_account_response_model_list(cloud_account_data):
    return {
        "total_count": fields.Integer(required=True, description="Number of CloudAccounts",
                                      attribute="data.total_count"),
        "page_count": fields.Integer(required=True, description="Number of Pages", attribute="data.page_count"),
        "cloud_accounts": fields.Nested(cloud_account_data, required=True, description="Metadata Info.",
                                        attribute="data.cloud_and_tool_accounts")
    }


def cloud_account_data_model_list():
    return {
        "cloud_account_name": fields.String(required=True, description="Name of the cloud account.", attribute="name"),
        "cloud_account_id": fields.String(required=True, description="ID of the cloud account.", attribute="id"),
        "status": fields.String(required=True, description="Cloud account status.", attribute="status"),
        "service": fields.String(required=True, description="Cloud Service.", attribute="service_name")
    }


def cloud_account_response_model_view(wildcard_model):
    return {
        "cloud_account_name": fields.String(required=True, description="Name of the cloud account.",
                                            attribute="data.name"),
        "cloud_account_id": fields.String(required=True, description="The unique identifier for a cloud account.",
                                          attribute="data.id"),
        "status": fields.String(required=True,
                                description="Indicates the status of the cloud account - active / inactive.",
                                attribute="data.status"),
        "service": fields.String(required=True, description="The name of the cloud service.for example, AWS.",
                                 attribute="data.service_name"),
        "service_id": fields.String(required=True, description="The unique identifier associated with the service.",
                                    attribute="data.service_id"),
        "description": fields.String(required=True, description="A brief description of the cloud account.",
                                     attribute="data.description"),
        "environment": fields.String(required=True, description="Cloud account environment.for example, Development",
                                     attribute="data.environment"),
        "scope": fields.String(required=True, description="Scope of the cloud account.for example, global",
                               attribute="data.scope"),
        "auth_values": fields.Nested(wildcard_model, required=True, description="Data that describes the authentication credentials.",
                                     attribute="data.auth_values"),
        "service_discovery": fields.String(required=True, description="Version of service discovery.",
                                           attribute="data.service_discovery"),
        "metadata": fields.Nested(wildcard_model, required=True,
                                  description="Data about tenant and regions of the cloud account, if applicable.",
                                  attribute="data.metadata"),
        "roles": fields.List(fields.Raw, required=True, description="List of role ID authorized to access the cloud account.",
                             attribute="data.roles"),
        "resource_catalog_allowed": fields.Boolean(required=True,
                                                   description="Flag to define the support of resource catalog.",
                                                   attribute="data.resource_catalog_allowed"),
        "resource_listing_support": fields.Boolean(required=True,
                                                   description="Flag to define the support of resource listing.",
                                                   attribute="data.resource_listing_support"),
        "delete_status": fields.String(required=True, description="Status of account deletion.",
                                       attribute="data.delete_status"),
        "created_by": fields.String(required=True, description="Name of the user who created the cloud account.",
                                    attribute="data.created_by"),
        "created_at": fields.String(required=True, description="Cloud account creation time.",
                                    attribute="data.created_at"),
        "updated_by": fields.String(required=True, description="Name of the user who updated the cloud account.",
                                    attribute="data.updated_by"),
        "updated_at": fields.String(required=True, description="Cloud account updation time.",
                                    attribute="data.updated_at")}


def aws_cloud_account_auth_values_model():
    return {
        "access_key": fields.String(required=True, description="Access Key of AWS account."),
        "secret_key": fields.String(required=True, description="Secret Key of AWS account."),
        "account_type": fields.String(required=True, description="Type of the account to be created.",
                                      enum=["master_account", "linked_account"]),
        "bucket_name": fields.String(required=False,
                                     description="Billing Bucket Name to process billing data.It is mandatory for the "
                                                 "account_type 'master_account'"),
        "master_account": fields.String(required=False,
                                        description="Cloud account ID of the existing Master Account in the system."
                                                    "It is required if the account_type is chosen as 'linked_account'")
    }


def cloud_account_request_model(cloud_account_auth_values_model):
    return {
        "name": fields.String(required=True, description="Unique name for the Cloud account to be created"),
        "description": fields.String(required=False, description="Description of the Cloud account to be created"),
        "scope": fields.String(required=True, description="Cloud Service",
                               enum=["global", "tenant", "private", "account"], default="global"),
        "environment": fields.String(required=True, description="Cloud Service",
                                     enum=["All", "Production", "Staging", "QA", "Development"], default="All"),
        "auth_values": fields.Nested(cloud_account_auth_values_model, required=True,
                                     description="Authentication credentials of Cloud account.")
    }


def azure_cloud_account_auth_values_model():
    return {
        "subscription_id": fields.String(required=True, description="Azure Subscription ID."),
        "application_id": fields.String(required=True, description="Azure Application ID."),
        "application_secret": fields.String(required=True, description="Azure Application Secret Key"),
        "subscription_type": fields.String(required=True,
                                           description="Subscription type of the account to be on-boarded.",
                                           enum=["Azure_CSP-Direct", "Pay_as_You_Go", "Enterprise"])
    }


def azure_cloud_account_request_model(azure_cloud_account_auth_values_model):
    return {
        "name": fields.String(required=True, description="Unique name for the Cloud account to be created"),
        "description": fields.String(required=False, description="Description of the Cloud account to be created"),
        "scope": fields.String(required=True, description="Cloud Service",
                               enum=["global", "tenant", "private", "account"], default="global"),
        "environment": fields.String(required=True, description="Cloud Service",
                                     enum=["All", "Production", "Staging", "QA", "Development"], default="All"),
        "auth_values": fields.Nested(azure_cloud_account_auth_values_model, required=True,
                                     description="Authentication credentials of Azure Cloud account.")
    }


def cloud_account_create_response_model():
    return {
        "cloud_account_id": fields.String(required=True, description="Cloud account ID", attribute="data.id")
    }


def wild_card_model():
    return {'*': fields.Wildcard(fields.Raw)}


def cloud_account_dependency_response_model(wild_card_model):
    return {"dependency": fields.Nested(wild_card_model, required=True, description="Dependency Info.",
                                        attribute="data.dependency"),
            "delete_status": fields.String(required=True, description="Delete Status", attribute="data.delete_status")
            }


def cloud_account_delete_response_model():
    return {
        "message": fields.String(required=True, description="Response message.")
    }


def cloud_account_rediscover_response():
    return {
        "message": fields.String(required=True, description="Response message.")
    }
