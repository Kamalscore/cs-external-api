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
        )
    )
