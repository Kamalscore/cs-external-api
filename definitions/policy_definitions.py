# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class PolicyURLDefinitions(object):
    URLInfo = dict(
        view=dict(
            path='/v1/{project_id}/policies/{policy_id}',
            method='get'
        ),
        list=dict(
            path='/v1/{project_id}/policies',
            method='get'
        ),
        create=dict(
            path='/v1/{project_id}/policies',
            method='post'
        ),
        update=dict(
            path='/v1/{project_id}/policies/{policy_id}',
            method='put'
        ),
        delete=dict(
            path='/v1/{project_id}/policies/{policy_id}',
            method='delete'
        ),
        execute=dict(
            path='/v1/{project_id}/policies/{policy_id}/execute',
            method='post'
        ),
        job_details=dict(
            path='/v1/{project_id}/policy_jobs/{job_id}',
            method='get'
        ),
        policy_recommendations=dict(
            path='/v1/{project_id}/recommendations',
            method='get'
        ),
        recommendation_view=dict(
            path='/v1/{project_id}/recommendations/{recommendation_id}',
            method='get'
        ),
        execute_recommendation=dict(
            path='/v1/{project_id}/recommendations/{recommendation_id}/resolve',
            method='post'
        )
    )
