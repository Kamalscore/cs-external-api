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
                                       attribute='data.cookbook_path'),
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
        'updated_by': fields.String(required=True, description="Name of the user who updated the script. ",
                                    attribute='data.updated_by'),
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


def script_response_list(script_data_model):
    return {
        'scripts': fields.Nested(script_data_model,
                                 required=True, description="Metadata Info.",
                                 attribute='data.scripts',
                                 skip_none=True),
    }


def script_info_model():
    return {
        'path_type': fields.String(required=True, description="path_type"),
        'name': fields.String(required=True, description="Script Name"),
        'path': fields.String(required=True, description="Path of the script")
    }


def script_data_model_create(script_info_model, wild_card_model, minimum_requirements_model):
    return {
        'name': fields.String(required=True, description="Script Name"),
        'uri': fields.String(description="Unique URI for script"),
        'description': fields.String(description="Description about script"),
        'category': fields.List(fields.String, required=True, description="Script Category",
                                enum=["Application", "Languages", "Database", "Security", "System", "Web Server",
                                      "Others"]),
        'platform': fields.List(fields.String, required=True, description="Platforms supported by script.",
                                enum=["linux", "windows"]),
        'operating_system': fields.List(fields.String, required=True, description="OS supported by script",
                                        enum=['ubuntu', 'centos', 'fedora', 'redhat', 'windows']),
        'config_type': fields.String(required=True, description="Config type of the script"),
        'scope': fields.String(required=True, description="Scope of the script", enum=['private', 'account', 'tenant']),

        'script_info': fields.List(fields.Nested(script_info_model, required=True, description='script info')),
        'dependencies': fields.List(
            fields.Nested(script_info_model, description='Details of the dependent scripts if any')),
        'input_source': fields.String(description="Input source of the script during execution (Script/Resource)",
                                      default='Script'),
        'is_scanned': fields.String(description="Whether the script needs to be scanned or not", default=True),
        'scanned_parameters': fields.Nested(wild_card_model, description="Parameter object scanned by corestack"),
        'minimum_requirement': fields.Nested(minimum_requirements_model,
                                             description="Minimum requirements to install the script"),
        'playbook_yaml': fields.String(description="Playbook yaml path - mandatory for ansible scripts"),
        #                                attribute='data.playbook_path'),
        # 'cookbook_name': fields.String(required=True, description="Cookbook path - available for chef alone",
        #                                attribute='data.cookbook_name'),
        # 'shell_script_path': fields.String(required=True, description="Shell script path - available for shell alone",
        #                                    attribute='data.shell_script_path'),
        # 'shell_script_name': fields.String(required=True, description="Shell script path - available for shell alone",
        #                                    attribute='data.shell_script_name'),
        # 'module_path': fields.String(required=True, description="Module path - available for puppet alone",
        #                              attribute='data.module_path'),
        # 'module_name': fields.String(required=True, description="Module path - available for puppet alone.",
        #                              attribute='data.module_name'),
        'parameters': fields.Nested(wild_card_model, required=True, description="Parameters of the script."),
    }


def script_minimum_requirements_model():
    return {
        "ram(MB)": fields.Float(description="Minimum RAM required(in MB) to install the script.", default=0.0),
        "cpu": fields.Integer(description="Minimum CPU core required(in MB) to install the script.", default=0),
        "disk(MB)": fields.Float(description="Minimum disk space required(in MB) to install the script.", default=0.0),
    }


def script_create_update_response_model():
    return {
        'script_id': fields.String(description="Unique ID of the script", attribute='data.id')
    }


def script_execute_request(job_input_data_model):
    return {
        'job_name': fields.String(required=True, description="Name of the script job"),
        'job_details': fields.Nested(job_input_data_model,
                                     required=True, description="Execution input such as script/host details",
                                     skip_none=True),
    }


def script_execute_job_input_model(wild_card_model):
    return {
        "parameter_source": fields.String(description="Parameter source - whether as per the one defined in script "
                                                      "or custom json", default="script", enum=["script", "json"]),
        "parameters": fields.Nested(wild_card_model, required=True, description="Parameters of the script."),
        "script_name": fields.List(fields.String, required=True, description='script info'),
        "username": fields.String(required=True, description="Username of the target machine"),
        "platform": fields.String(required=True, description="OS platform of the target machine (linux/windows)"),
        "host": fields.String(required=True, description="Target machine's IP/DNS"),
        "password": fields.String(description="Password of the target machine's IP/DNS"),
        "keypair_flag": fields.String(required=True,
                                      description="Flag to indicate whether to connect using keypair or not"),
        "key_file": fields.String(required=True, description="Private key content if keypair_flag is true"),
        "port": fields.String(required=True, description="SSH/WinRM port")
    }


def script_execute_response_model():
    return {
        'script_job_id': fields.String(description="Unique ID of the Script Job", attribute='data.id')
    }


def script_delete_response():
    return {
        'message': fields.String(required=True, description="Response message.")
    }
