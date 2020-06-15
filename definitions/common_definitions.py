# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


class RequestMapping(object):
    create_user = {
        "timezone": "timezone_id",
        "project_master_id": "account_id",
        "roles": "role_assignment",
        "require_access_key": "is_accesskey_required"
    }
    change_timezone = {
        "current_timezone": "current_timezone_id",
        "new_timezone": "new_timezone_id"
    }
