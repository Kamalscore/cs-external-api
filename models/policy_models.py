# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from flask_restplus import fields


def policy_create_model(policy_meta_data):
    return {
        "name": fields.String(required=True, description="policy name"),
        "description": fields.String(required=True, description="A brief explanation of the policy."),
        "type": fields.List(fields.String, required=False, description="Indicates the type of policy"),
        "category": fields.String(required=True, description="The category will be either service or resource"),
        "resource_type": fields.List(fields.String, required=False,
                                     description="The category will be either service or resource"),
        "content": fields.String(required=True, description="The policy content"),
        "is_system_policy": fields.Boolean(),
        "metadata": fields.Nested(policy_meta_data, required=False, description="Metadata about policy"),
        "engine_type": fields.String(required=True,
                                     description="Engine type of policy, mandatory if content type is git.", default="",
                                     enum=["congress", "azure_policy", "aws_config", "chef_inspec"]),
        "services": fields.List(fields.String, required=True, description="Displays the service associated with the\
        policy, for example, AWS, AzureRM, Openstack., etc,"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of the\
        activity they perform, for example provisioning, Account Management, 	Utilization, etc. This value is\
        displayed in this field"),
        "sub_classification": fields.String(required=True, description="Sub classification for policy"),
        "scope": fields.String(required=True,
                               description="The scope of the policy (global, accout, tenant or private)",
                               enum=["global", "account", "tenant", "private"]),
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
        "resource_type": fields.List(fields.String, required=False,
                                     description="The category will be either service or resource"),
        "content": fields.String(required=True, description="The policy content"),
        "is_system_policy": fields.Boolean(),
        "metadata": fields.Nested(policy_meta_data, required=False, description="Metadata about policy"),
        "engine_type": fields.String(required=False,
                                     description="Engine type of policy, mandatory if content type is git.", default="",
                                     enum=["congress", "azure_policy", "aws_config", "chef_inspec"]),
        "services": fields.List(fields.String, required=True, description="Displays the service associated with the\
           policy, for example, AWS, AzureRM, Openstack., etc,"),
        "classification": fields.String(required=True, description="Policies are classified based on the basis of the\
           activity they perform, for example provisioning, Account Management, 	Utilization, etc. This value is\
           displayed in this field"),
        "sub_classification": fields.String(required=True, description="Sub classification for policy"),
        "scope": fields.String(required=True,
                               description="The scope of the policy (global, accout, tenant or private)",
                               enum=["global", "account", "tenant", "private"]),
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
        'file': fields.String(required=True, description="Metadata about policy")
    }


def policy_update_response():
    return {
        'updated': fields.String(required=True, description="Response Message.",
                                  attribute="data")
    }


def policy_view_response(policy_meta_data):
    return {
        "id": fields.String(required=True, description="The unique identifier created for each policy.",
                            attribute="data.policies.id"),
        "name": fields.String(required=True, description="The name of the policy.", attribute="data.policies.name"),
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
        "metadata": fields.Nested(policy_meta_data, required=True, description="Metadata about policy",
                                  attribute="data.policies.metadata"),
        "scope": fields.String(required=True, description="The scope of the policy.",
                               attribute="data.policies.scope", enum=["global", "account", "tenant", "private"]),
        "content_type": fields.String(required=True, description="Content type of policy (Git or File)",
                                      attribute="data.policies.content_type"),
        "content": fields.String(required=True, description="The policy content.", attribute="data.policies.content"),
        "content_url": fields.String(required=True, description="Git project URL when the content type is git.",
                                     attribute="data.policies.content_url"),
        "content_username": fields.String(required=True, description="Username of Git repo if repo is authenticated",
                                          attribute="data.policies.content_username"),
        "content_path": fields.String(required=True, description="Root path of the policy in git repo.",
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
