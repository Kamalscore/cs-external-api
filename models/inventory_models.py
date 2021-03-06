# This file is subject to the terms and conditions defined in the file
# 'LICENSE.txt', which is part of this source code package.


from flask_restplus import fields


def inventory_tags_model_list():
    return {
        'key': fields.List(fields.String, required=False, description="Tags associated with the resource for inventory")
    }


def inventory_filter_data_model_list():
    return {
        'data': fields.List(fields.Raw, required=True, description="Filters available in inventory"),
        'type': fields.String(required=True, description="Type of the data available in models list", attribute='label')
    }


def inventory_filter_response(inventory_filter_data_model):
    return {
        'filters': fields.Nested(inventory_filter_data_model, required=True,
                                 description="Filters available in inventory", attribute='data.filters')
    }


def inventory_category_count_filter_data_model():
    return {
        'cloud_account': fields.List(fields.String, required=True, description="Id's for the cloud account"),
        'resource_category': fields.String(required=False, description="Name for the category"),
        'region': fields.List(fields.String, required=False,
                              description="List of regions for the resource filter data"),
        'tags': fields.Raw(required=False, description="List of tags associated with the resource details")
    }


def inventory_category_count_request(inventory_count_detail_model):
    return {
        'identifier': fields.String(required=True, description="Category/Resource based count for the cloud",
                                    default="category", enum=["category", "resource"]),
        'filters': fields.Nested(inventory_count_detail_model, required=True, description="Resource filters detail")
    }


def inventory_category_count_data_model_list():
    return {
        'count': fields.String(required=True, description="Count based on the category for account"),
        'data': fields.String(required=True, description="Count details")
    }


def inventory_resource_count_model_data():
    return {
        'count': fields.String(required=False, description="Inventory category count details", attribute='count'),
        'resource_category': fields.String(required=False, description="Name of the category", attribute='category'),
        'resource_type': fields.String(required=False, description="Name of the component", attribute='component'),
        'resource': fields.String(required=False, description="Name of the resource", attribute='resource'),
    }


def inventory_category_count_model_data():
    return {
        'count': fields.String(required=False, description="Inventory category count details", attribute='count'),
        'resource_category': fields.String(required=False, description="Name of the category", attribute='category')
    }


def inventory_category_count_response(inventory_category_count_model_data_list, inventory_resource_count_model_data_list):
    return {
        'category_details': fields.Nested(inventory_category_count_model_data_list, required=False,
                                          description="Inventory category count details",
                                          attribute='data.category_count_details', skip_none=True),
        'resource_details': fields.Nested(inventory_resource_count_model_data_list, required=False,
                                          description="Inventory resource count details",
                                          attribute='data.all', skip_none=True)
    }


def inventory_resource_request_filter_data_model():
    return {
        'cloud': fields.String(required=True, description="Name of the cloud"),
        'cloud_account': fields.List(fields.String, required=True, description="Id of the cloud account"),
        'resource_category': fields.String(required=True, description="Name of the category"),
        'resource_type': fields.String(required=True, description="Name of the component"),
        'resource': fields.String(required=True, description="Name of the resource"),
        'region': fields.List(fields.String, required=False,
                              description="List of regions for the resource filter data"),
        'tags': fields.Raw(required=False, description="List of tags associated with the resource details")
    }


def inventory_resource_request(inventory_resource_request_filter_data_model_list):
    return {
        'filters': fields.Nested(inventory_resource_request_filter_data_model_list, required=True,
                                 description="Filter resource details")
    }


def inventory_resource_list_model_data():
    return {
        'tenant_id': fields.String(required=True, description="tenant_id of the resource inventory",
                                   attribute='project_id'),
        'cloud': fields.String(required=True, description="Name of the cloud", attribute='service_name'),
        'cloud_account_id': fields.String(required=True, description="Id of the cloud account",
                                          attribute='service_account_id'),
        'cloud_account_name': fields.String(required=True, description="Inventory summary details",
                                            attribute='service_account_name'),
        'resource_category': fields.String(required=True, description="Name of the category",
                                           attribute='category'),
        'resource_type': fields.String(required=True, description="Name of the component", attribute='component'),
        'resource': fields.String(required=True, description="Name of the resource",
                                  attribute='resource'),
        'corestack_resource_id': fields.String(required=True, description="Unique element for the resource",
                                               attribute='check_resource_element'),
        'tags': fields.Raw(required=True, description="Tags associated with the resource", attribute='tags'),
        'summary_details': fields.Raw(required=True, description="Inventory summary details",
                                      attribute='summary_details'),
    }


def inventory_response_details(inventory_resource_list_model_list):
    return {
        'count': fields.String(required=True, description="Inventory summary details",
                               attribute='data.total_count'),
        'resource_details': fields.Nested(inventory_resource_list_model_list, required=True,
                                          description="Inventory summary details",
                                          attribute='data.resource_list')
    }
