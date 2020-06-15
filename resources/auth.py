import logging

from flask import request
from flask_restplus import Resource, marshal

from app import api
from client import get_token
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION, CS_ENDPOINT_URL_DEFAULT_VALUE, \
    CS_ENDPOINT_URL_PROPERTY_NAME
from definitions.auth_definitions import AuthURLDefinitions
from models.swagger_models import auth_request, auth_response, token, error, auth_tenant_model, user_timezone_model, \
    auth_user_model, refresh_auth_token_request, refresh_auth_token_response
from utils.HelperUtils import getClassName, invoke_api

auth_name_space = api.namespace(name='Tokens', path="/", description='Manage Tokens')
tokenModel = api.model('Token', token(), discription="This contains the attributes "
                                                     "access_token, expires_at & "
                                                     "issued_at. access_token will be "
                                                     "passed with X-Auth-Token header in "
                                                     "all other APIs for authentication.", for_doc_alone=True)
authTenantModel = api.model('TokenTenantModel', auth_tenant_model(), description="List of tenants within the "
                                                                                 "CoreStack account. Each tenant will "
                                                                                 "have an id & name that uniquely "
                                                                                 "identifies it.", for_doc_alone=True)
requestModel = api.model('AuthRequest', auth_request())
RefreshTokenRequestModel = api.model('RefreshTokenRequestModel', refresh_auth_token_request())
RefreshTokenResponseModel = api.model('RefreshTokenResponseModel', refresh_auth_token_response())
auth_api_definition = AuthURLDefinitions.URLInfo
timezoneModel = api.model('TimezoneModel', user_timezone_model(), for_doc_alone=True)
userModel = api.model('UserModel', auth_user_model(timezoneModel), description="Contains information about the user "
                                                                               "associated with the Access Key / Secret "
                                                                               "Key.", for_doc_alone=True)
responseModel = api.model('AuthResponse', auth_response(tokenModel, authTenantModel, userModel))
# responseDetailedModel = api.model('AuthDetailedResponse', auth_detailed_response(tokenModel, userModel, wildcardModel))
# responseDetailedModel = api.inherit('AuthDetailedResponse', responseModel, auth_detailed_response(tokenModel, userModel, wildcardModel))
errorModel = api.model('Error', error())


@auth_name_space.route("/v1/auth/tokens")
class AuthResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(AuthResource))

    @api.doc(id='authToken', name="Auth Request",
             description="CoreStack requires Auth token to be passed in all the API headers. "
                         "Auth token has to be generated and it is valid only for an hour. New "
                         "token can be generated using this API. Extract Auth-token, "
                         "Tenant "
                         "Id & Account Id from the response. This will be required in most of "
                         "the API calls")
    @api.expect(requestModel, validate=True, name='authRequest')
    # @auth_name_space.response(model=responseDetailedModel, code=201, description='Created')
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


@auth_name_space.route("/v1/auth/tokens/refresh")
class AuthResourceRefresh(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(AuthResourceRefresh))

    @api.doc(id='RefreshToken', name="Refresh Token Request",
             description="Token generated in authToken API will be valid for an hour. Post that access_token will "
                         "automatically expire. When the access_token is expired, there are two options. "
                         "<ol> <li> use the authToken API to generate a new token </li>"
                         "<li> use refreshToken API to extend the validity of the current token. </li> </ol>"
                         "The refreshed token will also expire after an hour, refer to expires_at in the response for "
                         "the validity of the token. When the refreshed token also expires, call again the "
                         "refreshToken API to extend it further. Like wise a token can extended 3 times, "
                         "refer to refresh_count in the response. After 3 refresh attempts, token will expire and "
                         "cannot be extended any further. Need to use authToken API to generate a new token.",
             )
    @api.expect(RefreshTokenRequestModel, validate=True, name='refresh token')
    @auth_name_space.response(model=RefreshTokenResponseModel, code=200, description='Success')
    @auth_name_space.response(model=errorModel, code=400, description='Bad Request')
    @auth_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @auth_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            t = request.json
            token_value = t.pop("access_token")
            t["token_id"] = token_value
            headers = request.headers
            args = request.args
            format_params = {}
            base_url = getProperty(WEB_CONFIG_SECTION, CS_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(auth_api_definition, 'refresh_token', format_params, args=args,
                                  headers=headers, req_body=t, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), RefreshTokenResponseModel), 200
            else:
                message, response_code = marshal(response.json(), errorModel), response.status_code
                if message.get("message") == "Token Expired. Please login again":
                    message["message"] = "Token Expired and cannot be extended using refreshToken API. " \
                                  "Use authToken API to generated a new token"
                return message, response_code
        except KeyError as e:
            auth_name_space.abort(402, e.__doc__, status=e, statusCode="402")
        except Exception as e:
            auth_name_space.abort(500, e.__doc__, status=e, statusCode="500")
