# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class RoleUrlDefinitions(object):
    URLInfo = dict(
        list=dict(
            path='/v1/{tenant_id}/roles',
            method='get'
        ),
        get_roleid=dict(
            path='/v1/{tenant_id}/roles',
            method='post',
            query_params=dict(action='list_roleids')
        )
    )
