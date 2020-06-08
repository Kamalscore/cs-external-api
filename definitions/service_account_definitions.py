# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class ServiceAccountUrlDefinitions(object):
    URLInfo = dict(
        list=dict(
            path='/v1/{tenant_id}/serviceaccounts',
            method='get'
        ),
        view=dict(
            path='/v1/{tenant_id}/serviceaccounts/{service_account_id}',
            method='get'
        ),
        create=dict(
            path='/v1/{tenant_id}/serviceaccounts',
            method='post'
        ),
        update=dict(
            path='/v1/{tenant_id}/serviceaccounts/{service_account_id}',
            method='put'
        ),
        delete=dict(
            path='/v1/{tenant_id}/serviceaccounts/{service_account_id}',
            method='delete'
        ),
        rediscover=dict(
            path='/v1/{tenant_id}/serviceaccounts',
            method='get',
            query_params=dict(type='re-discover', action='sync')
        )
    )
