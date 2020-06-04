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


def script_data_model_view(wild_card_model):
    return {
        'script_id': fields.String(required=True, description="Script Id", attribute='data.id'),
        'script_name': fields.String(required=True, description="Script Name", attribute='data.name'),
        'uri': fields.String(required=True, description="Unique URI for script", attribute='data.uri'),
        'description': fields.String(required=True, description="Description about script",
                                     attribute='data.description'),
        'status': fields.String(required=True, description="Status of the script", attribute='data.status'),
        'category': fields.List(fields.Raw, required=True, description="Script Category", attribute='data.category'),
        'platform': fields.List(fields.Raw, required=True, description="Platforms supported by script.",
                                attribute='data.platform'),
        'operating_systems': fields.List(fields.Raw, required=True, description="OS supported by script",
                                         attribute='data.operating_systems'),
        'type': fields.String(required=True, description="Config type of the script", attribute='data.config_type'),
        'scope': fields.String(required=True, description="Scope of the script", attribute='data.scope'),
        'path_type': fields.String(required=True, description="Script path type such as"
                                                              " git/url/repository(puppet_alone)/galaxy(ansible).",
                                   attribute='data.path_type'),
        'playbook_path': fields.String(required=True, description="Playbook path - available for ansible alone",
                                       attribute='data.playbook_path'),
        'playbook_name': fields.String(required=True, description="Playbook name - available for ansible alone",
                                       attribute='data.playbook_name'),
        'cookbook_path': fields.String(required=True, description="Cookbook path - available for chef alone.",
                                       attribute='data.playbook_path'),
        'cookbook_name': fields.String(required=True, description="Cookbook path - available for chef alone",
                                       attribute='data.cookbook_name'),
        'shell_script_path': fields.String(required=True, description="Shell script path - available for shell alone",
                                           attribute='data.shell_script_path'),
        'shell_script_name': fields.String(required=True, description="Shell script path - available for shell alone",
                                           attribute='data.shell_script_name'),
        'module_path': fields.String(required=True, description="Module path - available for puppet alone",
                                     attribute='data.module_path'),
        'module_name': fields.String(required=True, description="Module path - available for puppet alone.",
                                     attribute='data.module_name'),
        'parameters': fields.Nested(wild_card_model, required=True, description="Parameters of the script.",
                                    attribute='data.parameters'),
        'created_by': fields.String(required=True, description="Name of the user who created the script.",
                                    attribute='data.created_by'),
        'created_at': fields.String(required=True, description="Script creation time", attribute='data.created_at'),
        'updated_by': fields.String(required=True, description="Name of the user who updated the script. ", attribute='data.updated_by'),
        'updated_at': fields.String(required=True, description="Script updation time", attribute='data.updated_at'),
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
        'data': fields.Nested(script_data_model, required=True, description="Metadata Info.",
                              attribute='data.scripts',
                              skip_none=True),
    }


def script_delete_response():
    return {
        'message': fields.String(required=True, description="Response message.")
    }
