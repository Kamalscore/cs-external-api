# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'


from flask_restplus import fields


def script_metadata_model():
    return {
        'is_scanned': fields.String(required=False,
                                    description="Flag to indicate whether the script is scanned or not.")
    }


def script_data_model_list():
    return {
        'script_id': fields.String(required=True, description="Script Id", attribute='id'),
        'script_name': fields.String(required=True, description="Script Name", attribute='name'),
        'uri': fields.String(required=True, description="Unique URI for script"),
        'description': fields.String(required=True, description="Description about script"),
        'status': fields.String(required=True, description="Status of the script"),
        'category': fields.List(fields.Raw, required=True, description="Script Category"),
        'platform': fields.List(fields.Raw, required=True, description="Platforms supported by script."),
        'operating_systems': fields.List(fields.Raw, required=True, description="OS supported by script"),
        'type': fields.String(required=True, description="Config type of the script", attribute='config_type'),
        'scope': fields.String(required=True, description="Scope of the script.")
    }


def script_request(script_metadata_model):
    return {
        'name': fields.String(required=True, description="Script Name."),
        'description': fields.String(required=True, description="Tenant Description."),
        'metadata': fields.Nested(script_metadata_model, required=True, description="Metadata Info."),
        'config_type': fields.String(required=True, description="Config Type (chef/ansible/puppet/shell)"),
        'status': fields.Boolean(required=True, description="Script's status.."),
    }


def script_response(script_data_model):
    return {
        'message': fields.String(required=True, description="Response message."),
        'data': fields.Nested(script_data_model, required=True, description="Metadata Info.", attribute='data.scripts',
                              skip_none=True),
    }


def script_delete_response():
    return {
        'message': fields.String(required=True, description="Response message.")
    }
