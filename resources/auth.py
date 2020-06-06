import logging

from flask import request
from flask_restplus import Resource, marshal

from client import get_token
from models.swagger_models import auth_request, auth_response, token, error, auth_tenant_model, user_timezone_model, \
    auth_user_model, auth_detailed_response

from app import api
from utils.HelperUtils import getClassName

auth_name_space = api.namespace(name='Tokens', path="/", description='Manage Tokens')
tokenModel = api.model('Token', token(), discription="This contains the attributes "
                                                     "access_token, expires_at & "
                                                     "issued_at. access_token will be "
                                                     "passed with X-Auth-Token header in "
                                                     "all other APIs for authentication.")
authTenantModel = api.model('TokenTenantModel', auth_tenant_model(), description="List of tenants within the "
                                                                                 "CoreStack account. Each tenant will "
                                                                                 "have an id & name that uniquely "
                                                                                 "identifies it.")
requestModel = api.model('AuthRequest', auth_request())
timezoneModel = api.model('TimezoneModel', user_timezone_model())
userModel = api.model('User', auth_user_model(timezoneModel), description="Contains information about the user "
                                                                          "associated with the Access Key / Secret "
                                                                          "Key.")
responseModel = api.model('AuthResponse', auth_response(tokenModel, authTenantModel, userModel))
# responseDetailedModel = api.model('AuthDetailedResponse', auth_detailed_response(tokenModel, userModel, wildcardModel))
#responseDetailedModel = api.inherit('AuthDetailedResponse', responseModel, auth_detailed_response(tokenModel, userModel, wildcardModel))
errorModel = api.model('Error', error())


@auth_name_space.route("/v1/auth/tokens")
class AuthResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(AuthResource))

    @api.doc(name="Auth Request", description="CoreStack requires Auth token to be passed in all the API headers. "
                                              "Auth token has to be generated and it is valid only for an hour. New "
                                              "token can be generated using this API.<br><br>Extract <b>Auth-token, "
                                              "Tenant "
                                              "Id & Account Id</b> from the response. This will be required in most of "
                                              "the API calls</br>")
    @api.expect(requestModel, validate=True, name='authRequest')
    #@auth_name_space.response(model=responseDetailedModel, code=201, description='Created')
    @auth_name_space.response(model=responseModel, code=201, description='Created')
    @auth_name_space.response(model=errorModel, code=400, description='Bad Request')
    @auth_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @auth_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            # is_detail_required = bool(request.args.get('is_detail_required'))
            print(request.json)
            response = get_token(request.json["access_key"], request.json["secret_key"])
            if response.status_code == 200:
                return marshal(response.json(), responseModel), 201
            else:
                # TODO Need to raise the proper errors by checking the status like 400, 401, 403 etc...
                return response.text.encode('utf8'), response.status_code
        except KeyError as e:
            auth_name_space.abort(402, e.__doc__, status=e, statusCode="402")
        except Exception as e:
            auth_name_space.abort(500, e.__doc__, status=e, statusCode="500")
