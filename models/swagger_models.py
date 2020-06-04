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
            'message': fields.String(required=True, description="Response message."),
            'token': fields.Nested(tokenModel, required=True, description="Token.", attribute='data.token', skip_none=True),
            'user': fields.Nested(userModel, required=True, description="Token.", attribute='data.user', skip_none=True),
            'account_id': fields.String(required=True, description="Account Id.", attribute='data.user.project_master_id'),
            'auth_type': fields.String(required=True, description="Account Id.", attribute='data.auth_type'),
            'auth_method': fields.String(required=True, description="Account Id.", attribute='data.auth_method'),
            'require_access_key': fields.Boolean(required=True, description="Account Id.", attribute='data.require_access_key'),
            'is_account_admin': fields.Boolean(required=True, description="Account Id.", attribute='data.is_account_admin'),
            'tenants': fields.List(fields.Nested(tokenTenantModel), required=True, description="Tenants List.", attribute='data.projects')
            }


def auth_detailed_response(tokenModel, wildcardModel):
    return {
            'message': fields.String(required=True, description="Response message."),
            'token': fields.Nested(tokenModel, required=True, description="Token.", attribute='data.token'),
            'user': fields.Nested(wildcardModel, required=True, description="Token.", attribute='data.user'),
            'data': fields.Nested(wildcardModel, required=True, description="Complete Data."),
            'account_id': fields.String(required=True, description="Account Id.", attribute='data.user.project_master_id'),
            'auth_type': fields.String(required=True, description="Account Id.", attribute='data.auth_type'),
            'auth_method': fields.String(required=True, description="Account Id.", attribute='data.auth_method'),
            'require_access_key': fields.Boolean(required=True, description="Account Id.", attribute='data.require_access_key'),
            'is_account_admin': fields.Boolean(required=True, description="Account Id.", attribute='data.is_account_admin'),
            'tenants': fields.List(fields.Raw, required=True, description="Tenants List.", attribute='data.projects')
            }


def wild_card_model():
    return {'*': fields.Wildcard(fields.String)}


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
        'tenant_id': fields.String(required=True, description="Tenant Id.")
    }


def tenant_response(tenantDataModel):
    return {
            'message': fields.String(required=True, description="Response Message."),
            'tenants': fields.Nested(tenantDataModel, required=True, description="Metadata Info.", attribute='data.projects')
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
