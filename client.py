# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import requests


def _url(path):
    return "http://localhost:18080" + path


def get_token(access_key=str, secret_key=str):
    """
    :param access_key: Access Key
    :param secret_key: Secret Key

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    body = {"access_key": access_key, "secret_key": secret_key}
    return requests.post(_url("/v1/auth/tokens"), json=body)


def get_tenants(access_token=str):
    """
    :param access_token: Access Token

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    headers = {"X-Auth-User": access_token}
    return requests.get(_url("/v1/projects"), headers=headers)


def get_tenant(access_token, tenant_id):
    """
    :param access_token: Access Token
    :param tenant_id: Tenant id

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    headers = {"X-Auth-User": access_token}
    return requests.get(_url("/v1/projects/"+tenant_id), headers=headers)


def delete_tenant(access_token, tenant_id):
    """
    :param access_token: Access Token
    :param tenant_id: Tenant id

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    headers = {"X-Auth-User": access_token}
    return requests.delete(_url("/v1/projects/"+tenant_id), headers=headers)


def create_tenant(access_token=str(), body=dict):
    """
    :param access_token: Access Token
    :param body: request body

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    headers = {"X-Auth-User": access_token}
    return requests.post(_url("/v1/projects"), json=body, headers=headers)


def update_tenant(access_token, tenant_id, body):
    """
    :param tenant_id:
    :param access_token: Access Token
    :param body: request body

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    headers = {"X-Auth-User": access_token}
    return requests.put(_url("/v1/projects/"+tenant_id), json=body, headers=headers)
