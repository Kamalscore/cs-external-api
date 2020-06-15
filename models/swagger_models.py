# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.
import enum

# from flask_restplus import fields
from config import custom_fields as fields


def auth_request():
    return {'access_key': fields.String(required=True,
                                        description="API Access Key. This can be retrieved from the <b>My Profile</b> page. "
                                                    "Also this will be sent over email when the keys are generated.",
                                        help="API Access Key cannot be blank."),

            'secret_key': fields.String(required=True,
                                        description="API Secret Key. This will be available in the email sent when "
                                                    "the keys are generated. If you have lost the secret key, "
                                                    "it cannot be retrieved. Request your admin to generate a new set "
                                                    "of keys, if lost.",
                                        help="API Secret Key cannot be blank.")
            }


def auth_response(tokenModel, tokenTenantModel, userModel):
    return {
        # 'message': fields.String(required=True, description="Response message."),
        'token': fields.Nested(tokenModel, required=True, description="This contains the atrributes access_token, "
                                                                      "expires_at & issued_at. access_token will be "
                                                                      "passed with X-Auth-Token header in all other "
                                                                      "APIs for authentication.",
                               attribute='data.token'),
        'user': fields.Nested(userModel, required=True, description="Contains information about the user associated "
                                                                    "with the Access Key / Secret Key.",
                              attribute='data.user'),
        'account_id': fields.String(required=True, description="Id of the Account in CoreStack. There can be "
                                                               "multiple tenats within an account, so account_id "
                                                               "will be required for performing account level "
                                                               "actions such as createTenant.",
                                    attribute='data.user.project_master_id'),
        # 'auth_type': fields.String(required=True, description="Account Id.", attribute='data.auth_type'),
        # 'auth_method': fields.String(required=True, description="Account Id.", attribute='data.auth_method'),
        # 'require_access_key': fields.Boolean(required=True, description="Account Id.", attribute='data.require_access_key'),
        'is_account_admin': fields.Boolean(required=True, description="Implies the user associated with Access "
                                                                      "Key / Secret Key is an account admin in "
                                                                      "CoreStack. True means account admin.",
                                           attribute='data.is_account_admin'),
        'tenants': fields.List(fields.Nested(tokenTenantModel), required=True, description="List of tenants "
                                                                                           "within the CoreStack "
                                                                                           "account. Each tenant "
                                                                                           "will have an id & "
                                                                                           "name that uniquely "
                                                                                           "identifies it.",
                               attribute='data.projects')
    }


def auth_detailed_response(tokenModel, userModel, wildcardModel):
    return {
        'auth_type': fields.String(required=True, description="Authentication type.", attribute='data.auth_type'),
        'require_access_key': fields.Boolean(required=True, description="Whether access key required.",
                                             attribute='data.require_access_key'),
        'alias_details': fields.Nested(wildcardModel, required=True, description="Alias details.",
                                       attribute='data.alias_details'),
        'workflow': fields.Nested(wildcardModel, required=True, description="Workflow details",
                                  attribute='data.workflow'),
        'account_id': fields.String(required=True, description="Account id.", attribute='data.user.project_master_id'),
        'is_account_admin': fields.Boolean(required=True, description="Whether account admin or not.",
                                           attribute='data.is_account_admin'),
        'header_logo': fields.String(required=True, description="Header logo.", attribute='data.user.header_logo'),
        'user': fields.Nested(userModel, required=True, description="Token.", attribute='data.user'),
        'auth_method': fields.String(required=True, description="Authentication method.", attribute='data.auth_method'),
        'tenants': fields.List(fields.Raw, required=True, description="Tenants list.", attribute='data.projects'),
        'audit': fields.Nested(wildcardModel, required=True, description="Audit details.", attribute='data.audit'),
        'cost_unit': fields.String(required=True, description="Constant unit.", attribute='data.cost_unit'),
        'is_full_access': fields.Boolean(required=True, description="Whether full access or not.",
                                         attribute='data.is_full_access'),
        'subscription_details': fields.Nested(wildcardModel, required=True, description="Subscription details.",
                                              attribute='data.subscription_details'),
        'payment': fields.List(fields.Raw, required=True, description="Payment list.", attribute='data.payment'),
        'is_product_admin': fields.Boolean(required=True, description="Whether Product admin or not.",
                                           attribute='data.is_product_admin'),
        'token': fields.Nested(tokenModel, required=True, description="Token.", attribute='data.token'),
        'cost_currency': fields.String(required=True, description="Cost currency.", attribute='data.cost_currency'),
        'footer_text': fields.String(required=True, description="Footer text.", attribute='data.footer_text')
    }


def auth_user_model(timezoneModel):
    return {
        'name': fields.String(required=True, description="Name of the user."),
        'id': fields.String(required=True, description="Id of the user. This will be used for performing user "
                                                       "level operations such as getUser, changePassword and so "
                                                       "on."),
        'email': fields.String(required=True, description="Email Id of the user. This wil be unique."),
        # 'active_tenant_id': fields.String(required=True, description="Active tenant id."),
        'timezone': fields.Nested(timezoneModel, required=True, description="Contains information about the "
                                                                            "timezone set for the user."),
    }


def user_timezone_model():
    return {
        'id': fields.String(required=True, description="Id of the Timezone such as Asia/Kolkata, Asia/Dubai and "
                                                       "so on."),
        'raw_offset': fields.String(required=True, description="Raw offset of the timezone. It means the amount "
                                                               "of time in milliseconds to add to UTC to get "
                                                               "standard time in the required time zone.")
    }


def wild_card_model():
    return {'*': fields.Wildcard(fields.Raw)}


def token():
    return {
        'issued_at': fields.String(required=True, description="DateTime in UTC when the token was issued."),
        'expires_at': fields.String(required=True, description="Token expiry datetime in UTC."),
        'access_token': fields.String(required=True, description="This will be used as X-Auth-Token in all other "
                                                                 "APIs.", attribute='key')
        # 'refresh_token': fields.String(required=True, description="Refresh Token.")
    }


def error():
    return {
        'message': fields.String(required=True, description="Error response message.")
    }


def tenant_request(tenantMetadataModel):
    return {
        'name': fields.String(required=True, description='Name of the new tenant to be created. Tenant Name must '
                                                         'be globally unique within CoreStack. If the same tenant '
                                                         'name is used in another account, creation wil fail. '
                                                         'Tenant Name must start with alphabet and can contain '
                                                         '2-50 characters. Special characters \' " # ? / \ are '
                                                         'not allowed.'),
        'description': fields.String(required=True, description="Description of the new tenant to be created."),
        'metadata': fields.Nested(tenantMetadataModel, description="metadata is a freeform JSON. "
                                                                                  "It allows to store custom keys "
                                                                                  "and values. It will be useful "
                                                                                  "for storing information about "
                                                                                  "an external applications that "
                                                                                  "will refer to CoreStack "
                                                                                  "tenant."),
        'account_id': fields.String(required=True, description="Id of the CoreStack account under which the new "
                                                               "tenant to be created."),
        # 'status': fields.Boolean(required=True, description="To be removed from the wrapper and passed as true to the internal API."),
    }


class EnumStatus(enum.Enum):
    active = 'active'
    suspended = 'suspended'


def tenant_update_request(tenantMetadataModel):
    return {
        'description': fields.String(required=False, description="Description of the the tenant."),
        'metadata': fields.Nested(tenantMetadataModel, required=False,
                                  description="metadata is freeform JSON. It allows to store custom keys and values. It will be useful for storing information about an external applications that will refer to CoreStack tenant."),
        'account_id': fields.String(required=True,
                                    description="Id of the CoreStack account under which the tenant to be updated."),
        'status': fields.String(required=False, description="Status of the tenant can be active or suspended. When "
                                                            "suspended no operations can be performed within that "
                                                            "tenant.", enum=["active", "suspended"]),
    }


def tenant_metadata_model():
    return {
        'message': fields.String(required=True, description="Error response message.")
    }


def auth_tenant_model():
    return {
        'id': fields.String(required=True, description="Id of the tenant. This will be used for performing tenant "
                                                       "level operations such as createPolicy, createScript, "
                                                       "onboardCloudAccount and so on."),
        'name': fields.String(required=True, description="Unique name of the tenant provided as input when "
                                                         "creating.")
    }


def tenant_data_model():
    return {
        'account_id': fields.String(required=True, description="Tenant Id.", attribute='project_master_id'),
        '*': fields.Wildcard(fields.String)
    }


def tenant_response(tenantDataModel):
    return {
        # 'message': fields.String(required=True, description="Response Message."),
        'tenants': fields.Nested(tenantDataModel, required=True, description="Tenants List.",
                                 attribute='data.projects')
    }


def list_tenant(id_attribute='project_master_id'):
    return {
        'tenant_id': fields.String(required=True, description="Id of the tenant. This will be used for performing "
                                                              "tenant level operations such as createPolicy, "
                                                              "createScript, onboardCloudAccount and so on.",
                                   attribute='id'),
        'name': fields.String(required=True, description="Unique name of the tenant provided as input while "
                                                         "creating."),
        'description': fields.String(required=True, description="Description of the tenant."),
        'account_id': fields.String(required=True, description="Id of the CoreStack account under which this tenant "
                                                               "resides.",
                                    attribute=id_attribute, output_key='account_id'),

        'status': fields.String(required=True, description="Status of the tenant can be active or suspended. When "
                                                           "suspended no operations can be performed within that "
                                                           "tenant."),
        'created_at': fields.String(required=True, description="Created DateTime in UTC of the tenant.")
    }


def get_tenant_model(metadataModel):
    return {
        'metadata': fields.Nested(metadataModel, required=True,
                                  description="metadata is a freeform JSON. It allows to store "
                                              "custom keys and values. It will be useful for "
                                              "storing information about an external applications "
                                              "that will refer to CoreStack tenant"),
        'created_by': fields.String(required=True, description="Name of the user created this tenant."),
        'updated_by': fields.String(required=True, description="Name of the user last updated this tenant."),
        'updated_at': fields.String(required=True, description="DateTime in UTC when the tenant was last updated."),

        'account_name': fields.String(required=True, description="Name of the CoreStack account under which this "
                                                                 "tenant resides.", attribute='project_master_name')
    }


def tenant_create_response():
    return {
        # 'message': fields.String(required=True, description="Response Message."),
        'tenant_id': fields.String(required=True, description="Id of the newly created tenant. This will be used for "
                                                              "performing tenant level operations such as "
                                                              "createPolicy, createScript, onboardCloudAccount and so "
                                                              "on.", attribute='data.id')
    }


def tenant_update_response():
    return {
        'tenant_id': fields.String(required=True,
                                   description="Id of the updated tenant. This Id will be used for performing tenant "
                                               "level operations such as createPolicy, createScript, "
                                               "onboardCloudAccount and so on.",
                                   attribute='data.project_id')
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


def refresh_auth_token_request():
    return {
        "access_token": fields.String(required=True, description="access token obtained from the auth token api")

    }


def refresh_auth_token_response():
    return {
        "access_token": fields.String(required=True, description="access token obtained from the auth token api",
                                      attribute='token'),
        "issued_at": fields.String(required=True, description="Time in UTC at which the token was issued  at",
                                   attribute='issued_at'),
        "expires_at": fields.String(required=True, description="Time in UTC till which the token will be valid till",
                                    attribute='issued_at'),
        "refresh_count": fields.String(required=True, description="The count of refresh token used.It can be used"
                                                                  "for 3 max refresh count after which the token will"
                                                                  "expired.", attribute='refresh_count')
    }
