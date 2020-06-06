# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'


class ScriptURLDefinitions(object):
    URLInfo = dict(
        list=dict(
            path='/v1/{tenant_id}/scripts',
            method='get'
        ),
        view=dict(
            path='/v1/{tenant_id}/scripts/{script_id}',
            method='get'
        ),
        scan=dict(
            path='/v1/{tenant_id}/scripts',
            method='post',
            query_params=dict(action='scan')
        ),
        create=dict(
            path='/v1/{tenant_id}/scripts',
            method='post'
        ),
        update=dict(
            path='/v1/{tenant_id}/scripts/{script_id}',
            method='put'
        ),
        delete=dict(
            path='/v1/{tenant_id}/scripts/{script_id}',
            method='delete'
        ),
        execute=dict(
            path='/v1/{tenant_id}/scripts',
            method='post',
            query_params=dict(action='execute')
        )
    )
