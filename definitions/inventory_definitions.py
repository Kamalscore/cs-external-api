# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class InventoryURLDefinitions(object):
    URLInfo = dict(
        get_count_details=dict(
            path='/v2/{tenant_id}/resources/count',
            method='post'
        ),
        get_filter_details=dict(
            path='/v2/{tenant_id}/resources/filters',
            method='get'
        )
    )
