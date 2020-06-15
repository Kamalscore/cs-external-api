# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


from flask_restplus import fields


def list_user_data(roles_assignment_data):
    return {
        "user_id": fields.String(required=True, description="ID of the User. This is an auto generated and unique in "
                                                            "the CoreStack system", attribute="id"),
        "username": fields.String(required=True, description="Username is unique in the CoreStack system. User can use "
                                                             "this to login to CoreStack portal in addition to email",
                                  attribute="username"),
        "status": fields.String(required=True, description="Current Status of the user - active or inactive. Inactive"
                                                           " user cannot login or use AccessKeys",
                                attribute="status"),
        "email": fields.String(required=True, description="Email of the User. This is unique in the CoreStack system",
                               attribute="email"),
        "role_assignment": fields.Nested(roles_assignment_data, required=True,
                                         description="List of roles assignments or the user. The same user can be"
                                                     " assigned different roles in different tenants",
                                         attribute="roles"),
        "timezone_id": fields.String(required=True, description="Id of the Timezone such as Asia/Kolkata, Asia/Dubai "
                                                                "and so on",
                                     attribute="timezone")
    }


def list_role_assignment(roles_data):
    return {
        "tenant_name": fields.String(required=True, description="Name of the tenant within the CoreStack account",
                                     attribute="project_name"),
        "tenant_id": fields.String(required=True, description="ID of the tenant within the CoreStack account",
                                   attribute="project_id"),
        "roles": fields.Nested(roles_data, required=True, description="List of roles for this tenant. User can have"
                                                                      " multiple roles within a tenant",
                               attribute="roles")
    }


def list_roles():
    return {
        "name": fields.String(required=True, description="Name of the Role assigned to the user under a tenant",
                              attribute="name"),
        "id": fields.String(required=True, description="ID of the Role assigned to the user under a tenant",
                            attribute="id"),
    }


def list_user_response_model(list_user_data):
    return {
        "total_count": fields.Integer(required=True, description="Number of users in CoreStack account.",
                                      attribute="data.total_count"),
        "users": fields.Nested(list_user_data, required=True, description="List all users within a CoreStack account.",
                               attribute="data.users")
    }


def describe_user_response_model(roles_assignment_data):
    return {
        "user_id": fields.String(required=True,
                                 description="ID of the User. This is an auto generated and unique in the CoreStack "
                                             "system",
                                 attribute="data.id"),
        "username": fields.String(required=True,
                                  description="Username is unique in the CoreStack system. User can use this to login "
                                              "to CoreStack portal in addition to email",
                                  attribute="data.username"),
        "status": fields.String(required=True,
                                description="Current Status of the user - active or inactive. Inactive user "
                                            "cannot login or use AccessKeys.",
                                attribute="data.status"),
        "email": fields.String(required=True,
                               description="Email of the User. This is unique in the CoreStack system.",
                               attribute="data.email"),
        "first_name": fields.String(required=True,
                                    description="First Name of the user. It can be only alphanumeric.",
                                    attribute="data.first_name"),
        "last_name": fields.String(required=True,
                                   description="Last Name of the user. It can be only alphanumeric.",
                                   attribute="data.last_name"),
        "role_assignment": fields.Nested(roles_assignment_data, required=True,
                                         description="List of roles assignments for the user. The same user can be "
                                                     "assigned different roles in different tenants",
                                         attribute="data.roles"),
        "timezone_id": fields.String(required=True,
                                     description="ID of the Timezone such as Asia/Kolkata, Asia/Dubai and so on",
                                     attribute="data.timezone"),
        "created_by": fields.String(require=True,
                                    description="Name of the user/admin who created this user",
                                    attribute="data.created_by"),
        "created_at": fields.String(require=True,
                                    description="DateTime when the user was created",
                                    attribute="data.created_at"),
        "updated_by": fields.String(require=True,
                                    description="Name of the user/admin last updated this user",
                                    attribute="data.updated_by"),
        "updated_at": fields.String(require=True,
                                    description="DateTime when the user was last updated",
                                    attribute="data.updated_at"),
        "sso_userid": fields.String(require=True,
                                    description="User's Single Sign-on Id, if CoreStack is deployed using"
                                                " SingleSignOn (SSO) model",
                                    attribute="data.sso_userid"),
        "account_id": fields.String(require=True,
                                    description="ID of the Account in CoreStack. It will be available in the authToken"
                                                " API response",
                                    attribute="data.project_master_id"),
        "is_accesskey_available": fields.Boolean(require=True,
                                                 description="Is Access Key available for this user.",
                                                 attribute="data.require_access_key")
    }


def user_delete_response_model():
    return {
        "message": fields.String(require=True, description="Response message.", attribute="message")
    }


def user_create_request_model(add_role_assignment):
    return {
        "username": fields.String(required=True, description="The unique username for the user to be created. "
                                                             "This value is expected to be unique across all accounts. "
                                                             "Hence it is recommended that you use the email address as"
                                                             " the value here. Validations:- Min length - 5, "
                                                             "Alphanumeric"),
        "password": fields.String(required=True, description="Password length must be of 8-15 characters with at least "
                                                             "one special character(_$^@*!#&.), one number and starting"
                                                             " character must be an alphabet"),
        "email": fields.String(required=True, description="Email ID of the user. This wil be unique across all the"
                                                          " CoreStack accounts"),
        "timezone_id": fields.String(required=True,
                                     description="ID of the timezone to be set for th user. For a valid list of "
                                                 "timezone values to use, please refer "
                                                 "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"),
        "account_id": fields.String(required=True, description="ID of the Account in CoreStack. It will be available "
                                                               "in the authToken API response"),
        "first_name": fields.String(required=False, description="First Name of the user. It can be only alphanumeric"),
        "last_name": fields.String(required=False, description="Last Name of the user. It can be only alphanumeric"),
        "role_assignment": fields.List(fields.Nested(add_role_assignment), required=True,
                                       description="List of roles assignments for the user. The same user can be "
                                                   "assigned different roles in different tenants"),
        "is_accesskey_required": fields.Boolean(required=False, description="Is Access Key to be generated for this "
                                                                            "user",
                                                default=False)
    }


def add_role_assignment():
    return {
        "tenant_id": fields.String(required=True, description="ID of the tenant within the CoreStack account"),
        "role_names": fields.List(fields.String(required=True, description=""), required=True,
                                  description="Name of the Roles to be assigned to the user under a tenant")
    }


def update_role_assignment():
    return {
        "tenant_id": fields.String(required=False, description="ID of the tenant within the CoreStack account"),
        "role_names": fields.List(fields.String(required=False, description=""), required=False,
                                  description="Name of the Roles to be assigned to the user under a tenant")
    }


def user_create_response_model():
    return {
        "user_id": fields.String(required=True, description="ID of the newly created User", attribute="data.id")
    }


def user_update_request_model(add_role_assignment):
    return {
        "email": fields.String(required=True, description="Email ID of the user. This wil be unique across all the"
                                                          " CoreStack accounts"),
        "first_name": fields.String(required=False, description="First Name of the user. It can be only alphanumeric"),
        "last_name": fields.String(required=False, description="Last Name of the user. It can be only alphanumeric"),
        "timezone_id": fields.String(required=True,
                                     description="ID of the timezone to be set for th user. For a valid list of "
                                                 "timezone values to use, please refer "
                                                 "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"),
        "role_assignment": fields.List(fields.Nested(add_role_assignment), required=False,
                                       description="List of roles assignments for the user. The same user can be "
                                                   "assigned different roles in different tenants")
    }


def user_update_response_model():
    return {
        "user_id": fields.String(required=True, description="ID of the updated User", attribute="data.id")
    }


def change_password_request_model():
    return {
        "current_password": fields.String(required=True, description="Current password of the user being used. If you "
                                                                     "are unaware of the current password, use forgot "
                                                                     "password option in the CoreStack portal."),
        "new_password": fields.String(required=True, description="New Password to be set for the user. Password length"
                                                                 " must be of 8-15 characters with atleast one special"
                                                                 " character(_$^@*!#&.), one number and starting "
                                                                 "character must be an alphabet.")
    }


def change_password_response_model():
    return {
        "user_id": fields.String(required=True, description="ID of the User to whom the password is changed",
                                 attribute="data.id")
    }


def change_timezone_request_model():
    return {
        "current_timezone_id": fields.String(required=True, description="Current timezone set for the user. If you are "
                                                                        "unaware of the current timezone, use "
                                                                        "authToken or describeUser opertion to know the"
                                                                        " timezone id. Timezone ID can be Asia/Kolkata,"
                                                                        " Asia/Dubai and so on"),
        "new_timezone_id": fields.String(required=True,
                                         description="New timezone id to be set for the user. For a valid list of "
                                                     "timezone values to use, please refer"
                                                     " https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
    }


def change_timezone_data_model():
    return {
        "raw_offset": fields.String(required=True, description="Raw offset of the timezone. It means the amount of time"
                                                               " in milliseconds to add to UTC to get standard time in"
                                                               " the required time zone",
                                    attribute="raw_offset"),
        "id": fields.String(required=True, description="ID of the Timezone such as Asia/Kolkata, Asia/Dubai and so on",
                            attribute="id")
    }


def change_timezone_response_model(change_timezone_data_model):
    return {
        "timezone": fields.Nested(change_timezone_data_model, required=True,
                                  description="Contains information about the timezone set for the user. "
                                              "Raw offset of the timezone. It means the amount of time in milliseconds "
                                              "to add to UTC to get standard time in the required time zone. Id of the "
                                              "Timezone such as Asia/Kolkata, Asia/Dubai and so on",
                                  attribute="data.timezone"),
        "user_id": fields.String(required=True, description="ID of the user to whom the timezone is changed",
                                 attribute="data.user_id")
    }
