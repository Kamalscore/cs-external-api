# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restplus import Api

authorizations = {
    'auth_user': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Auth-User'
    },
    'auth_token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Auth-Token'
    }
}

app = Flask(__name__)
api = Api(app=app, version="1.0.0", title="Corestack External API", description="A Service API Wrapper!",
          terms_url="http://corestack.io/",
          contact="Contact CloudEnablers", contact_email="dev@cloudenablers.com",
          license="CloudEnablers Inc License", license_url="http://corestack.io/licenses/LICENSE-2.0.html",
          authorizations=authorizations)
app.config['RESTPLUS_MASK_SWAGGER'] = False
CORS = CORS(app)
ma = Marshmallow(app)
