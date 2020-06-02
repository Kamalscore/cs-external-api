from flask import Flask, jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app=app, version="1.0.0", title="API Wrapper", description="A Service API Wrapper!",
          terms_url="http://corestack.io/",
          contact="Contact CloudEnablers", contact_email="dev@cloudenablers.com",
          license="CloudEnablers Inc License", license_url="http://corestack.io/licenses/LICENSE-2.0.html")
app.config['RESTPLUS_MASK_SWAGGER'] = False
CORS = CORS(app)
ma = Marshmallow(app)

