# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'

from flask_restplus import fields


def script_job_list_model():
    return {
        'script_job_id': fields.String(description="Unique ID of the Script Job", attribute='id'),
        'script_job_name': fields.String(description="Name of the Script Job", attribute='name'),
        'status': fields.String(required=True, description="Overall status of the script execution", attribute='status'),
        'status_reason': fields.String(required=True, description="Error message if failed", attribute='status_reason'),
        'started_at': fields.String(required=True, description="Script Job start time in UTC", attribute='created_at'),
        'completed_at': fields.String(required=True, description="Script Job completion time in UTC"
                                      , attribute='completed_at', skip_none=True),
        'execution_type': fields.String(required=True, description="Script Job execution type (on_demand/scheduled)",
                                        attribute='execution_type'),
        "initiated_by" : fields.String(required=True, description="User who initiated the script execution",
                                        attribute='user_name')
    }


def script_job_list_response(script_job_list_model):
    return {
        'total_script_jobs': fields.String(required=True, description="Total number of script jobs available",
                                       attribute='data.total_count'),
        'total_pages': fields.String(required=True, description="Total number of pages",
                                     attribute='data.page_count'),
        'script_jobs': fields.Nested(script_job_list_model,
                                 required=True, description="Script Jobs List.",
                                 attribute='data.jobs',
                                 skip_none=True)
    }

def script_job_script_info_data_model(wild_card_model):
    return {
        'script_id': fields.String(required=True, description="Script Id", attribute='id'),
        'script_name': fields.String(required=True, description="Script Name", attribute='name'),
        "config_type": fields.String(required=True, description='Config type of the script(s)'),
        "parameters": fields.Nested(wild_card_model, required=True, description="Parameters of the script.",
                                    skip_none=True),
        "parameter_source": fields.String(description="Parameter source - whether as per the one defined in script "
                                                      "or custom json", default="script", enum=["script", "json"]),
        "output_parameters": fields.Nested(wild_card_model, required=True, skip_none=True,
                                           description="Output parameters of the script (all applied parameters)."),
        'status': fields.String(required=True, description="Status of the script execution"),
        'status_reason': fields.String(required=True, description="Error message if failed"),
        'started_at': fields.String(required=True, description="Execution start time in UTC")
    }


def script_job_job_info_model(script_info_model):
    return {
        "host": fields.String(required=True, description="Target machine's IP/DNS"),
        "username": fields.String(required=True, description="Username of the target machine"),
        'platform': fields.String(required=True, description="Platform of the target machine."),
        'script_info': fields.Nested(script_info_model,
                                     description="Script execution details", attribute='script_info')
    }

def script_job_view_model(job_info_model):
    return {
        'script_job_id': fields.String(description="Unique ID of the Script Job", attribute='data.id'),
        'script_job_name': fields.String(description="Name of the Script Job", attribute='data.name'),
        'status': fields.String(required=True, description="Overall status of the script execution", attribute='data.status'),
        'status_reason': fields.String(required=True, description="Error message if failed", attribute='data.status_reason'),
        'started_at': fields.String(required=True, description="Script Job start time in UTC", attribute='data.created_at'),
        'completed_at': fields.String(required=True, description="Script Job completion time in UTC", attribute='data.completed_at'),
        'execution_type': fields.String(required=True, description="Script Job execution type (on_demand/scheduled)",
                                        attribute='data.execution_type'),
        "initiated_by" : fields.String(required=True, description="User who initiated script execution",
                                        attribute='data.user_name'),
        "job_info" : fields.Nested(job_info_model,
                                     description="Script execution details", attribute='data.job_info')
    }
