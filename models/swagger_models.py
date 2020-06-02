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


def auth_response(tokenModel):
    return {
            'message': fields.String(required=True, description="Response message."),
            'token': fields.Nested(tokenModel, required=True, description="Token."),
            'account_id': fields.String(required=True, description="Account Id."),
            'tenant_id': fields.String(required=True, description="Tenant Id."),
            'tenants': fields.List(fields.String, required=True, description="Tenants List.")
            }


def token():
    return {
            'issued_at': fields.String(required=True, description="Issued At Date."),
            'expires_at': fields.String(required=True, description="Expires At Date."),
            'access_token': fields.String(required=True, description="Access Token."),
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


def tenant_data_model():
    return {
            'tenant_id': fields.String(required=True, description="Tenant Id.")
            }


def tenant_response(tenantDataModel):
    return {
            'message': fields.String(required=True, description="Response Message."),
            'data': fields.Nested(tenantDataModel, required=True, description="Metadata Info."),
            }


def tenant_delete_response():
    return {
            'message': fields.String(required=True, description="Response message.")
            }