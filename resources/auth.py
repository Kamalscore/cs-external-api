import logging

from flask import jsonify, make_response, request, abort
from flask_restplus import Resource
from models.swagger_models import auth_request, auth_response, token, error

from app import api, app
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
    @api.marshal_with(responseModel, code=201, description='Created')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def post(self):
        try:
            print(request.json)

            return {
                "message": "New token created",
            }
        except KeyError as e:
            auth_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
