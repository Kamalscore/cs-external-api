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
        "cloud_account_name": fields.String(required=True, description="CloudAccount Name.", attribute="name"),
        "cloud_account_id": fields.String(required=True, description="CloudAccount ID.", attribute="id"),
        "cloud_account_status": fields.String(required=True, description="CloudAccount Status.", attribute="status"),
        "service": fields.String(required=True, description="Cloud Service.", attribute="service_name")
    }


def cloud_account_response_model_view():
    return {
        "cloud_account_name": fields.String(required=True, description="CloudAccount Name.", attribute="data.name"),
        "cloud_account_id": fields.String(required=True, description="CloudAccount ID.", attribute="data.id"),
        "cloud_account_status": fields.String(required=True, description="CloudAccount Status.",
                                              attribute="data.status"),
        "service": fields.String(required=True, description="Cloud Service.", attribute="data.service_name")
    }


def aws_cloud_account_auth_values_model():
    return {
        "access_key": fields.String(required=True, description="Access Key of AWS account."),
        "secret_key": fields.String(required=True, description="Secret Key of AWS account."),
        "account_type": fields.String(required=True, description="Type of the account to be created.",
                                      enum=["master_account", "linked_account"]),
        "bucket_name": fields.String(required=False,
                                     description="Billing Bucket Name to process billing data.It is mandatory for the account_type 'master_account'"),
        "master_account": fields.String(required=False,
                                        description="Cloud account ID of the existing Master Account in the system.It is required if the account_type is chosen as 'linked_account'")
    }


def aws_cloud_account_request_model(aws_cloud_account_auth_values_model):
    return {
        "name": fields.String(required=True, description="Unique name for the Cloud account to be created"),
        "description": fields.String(required=False, description="Description of the Cloud account to be created"),
        "scope": fields.String(required=True, description="Cloud Service",
                               enum=["global", "tenant", "private", "account"], default="global"),
        "environment": fields.String(required=True, description="Cloud Service",
                                     enum=["All", "Production", "Staging", "QA", "Development"], default="All"),
        "auth_values": fields.Nested(aws_cloud_account_auth_values_model, required=True,
                                     description="Authentication credentials of Azure Cloud account.")
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
