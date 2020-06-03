import logging

from flask import request, abort
from flask_restplus import Resource, marshal

from cllient import get_token
from models.swagger_models import auth_request, auth_response, token, error

from app import api
from utils.HelperUtils import getClassName

auth_name_space = api.namespace(name='Tokens', path="/", description='Manage Tokens')
tokenModel = api.model('Token', token())
requestModel = api.model('AuthRequest', auth_request())
responseModel = api.model('AuthResponse', auth_response(tokenModel))
errorModel = api.model('Error', error())


@auth_name_space.route("/v1/auth/tokens")
class AuthResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(AuthResource))

    @api.doc(name="Auth Request", description='Authentication Request')
    @api.expect(requestModel, validate=True)
    @auth_name_space.response(model=responseModel, code=201, description='Created', )
    @auth_name_space.response(model=errorModel, code=400, description='Bad Request')
    @auth_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @auth_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            print(request.json)
            response = get_token(request.json["access_key"], request.json["secret_key"])
            if response.status_code == 200:
                return marshal(response.json(), responseModel), 201
            else:
                # TODO Need to raise the proper errors by checking the status like 400, 401, 403 etc...
                raise abort(response.text.encode('utf8'))
        except KeyError as e:
            auth_name_space.abort(500, e.__doc__, status=e, statusCode="500")
