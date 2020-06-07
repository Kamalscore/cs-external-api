# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import base64
import inspect
import json
import time
from urllib.parse import urlencode

import requests

from client import _url
from utils.Constants import CS_ENDPOINT_URL_DEFAULT_VALUE

currentTimeInMillis = lambda: int(round(time.time() * 1000))


def getClassName(klass=object):
    return klass.__name__


def isNone(key):
    return key is None


def isNotNone(key):
    return key is not None


def parseToBool(val):
    """Convert a string representation of truth to True or False.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.\n
    **Note:** It doesn't raise any Error if 'val' is anything else.\n

    :rtype: bool
    """
    if isinstance(val, bool):
        return val
    val = val.lower() if isNotNone(val) else ""
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        return False


def importClass(fullyQualifiedClassName):
    components = fullyQualifiedClassName.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def listMethods(fullyQualifiedClassName):
    return inspect.getmembers(
        importClass(fullyQualifiedClassName) if type(fullyQualifiedClassName) is str else fullyQualifiedClassName,
        predicate=inspect.ismethod)


def hasMethod(fullyQualifiedClassName, methodName):
    for m in listMethods(fullyQualifiedClassName):
        if isNotNone(m) and type(m) is tuple and isNotNone(m[0]):
            if str(methodName).__eq__(str(m[0])):
                return True
    return False


def executeMethod(fullyQualifiedClassName, methodName, *args):
    _class = importClass(fullyQualifiedClassName) if type(fullyQualifiedClassName) is str else fullyQualifiedClassName
    return getattr(_class(), methodName)(*args)


def equalsIgnoreCase(a, b):
    try:
        return a.lower() == b.lower()
    except AttributeError:
        return a == b


def strToList(strList, delimiter):
    if isNone(strList):
        return []
    return str(strList).split(delimiter)


def getDecodedValue(encryptedValue):
    return base64.standard_b64decode(encryptedValue)


def invoke_api(definition, action, format_params=None, req_body=None, args=None, headers=None,
               base_url=CS_ENDPOINT_URL_DEFAULT_VALUE):
    url = definition.get(action, {}).get('path', '').format(**format_params)
    if not args:
        args = {}
    if definition.get(action, {}).get('query_params'):
        args.update(definition.get(action, {}).get('query_params'))
    url = _url(url, base_url)
    if args:
        url = url + '?' + urlencode(args)
    return requests.request(definition.get(action, {}).get('method'), url, data=json.dumps(req_body),
                            headers=headers)
