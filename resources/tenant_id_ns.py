# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging

from flask_restplus import Resource, fields

from models.swagger_models import error, service_acc_response, service_acc_data_model

from app import api
from utils.HelperUtils import getClassName

tenant_id_name_space = api.namespace(name='Token Id', path="/", description='Manage Token Id based resources')
dataModel = api.model('ServiceAccData', service_acc_data_model())
serviceAccResponseModel = api.model('ServiceAccResponse', service_acc_response(dataModel))
errorModel = api.model('Error', error())


@tenant_id_name_space.route("/v1/<string:tenant_id>/cloudaccounts")
class AuthResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(AuthResource))

    @api.doc(name="Service Account Request", description='Authentication Request')
    @api.marshal_list_with(serviceAccResponseModel, code=200, description='Success')
    @api.marshal_with(errorModel, code=400, description='Bad Request')
    @api.marshal_with(errorModel, code=401, description='Unauthorized')
    @api.marshal_with(errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            # Todo: Talk to QA and get the response
            # Todo: Map the QA data to wrapper data

            return [{
                "message": "List response",
            }]
        except KeyError as e:
            tenant_id_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
