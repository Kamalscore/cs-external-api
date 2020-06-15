# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


from flask_restplus import fields


def role_list_data():
    return {
        "role_id": fields.String(required=True, description="ID of the Role. This is an auto generated and unique "
                                                            "in the CoreStack system", attribute="id"),
        "role_name": fields.String(required=True, description="Rolename is unique in the CoreStack system for a "
                                                              "specific tenant.", attribute="name"),
        "access": fields.List(fields.String(required=True, description="Access assigned to this specific role"),
                              required=True, description="List of access assigned to this specific role.",
                              attribute="access"),
        "category": fields.String(required=True, description="Category of the specific role.Either default or custom",
                                  attribute="category")
    }


def role_list_response(role_list_data):
    return {
        "total_count": fields.Integer(required=True, description="Total number of roles available in the specific "
                                                                 "tenant", attribute="data.total_count"),
        "roles": fields.Nested(role_list_data, required=True, description="List of roles available in specific tenant",
                               attribute="data.roles")
    }
