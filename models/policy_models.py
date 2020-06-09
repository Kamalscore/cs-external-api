# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from flask_restplus import fields


def policy_create_model():
    return {
        "name": fields.String(required=True, description="policy name which is unique and does not allow special "
                                                         "character or space"),
        "display_name": fields.String(required=False, description="Display name of policy which allow space this is to "
                                                                  "mostly show on the ui"),
        "description": fields.String(required=True, description="A brief explanation of the policy."),
        "type": fields.List(fields.String, required=False, description="Indicates the type of policy"),
        "category": fields.String(required=True, description="The category will be either service or resource"),
        "content": fields.String(required=True, description="The policy content"),
        "is_system_policy": fields.Boolean(required=False, description="Flag to identify system policies"),
        "engine_type": fields.String(required=True,
                                     description="Engine type of policy, mandatory if content type is git.", default="",
                                     enum=["azure_policy", "aws_config", "chef_inspec", "congress", ]),
        "cloud": fields.List(fields.String, required=True, description="Displays the cloud associated with the\
        policy, for example, AWS, Azure etc"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of the\
        activity they perform, for example provisioning, Account Management, 	Utilization, etc. This value is\
        displayed in this field"),
        "sub_classification": fields.String(required=True, description="Sub classification for policy"),
        "scope": fields.String(required=True,
                               description="The scope of the policy Account scope - All users under that account will "
                                           "have access to view and execute Only Account admins can update/delete the "
                                           "policies, Tenant Scope - Users with access to the specific tenant will have"
                                           "access to policies who can describe or execute policies. Tenant admins "
                                           "can  only update/delete. Private Scope - User who created will only have "
                                           "access",
                               default="",
                               enum=["account", "tenant", "private"]),
        "content_type": fields.String(required=True, description="Policy content source (git, file)", default="",
                                      enum=["git", "file"]),
        "content_password_or_key": fields.String(
            required=False, description="Password or private key to access of Git repo if repo is authenticated "
                                        "required only in case of content type git"),
        "content_username": fields.String(required=False, description="Username of Git repo if repo is authenticated "
                                                                      "required only in case of content type git"),
        "content_url": fields.String(required=False, description="Git project URL when the content type is git "
                                                                 "required only in case of content type git"),
        "content_path": fields.String(required=False, description="Root path of the policy in git repo required only "
                                                                  "in case of content type git"),
        "severity": fields.String(required=True
                                  , description="Severity of policy", default="", enum=["low", "medium", "high"])
    }


def policy_update_model(policy_meta_data):
    return {
        "name": fields.String(required=True, description="policy name which is unique and does not allow space or "
                                                         "special character"),
        "display_name": fields.String(required=False, description="Display name of policy which allow space this is to "
                                                                  "mostly show on the ui"),
        "description": fields.String(required=False, description="A brief explanation of the policy."),
        "type": fields.List(fields.String, required=False, description="Indicates the type of policy"),
        "category": fields.String(required=True, description="The category will be either service or resource"),
        "content": fields.String(required=True, description="The policy content"),
        "is_system_policy": fields.Boolean(required=False, description="Flag to identify system policies"),
        "metadata": fields.Nested(policy_meta_data, required=False, description="Metadata about policy"),
        "engine_type": fields.String(required=False,
                                     description="Engine type of policy, mandatory if content type is git.", default="",
                                     enum=["azure_policy", "aws_config", "congress", "chef_inspec"]),
        "cloud": fields.List(fields.String, required=True, description="Displays the cloud associated with the policy,"
                                                                       " for example, AWS, Azure etc"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of the\
           activity they perform, for example provisioning, Account Management, 	Utilization, etc. This value is\
           displayed in this field"),
        "sub_classification": fields.String(required=True, description="Sub classification for policy"),
        "scope": fields.String(required=True,
                               description="The scope of the policy Account scope - All users under that account will "
                                           "have access to view and execute Only Account admins can update/delete the "
                                           "policies, Tenant Scope - Users with access to the specific tenant will have"
                                           "access to policies who can describe or execute policies. Tenant admins "
                                           "can  only update/delete. Private Scope - User who created will only have "
                                           "access",
                               default="",
                               enum=["account", "tenant", "private"]),
        "content_type": fields.String(required=False, description="Policy content source (git, file)", default="",
                                      enum=["git", "file"]),
        "content_password_or_key": fields.String(
            required=False, description="Password or private key to access of Git repo if repo is authenticated "
                                        "required if the content type is git"),
        "content_username": fields.String(required=False, description="Username of Git repo if repo is authenticated "
                                                                      "required if the content type is git"),
        "content_url": fields.String(required=False, description="Git project URL when the content type is git "
                                                                 "required if the content type is git"),
        "content_path": fields.String(required=False, description="Root path of the policy in git repo required if "
                                                                  "the content type is git"),
        "severity": fields.String(required=False
                                  , description="Severity of policy", default="", enum=["low", "medium", "high"])
    }


def policy_view_response():
    return {
        "policy_id": fields.String(required=True, description="The unique identifier created for each policy.",
                                   attribute="data.policies.id"),
        "policy_name": fields.String(required=True, description="The name of the policy without space or special "
                                                                "character ",
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
        "scope": fields.String(required=True,
                               description="The scope of the policy Account scope - All users under that account will "
                                           "have access to view and execute Only Account admins can update/delete the "
                                           "policies, Tenant Scope - Users with access to the specific tenant will have"
                                           "access to policies who can describe or execute policies. Tenant admins "
                                           "can  only update/delete. Private Scope - User who created will only have "
                                           "access",
                               default="",
                               attribute="data.policies.scope",
                               enum=["account", "tenant", "private"]),
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
        'policy_id': fields.String(required=True, description="Policy Id is unique identifier of a policy",
                                   attribute='id'),
        'name': fields.String(required=True, description="Policy Name is unique can allow only"),
        'display_name': fields.String(required=True, description="Display name of policy"),
        'uri': fields.String(required=True, description="Unique URI for policy"),
        'description': fields.String(required=True, description="A brief explanation of the policy."),
        'status': fields.String(required=True, description="Indicates whether the policy is active or inactive."),
        'services': fields.List(fields.String, required=True, description="Displays the service associated with the\
        policy, for example, AWS, AzureRM, Openstack., etc"),
        'engine_type': fields.String(required=True, description="Engine type of policy where it will execute"),
        'content_type': fields.String(required=True, description="Content type of policy (Git or File)"),
        "scope": fields.String(required=True,
                               description="The scope of the policy Account scope - All users under that account will "
                                           "have access to view and execute Only Account admins can update/delete the "
                                           "policies, Tenant Scope - Users with access to the specific tenant will have"
                                           "access to policies who can describe or execute policies. Tenant admins "
                                           "can  only update/delete. Private Scope - User who created will only have "
                                           "access"),
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
        "cloud_accounts": fields.String(required=True, description="Cloud account used for job execution",
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


def policy_recommendation_response():
    return {
        "recommendation_id": fields.String(required=True, description="unique recommendation Id",
                                           attribute='id'),
        "recommendation_name": fields.String(required=True, description="recommendation name",
                                             attribute='name'),
        "policy_id": fields.List(fields.String, required=True, description="list of policy ids for which the "
                                                                           "recommendation exists",
                                 attribute='policy_id'),
        "status": fields.String(required=True, description="resolution status of the recommendation the values will be"
                                                           "open, resolved",
                                attribute='status'),
        "impact": fields.String(required=True, description="impact of recommended changes", attribute='impact'),
        "classification": fields.String(required=True, description="classified based on the kind of recommendation"
                                                                   "provided to the user can be cost, security etc"
                                        , attribute='classification'),
        "cloud_account_id": fields.String(required=True, description="cloud account id impacted by the recommendation",
                                          attribute='service_account_id'),
        "cloud": fields.String(required=True, description="cloud on which this account exits for which the "
                                                          "recommendations exists", attribute='service_name'),
        "tenant_name": fields.String(required=True, description="tenant for which the recommendation exits ",
                                     attribute='project_name'),
        "created_at": fields.String(required=True, description="time at which the recommendation was created",
                                    attribute='created_at'),

    }


def recommendation_action_response():
    return {
        "name": fields.String(required=True, description="recommendation action name"),
        "terms_and_conditions": fields.String(required=True, description="Terms and conditions for performing the "
                                                                         "recommended action"),
        "resource_level": fields.String(required=True, description="if the action will be performed at the resource "
                                                                   "level"),
        "action_type": fields.String(required=True, description="Type of action will be always template"),
        "action_resource_name": fields.String(required=True, description="Name of template"),
        "description": fields.String(required=True, description="Description about the action in details"),
    }


def resource_recommendation_response():
    return {
        "resource_recommendation_id": fields.String(required=True,
                                                    description="unique identifier for resource recommendation",
                                                    attribute='id'),
        "resource_id": fields.String(required=True, description=" Resource identifier id of resource recommendation"),
        "resource_name": fields.String(required=True,
                                       description="Resource identifier name of resource recommendation"),
        "resource_type": fields.String(required=True, description="Type of resource"),
        "resourcegroup_location": fields.String(required=True, description="resource group location"),
        "status": fields.String(required=True, description="Status of resource recommendation")
    }


def policy_view_recommendation_response(actions_obj, resource_obj):
    return {
        "recommendation_id": fields.String(required=True, description="unique recommendation Id",
                                           attribute='data.id'),
        "recommendation_name": fields.String(required=True, description="recommendation name",
                                             attribute='data.name'),
        "policy_id": fields.List(fields.String, required=True, description="list of policy ids for which the "
                                                                           "recommendation exists",
                                 attribute='data.policy_id'),
        "status": fields.String(required=True, description="resolution status of the recommendation the values will be"
                                                           "open, resolved", attribute='data.status'),
        "impact": fields.String(required=True, description="impact of recommended changes", attribute='data.impact'),
        "classification": fields.String(required=True, description="classified based on the kind of recommendation"
                                                                   "provided to the user can be cost, security etc"
                                        , attribute='data.classification'),
        "cloud_account_id": fields.String(required=True, description="cloud account id impacted by the recommendation",
                                          attribute='data.service_account_id'),
        "cloud": fields.String(required=True, description="cloud on which this account exits for which the "
                                                          "recommendations exists", attribute='data.service_name'),
        "tenant_name": fields.String(required=True, description="tenant for which the recommendation exits ",
                                     attribute='data.project_name'),
        "created_at": fields.String(required=True, description="time at which the recommendation was created",
                                    attribute='data.created_at'),
        "description": fields.String(required=True, description="Description about the recommendation in details",
                                     attribute='data.description'),
        "actions": fields.List(fields.Nested(actions_obj), required=True,
                               description="List of actions which can be performed to resolve the policy violations",
                               attribute='data.actions', skip_none=True),
        "resources": fields.List(fields.Nested(resource_obj), required=True,
                                 description="List of resources on which the recommendations can be performed",
                                 attribute='data.resources', skip_none=True),
    }


def policy_execute_model(arguments, service_account):
    return {
        "args": fields.Nested(arguments, required=True, default={},
                              description="arguments to execute policy for example values can be in the below format "
                                          "{'listOfAllowedSKUs':['Basic_A0']} or {'requiredRetentionDays':'365',"
                                          "'effect':'AuditIfNotExists'} etc.The values are dynamic in nature can "
                                          "change from policy to policy"),
        "cloud_accounts": fields.List(fields.Nested(service_account), required=True,
                                      description="cloud account details to execute the policy")
    }


def service_account_details():
    return {
        'cloud': fields.String(required=True, description="The cloud name of the account for which the policy"
                                                          "will be executed ex: Azure, AWS etc"),
        "cloud_account_id": fields.String(required=True, description="Identifier of the cloud account on boarded in "
                                                                     "the on boarding section")
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
        'policy_id': fields.String(required=True, description="unique policy Id returned", attribute="data")
    }


def policy_delete_response():
    return {
        'message': fields.String(required=True, description="Delete Response message.")
    }


def policy_metadata_model():
    return {
        'file': fields.String(required=False, description="Metadata about policy", skip_none=True)
    }


def policy_update_response():
    return {
        'message': fields.String(required=True, description="Response Message on update",
                                 attribute="message")
    }


def policy_recommendations_response_list(data_model):
    return {
        'recommendations': fields.Nested(data_model,
                                         required=True, description="Policy recommendation Info list",
                                         attribute='data.recommendations',
                                         skip_none=True),
    }


def execute_recommendation_req(arguments):
    return {
        'action_name': fields.String(required=True, description="action to perform to resolve violations, the name can"
                                                                "be obtained from the view recommendation api"),
        'resources': fields.List(fields.String, required=True,
                                 description="resource resource_recommendation_id list for which the recommendation"
                                             "will be executed, this value can be obtained from the view "
                                             "recommendation api"),
        "args": fields.Nested(arguments, required=False, default={},
                              description="arguments to execute recommendation if any"
                                          "The values are dynamic in nature can change from recommendation to "
                                          "recommendation"),

    }


def execute_recommendation_response():
    return {
        'message': fields.String(required=True, description="Execute policy response message", attribute="data")
    }
