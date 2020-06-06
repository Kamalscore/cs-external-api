# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging

from flask import request, abort
from flask_restplus import Resource, marshal

from app import api
from definitions.inventory_definitions import InventoryURLDefinitions
from models.inventory_models import inventory_filter_response, inventory_filter_data_model_list, \
    inventory_category_count_request, inventory_category_count_response, inventory_category_count_data_model_list, \
    inventory_category_count_filter_data_model
from models.swagger_models import error, wild_card_model
from utils.HelperUtils import getClassName, invoke_api

inventory_name_space = api.namespace(name='Inventory', path="/", description='Manage Inventory')
wildcardModel = api.model('Dict', wild_card_model())
# Filters api
inventoryFilterDataModelList = api.model('InventoryData', inventory_filter_data_model_list())
inventoryFiltersResponseModelList = api.model('InventoryResponse',
                                              inventory_filter_response(inventoryFilterDataModelList))
# Category count api
inventoryCountDetailsModel = api.model('CountDetailsDataModel', inventory_category_count_filter_data_model())
inventoryCategoryCountRequestModel = api.model('CategoryCountRequest',
                                               inventory_category_count_request(inventoryCountDetailsModel))
inventoryCategoryCountDataModelList = api.model('CategoryCount', inventory_category_count_data_model_list())
inventoryCategoryCountResponseModel = api.model('CategoryCountResponse',
                                                inventory_category_count_response())
errorModel = api.model('Error', error())
inventory_api_definition = InventoryURLDefinitions.URLInfo


@inventory_name_space.route("/v1/<string:tenant_id>/inventory/count")
class InventoryCategoryDetails(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(InventoryResource))

    @api.doc(name="Get inventory category count",
             description='Get inventory category count',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'},
                 'service_name': {'description': '', 'in': 'query', 'type': 'str', 'enum': ['AWS', 'Azure'],
                                  'default': 'AWS'}
             })
    @api.expect(inventoryCategoryCountRequestModel, validate=True)
    @inventory_name_space.response(model=inventoryCategoryCountResponseModel, code=200, description='Success')
    @inventory_name_space.response(model=errorModel, code=400, description='Bad Request')
    @inventory_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @inventory_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, inventoryCategoryCountRequestModel, ordered=True, skip_none=True)
            format_params = {
                'tenant_id': tenant_id
            }
            args = request.args
            headers = request.headers
            response = invoke_api(inventory_api_definition, 'get_count_details', format_params, req_body, args=args,
                                  headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), inventoryCategoryCountResponseModel, ordered=True, skip_none=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            inventory_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@inventory_name_space.route("/v1/<string:tenant_id>/inventory/filters")
class InventoryResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(InventoryResource))

    @api.doc(name="Get Inventory Filters",
             description='Get all the available filters for the corresponding cloud.',
             params={
                 'X-Auth-User': {'description': 'Username', 'in': 'header', 'type': 'str'},
                 'X-Auth-Token': {'description': 'Auth token', 'in': 'header', 'type': 'str'},
                 'service_name': {'description': '', 'in': 'query', 'type': 'str', 'enum': ['AWS', 'Azure'],
                                  'default': 'AWS'}
             })
    @inventory_name_space.response(model=inventoryFiltersResponseModelList, code=200, description='Success')
    @inventory_name_space.response(model=errorModel, code=400, description='Bad Request')
    @inventory_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @inventory_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id}
            response = invoke_api(inventory_api_definition, 'get_filter_details', format_params, args=args,
                                  headers=headers)
            if response.status_code == 200:
                return marshal(response.json(), inventoryFiltersResponseModelList), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            inventory_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
