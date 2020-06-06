# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.
import os
import sys

from app import api, app
from config.LogManager import initLogManager
from config.config_loader import _processTemplate
from resources.auth import auth_name_space
from resources.cloud_account import cloud_account_name_space
from resources.inventory import inventory_name_space
from resources.policy import policy_name_space
from resources.script_jobs import script_job_name_space
from resources.scripts import script_name_space
from resources.tenant_id_ns import tenant_id_name_space
from resources.tenants import tenant_name_space


api.add_namespace(auth_name_space)
api.add_namespace(tenant_name_space)
api.add_namespace(tenant_id_name_space)
api.add_namespace(policy_name_space)
api.add_namespace(script_name_space)
api.add_namespace(script_job_name_space)
api.add_namespace(inventory_name_space)
api.add_namespace(cloud_account_name_space)

if __name__ == '__main__':
    # For loading the config file, take the location from command line
    # configFilePath = ['/tmp/etc/config.ini']
    # _processTemplate(sys.argv[1:])
    project_dir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir))
    _processTemplate(["%s/etc/config.ini" % project_dir])
    # Load the logging related configuration ans prepare the logging.
    initLogManager()

    app.run(host='0.0.0.0', debug=True, port=4000)
