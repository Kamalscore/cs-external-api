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
        create=dict(
            path='/v1/{tenant_id}/scripts',
            method='post'
        ),
        update=dict(
            path='/v1/{tenant_id}/scripts/{script_id}',
            method='put'
        ),
        execute=dict(
            path='/v1/{tenant_id}/scripts',
            method='post',
            query_params=dict(action='execute')
        )
    )

class ScripJobtURLDefinitions(object):
    URLInfo = dict(
        list=dict(
            path='/v1/{tenant_id}/scriptjobs',
            method='get'
        ),
        view=dict(
            path='/v1/{tenant_id}/scriptjobs/{script_job_id}',
            method='get',
            query_params=dict(version='v1')
        )
    )