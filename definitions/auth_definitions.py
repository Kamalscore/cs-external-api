# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class AuthURLDefinitions(object):
    URLInfo = dict(
        refresh_token=dict(
            path='/v1/auth/tokens?action=refresh',
            method='post'
        )
    )
