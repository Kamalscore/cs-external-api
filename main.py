# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.
import os
import sys

from app import api, app
from config.LogManager import initLogManager
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION
from config.config_loader import _processTemplate
from resources.auth import auth_name_space
from resources.cloud_account import cloud_account_name_space
from resources.inventory import inventory_name_space
from resources.policy import policy_name_space
from resources.roles import role_name_space
from resources.scripts import script_name_space
from resources.script_jobs import script_job_name_space
from resources.tenants import tenant_name_space
from resources.users import user_name_space
from resources.favicon import Fav16, Fav32



api.add_namespace(auth_name_space)
api.add_namespace(tenant_name_space)
api.add_namespace(policy_name_space)
api.add_namespace(script_name_space)
api.add_namespace(script_job_name_space)
api.add_namespace(inventory_name_space)
api.add_namespace(cloud_account_name_space)
api.add_namespace(user_name_space)
api.add_namespace(role_name_space)

if __name__ == '__main__':
    # For loading the config file, take the location from command line
    # configFilePath = ['/tmp/etc/config.ini']
    # _processTemplate(sys.argv[1:])

    # load from etc
    if os.path.exists('/etc/cs-external-api/cs-external-api.ini'):
        config_path = '/etc/cs-external-api/cs-external-api.ini'
    # else load default
    else:
        project_dir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir))
        config_path = "%s/etc/config.ini" % project_dir
    _processTemplate([config_path])
    # # Load the logging related configuration ans prepare the logging.
    initLogManager()
    port = getProperty(WEB_CONFIG_SECTION,  'web.port', '4000')
    app.run(host='0.0.0.0', debug=True, port=port)
