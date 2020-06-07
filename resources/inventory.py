# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.

import logging

from flask import request, abort
from flask_restplus import Resource, marshal

from app import api
from config.ConfigManager import getProperty, WEB_CONFIG_SECTION, CS_ENDPOINT_URL_DEFAULT_VALUE, \
    CS_INVENTORY_ENDPOINT_URL_PROPERTY_NAME
from definitions.inventory_definitions import InventoryURLDefinitions
from models.inventory_models import inventory_filter_response, inventory_filter_data_model_list, \
    inventory_category_count_request, inventory_category_count_response, inventory_category_count_data_model_list, \
    inventory_category_count_filter_data_model, inventory_response_details, \
    inventory_resource_request_filter_data_model, inventory_resource_request
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
# inventory resource details
inventoryResourceRequestModelDataList = api.model('InventoryResourceDetailsDataModel',
                                                  inventory_resource_request_filter_data_model())
inventoryResourceRequestModel = api.model('InventoryResourceDetailsRequest',
                                          inventory_resource_request(inventoryResourceRequestModelDataList))
inventoryResponseModel = api.model('InventoryResourceDetails', inventory_response_details())
errorModel = api.model('Error', error())
inventory_api_definition = InventoryURLDefinitions.URLInfo


@inventory_name_space.route("/v1/<string:tenant_id>/inventory/count")
class InventoryCategoryDetails(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(InventoryResource))

    @api.doc(name="Get inventory category count",
             description='Get inventory category/resource count based on the cloud',
             params={'service_name': {'description': '', 'in': 'query', 'type': 'str', 'enum': ['AWS', 'Azure'],
                                      'default': 'AWS'},
                     "tenant_id": "Specify the tenant Id for the policy"},
             security=['auth_user', 'auth_token'])
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
            base_url = getProperty(WEB_CONFIG_SECTION, CS_INVENTORY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(inventory_api_definition, 'get_count_details', format_params, req_body, args=args,
                                  headers=headers, base_url=base_url)
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
             params={'service_name': {'description': '', 'in': 'query', 'type': 'str', 'enum': ['AWS', 'Azure'],
                                      'default': 'AWS'},
                     "tenant_id": "Specify the tenant Id for the policy"},
             security=['auth_user', 'auth_token'])
    @inventory_name_space.response(model=inventoryFiltersResponseModelList, code=200, description='Success')
    @inventory_name_space.response(model=errorModel, code=400, description='Bad Request')
    @inventory_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @inventory_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def get(self, tenant_id):
        try:
            headers = request.headers
            args = request.args
            format_params = {'tenant_id': tenant_id}
            base_url = getProperty(WEB_CONFIG_SECTION, CS_INVENTORY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(inventory_api_definition, 'get_filter_details', format_params, args=args,
                                  headers=headers, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), inventoryFiltersResponseModelList), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            inventory_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")


@inventory_name_space.route("/v1/<string:tenant_id>/inventory/resources")
class InventoryResource(Resource):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(getClassName(InventoryResource))

    @api.doc(name="Get Inventory Filters",
             description='Get resource details based on the cloud accounts, category, component, resource.',
             params={"tenant_id": "Specify the tenant Id for the policy"},
             security=['auth_user', 'auth_token'])
    @api.expect(inventoryResourceRequestModel, validate=True)
    @inventory_name_space.response(model=inventoryResponseModel, code=200, description='Success')
    @inventory_name_space.response(model=errorModel, code=400, description='Bad Request')
    @inventory_name_space.response(model=errorModel, code=401, description='Unauthorized')
    @inventory_name_space.response(model=errorModel, code=500, description='Internal Server Error')
    def post(self, tenant_id):
        try:
            req_body = marshal(request.json, inventoryResourceRequestModel, ordered=True, skip_none=True)
            format_params = {
                'tenant_id': tenant_id
            }
            args = request.args
            headers = request.headers
            base_url = getProperty(WEB_CONFIG_SECTION, CS_INVENTORY_ENDPOINT_URL_PROPERTY_NAME,
                                   CS_ENDPOINT_URL_DEFAULT_VALUE)
            response = invoke_api(inventory_api_definition, 'get_resource_details', format_params, req_body, args=args,
                                  headers=headers, base_url=base_url)
            if response.status_code == 200:
                return marshal(response.json(), inventoryResponseModel, ordered=True, skip_none=True), 200
            else:
                return marshal(response.json(), errorModel), response.status_code
        except Exception as e:
            inventory_name_space.abort(500, e.__doc__, status="Internal Server Error", statusCode="500")
