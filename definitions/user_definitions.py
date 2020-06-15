# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class UserUrlDefinitions(object):
    URLInfo = dict(
        list=dict(
            path='/v1/users',
            method='get'
        ),
        view=dict(
            path='/v1/users/{user_id}',
            method='get'
        ),
        create=dict(
            path='/v1/users',
            method='post'
        ),
        update=dict(
            path='/v1/users/{user_id}',
            method='put'
        ),
        delete=dict(
            path='/v1/users/{user_id}',
            method='delete'
        ),
        update_password=dict(
            path='/v1/users/{user_id}/changepassword',
            method='put'
        ),
        update_timezone=dict(
            path='/v1/users/{user_id}/changetimezone',
            method='put'
        )
    )
