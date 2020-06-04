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


def get_projects(access_token=str):
    """
    :param access_token: Access Token

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    headers = {"X-Auth-User": access_token}
    return requests.get(_url("/v1/projects"), headers=headers)
