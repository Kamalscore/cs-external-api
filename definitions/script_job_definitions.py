# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

__author__ = 'nagalakshmi'


class ScripJobURLDefinitions(object):
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
