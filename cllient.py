import requests


def _url(path):
    return "http://52.229.12.111:18080" + path


def get_token(access_key=str, secret_key=str):
    """
    :param access_key: Access Key
    :param secret_key: Secret Key

    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    body = {"access_key": access_key, "secret_key": secret_key}
    return requests.post(_url("/v1/auth/tokens"), json=body)
