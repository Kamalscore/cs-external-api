# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.
from flask_restplus import fields


def auth_request():
    return {'access_key': fields.String(required=True,
                                  description="API Access Key. This will be available in the ""My Profile""page. If "
                                              "not, you can request your admin for one.",
                                  help="API Access Key cannot be blank."),

            'secret_key': fields.String(required=True,
                                        description="API Secret Key. This will be provided the first time when the "
                                                    "API access key is generated. Request your admin for a new key if "
                                                    "the secret key is lost.",
                                        help="API Secret Key cannot be blank.")
            }


def auth_response(tokenModel, tokenTenantModel, userModel):
    return {
            # 'message': fields.String(required=True, description="Response message."),
            'token': fields.Nested(tokenModel, required=True, description="Token.", attribute='data.token'),
            'user': fields.Nested(userModel, required=True, description="Token.", attribute='data.user'),
            'account_id': fields.String(required=True, description="Account Id.", attribute='data.user.project_master_id'),
            'auth_type': fields.String(required=True, description="Account Id.", attribute='data.auth_type'),
            'auth_method': fields.String(required=True, description="Account Id.", attribute='data.auth_method'),
            'require_access_key': fields.Boolean(required=True, description="Account Id.", attribute='data.require_access_key'),
            'is_account_admin': fields.Boolean(required=True, description="Account Id.", attribute='data.is_account_admin'),
            'tenants': fields.List(fields.Nested(tokenTenantModel), required=True, description="Tenants List.", attribute='data.projects')
            }


def auth_detailed_response(tokenModel, userModel, wildcardModel):
    return {
            'auth_type': fields.String(required=True, description="Authentication type.", attribute='data.auth_type'),
            'require_access_key': fields.Boolean(required=True, description="Whether access key required.", attribute='data.require_access_key'),
            'alias_details': fields.Nested(wildcardModel, required=True, description="Alias details.", attribute='data.alias_details'),
            'workflow': fields.Nested(wildcardModel, required=True, description="Workflow details", attribute='data.workflow'),
            'account_id': fields.String(required=True, description="Account id.", attribute='data.user.project_master_id'),
            'is_account_admin': fields.Boolean(required=True, description="Whether account admin or not.", attribute='data.is_account_admin'),
            'header_logo': fields.String(required=True, description="Header logo.", attribute='data.user.header_logo'),
            'user': fields.Nested(userModel, required=True, description="Token.", attribute='data.user'),
            'auth_method': fields.String(required=True, description="Authentication method.", attribute='data.auth_method'),
            'tenants': fields.List(fields.Raw, required=True, description="Tenants list.", attribute='data.projects'),
            'audit': fields.Nested(wildcardModel, required=True, description="Audit details.", attribute='data.audit'),
            'cost_unit': fields.String(required=True, description="Constant unit.", attribute='data.cost_unit'),
            'is_full_access': fields.Boolean(required=True, description="Whether full access or not.", attribute='data.is_full_access'),
            'subscription_details': fields.Nested(wildcardModel, required=True, description="Subscription details.", attribute='data.subscription_details'),
            'payment': fields.List(fields.Raw, required=True, description="Payment list.", attribute='data.payment'),
            'is_product_admin': fields.Boolean(required=True, description="Whether Product admin or not.", attribute='data.is_product_admin'),
            'token': fields.Nested(tokenModel, required=True, description="Token.", attribute='data.token'),
            'cost_currency': fields.String(required=True, description="Cost currency.", attribute='data.cost_currency'),
            'footer_text': fields.String(required=True, description="Footer text.", attribute='data.footer_text')
        }


def auth_user_model(wildcardModel):
    return {
            'name': fields.String(required=True, description="User name."),
            'id': fields.String(required=True, description="User id."),
            'email': fields.String(required=True, description="User email."),
            'active_tenant_id': fields.String(required=True, description="Active tenant id."),
            'timezone': fields.Nested(wildcardModel, required=True, description="Timezone id."),
            }


def wild_card_model():
    return {'*': fields.Wildcard(fields.Raw)}


def token():
    return {
            'issued_at': fields.String(required=True, description="Issued At Date."),
            'expires_at': fields.String(required=True, description="Expires At Date."),
            'access_token': fields.String(required=True, description="Access Token.", attribute='key'),
            'refresh_token': fields.String(required=True, description="Refresh Token.")
            }


def error():
    return {
            'message': fields.String(required=True, description="Error response message.")
            }


def tenant_request(tenantMetadataModel):
    return {
            'name': fields.String(required=True, description="Tenant Name."),
            'description': fields.String(required=True, description="Tenant Description."),
            'metadata': fields.Nested(tenantMetadataModel, required=True, description="Metadata Info."),
            'account_id': fields.String(required=True, description="Account Id."),
            'status': fields.Boolean(required=True, description="Tenant's status.."),
            }


def tenant_update_request(tenantMetadataModel):
    return {
            'description': fields.String(required=False, description="Tenant Description."),
            'metadata': fields.Nested(tenantMetadataModel, required=False, description="Metadata Info."),
            'account_id': fields.String(required=True, description="Account Id."),
            'status': fields.Boolean(required=False, description="Tenant's status.."),
            }


def tenant_metadata_model():
    return {
            'message': fields.String(required=True, description="Error response message.")
            }


def auth_tenant_model():
    return {
            'id': fields.String(required=True, description="Tenant id."),
            'name': fields.String(required=True, description="Tenant name.")
            }


def tenant_data_model():
    return {
            'account_id': fields.String(required=True, description="Tenant Id.", attribute='project_master_id'),
            '*': fields.Wildcard(fields.String)
            }


def tenant_response(tenantDataModel):
    return {
            'message': fields.String(required=True, description="Response Message."),
            'tenants': fields.Nested(tenantDataModel, required=True, description="Metadata Info.", attribute='data.projects')
            }


def tenant_create_response():
    return {
            'message': fields.String(required=True, description="Response Message."),
            'id': fields.String(required=True, description="Tenant id.", attribute='data.id')
            }


def tenant_update_response():
    return {
            'id': fields.String(required=True, description="Tenant id.", attribute='data.project_id')
            }


def tenant_delete_response():
    return {
            'message': fields.String(required=True, description="Response message.")
            }


def service_acc_data_model():
    return {
            'total_count': fields.Integer(required=True, description="Total Count.")
            }


def service_acc_response(serviceAccDataModel):
    return {
            'message': fields.String(required=True, description="Response message."),
            # 'token': fields.Nested(tokenModel, required=True, description="Token."),
            'data': fields.Nested(serviceAccDataModel, required=True, description="Metadata Info."),
            }
