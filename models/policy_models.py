# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from flask_restplus import fields


def policy_create_model():
    return {
        "name": fields.String(required=True, description="policy name"),
        "description": fields.String(required=True, description="A brief explanation of the policy."),
        "type": fields.List(fields.String, required=False, description="Indicates the type of policy"),
        "category": fields.String(required=True, description="The category will be either service or resource"),
        "content": fields.String(required=True, description="The policy content"),
        "is_system_policy": fields.Boolean(),
        "engine_type": fields.String(required=True,
                                     description="Engine type of policy, mandatory if content type is git.", default="",
                                     enum=["azure_policy", "aws_config", "chef_inspec", "congress", ]),
        "services": fields.List(fields.String, required=True, description="Displays the service associated with the\
        policy, for example, AWS, AzureRM, Openstack., etc,"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of the\
        activity they perform, for example provisioning, Account Management, 	Utilization, etc. This value is\
        displayed in this field"),
        "sub_classification": fields.String(required=True, description="Sub classification for policy"),
        "scope": fields.String(required=True,
                               description="The scope of the policy (accout, tenant or private)",
                               enum=["account", "tenant", "private"]),
        "content_type": fields.String(required=True, description="Policy content source (git, file)", default="",
                                      enum=["git", "file"]),
        "content_password_or_key": fields.String(
            required=False, description="Password or private key to access of Git repo if repo is authenticated"),
        "content_username": fields.String(required=False, description="Username of Git repo if repo is authenticated"),
        "content_url": fields.String(required=False, description="Git project URL when the content type is git"),
        "content_path": fields.String(required=False, description="Root path of the policy in git repo"),
        "severity": fields.String(required=True
                                  , description="Severity of policy", default="", enum=["low", "medium", "high"])
    }


def policy_update_model(policy_meta_data):
    return {
        "name": fields.String(required=True, description="policy name"),
        "description": fields.String(required=False, description="A brief explanation of the policy."),
        "type": fields.List(fields.String, required=False, description="Indicates the type of policy"),
        "category": fields.String(required=True, description="The category will be either service or resource"),
        "content": fields.String(required=True, description="The policy content"),
        "is_system_policy": fields.Boolean(),
        "metadata": fields.Nested(policy_meta_data, required=False, description="Metadata about policy"),
        "engine_type": fields.String(required=False,
                                     description="Engine type of policy, mandatory if content type is git.", default="",
                                     enum=["azure_policy", "aws_config", "congress", "chef_inspec"]),
        "services": fields.List(fields.String, required=True, description="Displays the service associated with the\
           policy, for example, AWS, AzureRM, Openstack., etc,"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of the\
           activity they perform, for example provisioning, Account Management, 	Utilization, etc. This value is\
           displayed in this field"),
        "sub_classification": fields.String(required=True, description="Sub classification for policy"),
        "scope": fields.String(required=True,
                               description="The scope of the policy (global, accout, tenant or private)",
                               enum=["account", "tenant", "private"]),
        "content_type": fields.String(required=False, description="Policy content source (git, file)", default="",
                                      enum=["git", "file"]),
        "content_password_or_key": fields.String(
            required=False, description="Password or private key to access of Git repo if repo is authenticated"),
        "content_username": fields.String(required=False, description="Username of Git repo if repo is authenticated"),
        "content_url": fields.String(required=False, description="Git project URL when the content type is git"),
        "content_path": fields.String(required=False, description="Root path of the policy in git repo"),
        "severity": fields.String(required=False
                                  , description="Severity of policy", default="", enum=["low", "medium", "high"])
    }


def policy_view_response():
    return {
        "policy_id": fields.String(required=True, description="The unique identifier created for each policy.",
                                   attribute="data.policies.id"),
        "policy_name": fields.String(required=True, description="The name of the policy.",
                                     attribute="data.policies.name"),
        "description": fields.String(required=True, description="A brief explanation of the policy.",
                                     attribute="data.policies.description"),
        "status": fields.String(required=True, description="Indicates whether the policy is active or inactive.",
                                attribute="data.policies.status"),
        "category": fields.String(required=True, description="The category will be either service or resource.",
                                  attribute="data.policies.category"),
        "engine_type": fields.String(required=True, description="Engine type of policy",
                                     attribute="data.policies.engine_type"),
        "services": fields.List(fields.String, required=True, description="Displays the service associated with the "
                                                                          "policy for example, AWS, AzureRM, "
                                                                          "Openstack., etc",
                                attribute="data.policies.services"),
        "scope": fields.String(required=True, description="The scope of the policy.",
                               attribute="data.policies.scope", enum=["global", "account", "tenant", "private"]),
        "content_type": fields.String(required=True, description="Content type of policy (Git or File)",
                                      attribute="data.policies.content_type"),
        "content": fields.String(required=True, description="The policy content.", attribute="data.policies.content"),
        "git_content_url": fields.String(required=True, description="Git project URL when the content type is git.",
                                         attribute="data.policies.content_url"),
        "git_content_username": fields.String(required=True,
                                              description="Username of Git repo if repo is authenticated",
                                              attribute="data.policies.content_username"),
        "git_content_path": fields.String(required=True, description="Root path of the policy in git repo.",
                                          attribute="data.policies.content_path"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of\
         the activity they perform, for example provisioning, Account Management, Utilization, etc.\
          This value is displayed in this field.", attribute="data.policies.classification"),
        "sub_classification": fields.String(required=True, description="Sub classification of policy",
                                            attribute="data.policies.sub_classification"),
        "severity": fields.String(required=True, description="Severity of policy such as low, medium and high",
                                  attribute="data.policies.severity"),
        "is_system_policy": fields.String(required=True, description="Flag to identify system policy",
                                          attribute="data.policies.is_system_policy"),
        "uri": fields.String(required=True, description="Unique URI for policy", attribute="data.policies.uri")
    }


def policy_data_model_list():
    return {
        'policy_id': fields.String(required=True, description="Policy Id", attribute='id'),
        'name': fields.String(required=True, description="Policy Name"),
        'display_name': fields.String(required=True, description="Display name of policy"),
        'uri': fields.String(required=True, description="Unique URI for policy"),
        'description': fields.String(required=True, description="A brief explanation of the policy."),
        'status': fields.String(required=True, description="Indicates whether the policy is active or inactive."),
        'services': fields.List(fields.String, required=True, description="Displays the service associated with the\
        policy, for example, AWS, AzureRM, Openstack., etc"),
        'engine_type': fields.String(required=True, description="Engine type of policy where it will execute"),
        'content_type': fields.String(required=True, description="Content type of policy (Git or File)"),
        'scope': fields.String(required=True, description="Scope of the policy"),
        "severity": fields.String(required=True, description="Severity of policy such as low, medium and high"),
        "has_recommendations": fields.Boolean(required=False,
                                              description="is recommendations configured on failure of policy"),
        "is_parameterized": fields.Boolean(required=False,
                                           description="is parameter required to execute policy")
    }


def policy_job_response():
    return {
        "job_id": fields.String(required=True, description="Job Id", attribute='data.id'),
        "name": fields.String(required=True, description="Name of the Job", attribute='data.name'),
        "status": fields.String(required=True, description="Status of job execution", attribute='data.status'),
        "status_reason": fields.String(required=True, description="Reason for the job status",
                                       attribute='data.status_reason'),
        "engine": fields.String(required=True, description="Policy engine used for job execution",
                                attribute='data.engine'),
        "arguments": fields.String(required=True, description="arguments provided for job execution",
                                   attribute='data.args'),
        "service_accounts": fields.String(required=True, description="Service account used for job execution",
                                          attribute='data.service_accounts'),
        "execution_type": fields.String(required=True, description="Policy execution type can be on demand or scheduled"
                                        , attribute='data.execution_type'),
        "created_by": fields.String(required=True, description="Policy Job created by", attribute='data.created_by'),
        "created_at": fields.String(required=True, description="Policy Job create time", attribute='data.created_at'),
        "updated_by": fields.String(required=True, description="Policy Job updated by", attribute='data.updated_by'),
        "updated_at": fields.String(required=True, description="Policy Job update time", attribute='data.updated_at'),
        "tenant_name": fields.String(required=True, description="tenant name where job was created",
                                     attribute='data.project_name'),
        "policy_id": fields.String(required=True, description="Policy id of the Policy executed",
                                   attribute='data.policy_id'),
        "policy_name": fields.String(required=True, description="Policy id of the Policy executed",
                                     attribute='data.policy_name')

    }


def policy_execute_model(arguments, service_account):
    return {
        "args": fields.Nested(arguments, required=True, default={}, description="arguments to execute policy"),
        "service_accounts": fields.List(fields.Nested(service_account),
                                        required=True, description="service account details to execute the policy")
    }


def service_account_details():
    return {
        'service_type': fields.String(required=True, description="Type of the service (Eg. Cloud, Monitoring, "
                                                                 "Virtualization etc.). "),
        'service_name': fields.String(required=True, description="The service name of the associated service "
                                                                 "account, for example, AWS,Azure etc"),
        "id": fields.String(required=True, description="Identifier of the cloud account on which the "
                                                       "policy will be executed")
    }


def policy_execute_response():
    return {
        "job_id": fields.String(required=True, description="Job identifier of the executed policy",
                                attribute="data.job_id")
    }


def policy_response_list(policy_data_model):
    return {
        'policies': fields.Nested(policy_data_model,
                                  required=True, description="Policy Metadata Info.",
                                  attribute='data.policies',
                                  skip_none=True),
    }


def create_policy_data_model():
    return {
        'policy_id': fields.String(required=True, description="policy Id.", attribute="data")
    }


def policy_delete_response():
    return {
        'message': fields.String(required=True, description="Response message.")
    }


def policy_metadata_model():
    return {
        'file': fields.String(required=False, description="Metadata about policy", skip_none=True)
    }


def policy_update_response():
    return {
        'updated': fields.String(required=True, description="Response Message.",
                                 attribute="data")
    }
