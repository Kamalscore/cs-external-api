# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from app import api, app
from resources.auth import auth_name_space
from resources.policy import policy_name_space
from resources.scripts import script_name_space
from resources.tenant_id_ns import tenant_id_name_space
from resources.tenants import tenant_name_space
from resources.favicon import Fav16, Fav32

api.add_namespace(auth_name_space)
api.add_namespace(tenant_name_space)
api.add_namespace(tenant_id_name_space)
api.add_namespace(policy_name_space)
api.add_namespace(script_name_space)

if __name__ == '__main__':
    # Enable or disable the mask field, by default X-Fields
    app.run(debug=True)
