# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

from flask_restplus import fields


def script_data_model_list():
    return {
        'script_id': fields.String(required=True, description="Unique Id of the script", attribute='id'),
        'script_name': fields.String(required=True, description="Name of the script", attribute='name'),
        'uri': fields.String(required=True, description="Unique URI for script"),
        'description': fields.String(required=True, description="Description about script"),
        'status': fields.String(required=True, description="Status of the script"),
        'category': fields.List(fields.String, required=True, description="Category of the script",
                                enum=["Application", "Languages", "Database", "Security", "System", "Web Server",
                                      "Others"]),
        'platform': fields.List(fields.String, required=True, description="Platforms supported by script."),
        'operating_system': fields.List(fields.String, required=True, description="OS supported by script"),
        'type': fields.String(required=True, description="Config type of the script", attribute='config_type'),
        'scope': fields.String(required=True, description="Scope of the script (global/account/tenant/private)")
    }


def script_data_model_view():
    return {
        'script_id': fields.String(required=True, description="Unique Id of the script", attribute='data.id'),
        'script_name': fields.String(required=True, description="Name of the script", attribute='data.name'),
        'uri': fields.String(required=True, description="Unique URI for script", attribute='data.uri'),
        'description': fields.String(required=True, description="Description about script",
                                     attribute='data.description'),
        'status': fields.String(required=True, description="Status of the script(active/inactive)."
                                                           " Only active scripts can be executed",
                                attribute='data.status'),
        'category': fields.List(
            fields.Raw(enum=["Application", "Languages", "Database", "Security", "System", "Web Server",
                             "Others"]), required=True, description="Category the script belongs to the script",
            attribute='data.category'),
        'platform': fields.List(fields.Raw, required=True, description="Platforms supported by script.",
                                attribute='data.platform', enum=["linux", "windows"]),
        'operating_system': fields.List(fields.Raw, required=True, description="OS supported by script",
                                        attribute='data.operating_systems'),
        'type': fields.String(required=True, description="Config type of the script (chef/ansible/shell/puppet)",
                              attribute='data.config_type'),
        'scope': fields.String(required=True, description="Scope of the script  (global/account/tenant/private)",
                               attribute='data.scope'),
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
        'parameters': fields.Raw(required=True,
                                 description="A JSON object which contains the parameters of the script.",
                                 attribute='data.parameters'),
        'created_by': fields.String(required=True, description="Name of the user who created the script.",
                                    attribute='data.created_by'),
        'created_at': fields.String(required=True, description="Script creation time in UTC",
                                    attribute='data.created_at'),
        'updated_by': fields.String(required=True, description="Name of the user who updated the script. ",
                                    attribute='data.updated_by'),
        'updated_at': fields.String(required=True, description="Script updation time in UTC",
                                    attribute='data.updated_at'),
    }


def script_response_list(script_data_model):
    return {
        'total_scripts': fields.String(required=True, description="Total number of scripts available",
                                       attribute='data.total_count'),
        'total_pages': fields.String(required=True, description="Total number of pages",
                                     attribute='data.page_count'),
        'scripts': fields.Nested(script_data_model,
                                 required=True,
                                 description="Scripts List.",
                                 attribute='data.scripts',
                                 skip_none=True)
    }


def script_info_model():
    return {
        'name': fields.String(required=True, description="Script Name as available in the path"),
        'path_type': fields.String(required=True,
                                   description="Path type"
                                               "Corestack currently supports "
                                               "git/url/repository(puppet_alone)/galaxy(ansible)."),
        'path': fields.String(required=True,
                              description="Path of the script. Examples"
                                          "For git path_type: https://github.com/ansible/test-playbooks.git,"
                                          "For url path_type: https://s3.amazonaws.com/ansible/test-playbooks.tar,"
                                          "For galaxy: https://galaxy.ansible.com/community/zabbix.")
    }


def script_data_model_scan(script_info_model):
    return {
        'config_type': fields.String(required=True, description="Config type of the script",
                                     enum=['chef', 'ansible', 'puppet', 'shell']),
        'script_info': fields.List(fields.Nested(script_info_model, required=True, description='script info')),
        'dependencies': fields.List(
            fields.Nested(script_info_model, required=False, description='Details of the dependent scripts if any')),
        'playbook_yaml': fields.String(description="Playbook yaml path - mandatory for ansible scripts")
    }


def script_data_model_create(script_info_model, minimum_requirements_model):
    return {
        'name': fields.String(required=True, description="Name of the script and it should be unique."),
        'uri': fields.String(description="Unique URI for script - eg: script/ansi/linux/lamp_install. "
                                         "If not provided, corestack will generate it automatically"),
        'description': fields.String(description="Detailed description about script"),
        'category': fields.List(
            fields.String(enum=["Application", "Languages", "Database", "Security", "System", "Web Server",
                                "Others"]), required=True, description="Script Category"),
        'platform': fields.List(fields.String(enum=["linux", "windows"]), required=True,
                                description="Platforms supported by script."),
        'operating_system': fields.List(fields.String(enum=["centos",
                                                            "ubuntu",
                                                            "Win-2008(Server)",
                                                            "Win-2012(Server)",
                                                            "redhat",
                                                            "fedora",
                                                            "debian",
                                                            "Win-2016(Server)",
                                                            "Win-7(Desktop)",
                                                            "Win-8(Desktop)"
                                                            ]),
                                        required=True, description="OS supported by script"),
        'config_type': fields.String(required=True, description="Config type of the script. "
                                                                "Create is supported for ansible type scripts alone for now",
                                     enum=['ansible']),
        'scope': fields.String(required=True, description="Scope of the script. "
                                                          'Account - Only Account admins can create/update/delete. '
                                                          'Tenant - Only Tenant admins can create/update/delete. '
                                                          'Private - All Users can create/update/delete.',
                               enum=['private', 'account', 'tenant']),

        'script_info': fields.List(fields.Nested(script_info_model, required=True, description='script info')),
        'dependencies': fields.List(
            fields.Nested(script_info_model,
                          description='Details of the dependent scripts if any. '
                                      'For eg., A LAMP script will have apache, mysql, php as dependent scripts.'
                                      'This can be skipped if there are no dependent scripts or'
                                      ' if the actual script takes care of installing all dependencies')),
        'minimum_requirement': fields.Nested(minimum_requirements_model,
                                             description="Minimum requirements of the target machine to install the script"),
        'playbook_yaml': fields.String(description="Playbook yaml path - mandatory for ansible scripts")
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
        'host_details': fields.List(fields.Nested(job_input_data_model,
                                                  required=True,
                                                  description="Execution input such as script/host details",
                                                  skip_none=True)),
        "config_type": fields.String(description='Config type of the script(s)')
    }


def script_execute_job_input_model():
    return {
        "host": fields.String(required=True, description="Target machine's IP/DNS"),
        "username": fields.String(required=True, description="Username of the target machine"),
        "password": fields.String(description="Password of the target machine's IP/DNS"),
        "keypair_flag": fields.String(required=True,
                                      description="Flag to indicate whether to connect using keypair or not"),
        "key_file": fields.String(required=True, description="Private key content if keypair_flag is true"),
        "port": fields.String(required=True, description="SSH/WinRM port"),
        "platform": fields.String(required=True, description="OS platform of the target machine (linux/windows)",
                                  enum=["linux", "windows"]),
        "script_name": fields.List(fields.String, required=True, description='Name of the scripts to execute. '
                                                                             'This can be fetched from '
                                                                             'listScripts/describeScript API'),
        "playbook_hosts": fields.List(fields.String, required=True,
                                      description='Required only for ansible scripts. '
                                                  'Name of the hostgroup to be referred as per playbook. '
                                                  'For eg, if you are installing a 3 tier app, you might have hostgroup '
                                                  'such as dbserver, appserver, uiserver of the scripts to execute and '
                                                  'the playbook tasks will be based on the hostgroups. '
                                                  'The hostgroup initialized in a playbook can be fetched from '
                                                  'scanScript API'),
        "parameters": fields.Raw(required=True,
                                 description="A JSON object which contains the parameters of the script. "
                                             "Refer scanned_parameters from scanScript/viewScript API response "
                                             "to view parameter available."
                                             " Parameter JSON should be as follows."
                                             "{\"<script_name_as_available_in_path>\": "
                                             "{\"parameter_key\" : \"parameter_value\"},"
                                             "\"<dependent_script_name_as_available_in_path>\": "
                                             "{\"parameter_key\" : \"parameter_value\"}}. \n"
                                             "For Eg.{\"ansible_lamp\": {\"mysql_port\" : \"3307\"}}",
                                 example={"ansible_lamp": {"mysql_port" : "3307"}}),
        "parameter_source": fields.String(description="Parameter source - whether as per the one defined in script "
                                                      "or custom json", default="script", enum=["script", "json"]),
    }


def script_execute_response_model():
    return {
        'script_job_id': fields.String(description="Unique ID of the Script Job. Use this ID in describeScriptJob API "
                                                   "and check the execution status", attribute='data.job_id')
    }


def script_scan_response_model():
    return {
        "scanned_parameters": fields.Raw(required=True,
                                         description=" A JSON object which contains the scanned parameters "
                                                     "of the script.", attribute='data'),
        "hosts": fields.List(fields.String, required=True, description='Hosts available in the playbook if any',
                             skip_none=True)
    }


def script_delete_response():
    return {
        'message': fields.String(required=True, description="Delete Response message.")
    }
