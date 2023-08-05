import requests
import json
import logging
import time
import traceback

from .enums import Currency, Page
from .property import Property
from .utils import NEIGHBORHOODS_CABA, to_number, chunks

MELI_URL = "https://api.mercadolibre.com"
logger = logging.getLogger()

# Make a GET request to the given url raising an exception if it fails
# @return Response of the request
def get_api_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

# Get ids from api response, max results for each url is 1000
# @param urls list of urls of MercadoLibre
# @return list of ids
def get_ids(urls: list[str]):
    ids = []
    for url in urls:
        offset = 0
        max_results = 1
        while offset <= max_results:
            try:
                api_response = get_api_response(url + f"&offset={offset}")
                json_data = api_response.json()
                ids.extend([x.get("id", "") for x in json_data["results"]])
            except Exception as e:
                logger.error(f"Error getting ids from {url} with offset {offset}: {e}")

            max_results = min(json_data["paging"]["total"], 1000) if max_results == 1 else max_results
            offset += 50
    return ids

# Parse a property from the given data
# @param data json data from the API response
# @return Property
def parse_properties(data: dict):
    property_data = {}
    property_data["url"] = data.get("permalink", "")
    property_data["price"] = int(data.get("price", 0))
    property_data["currency"] = Currency.from_str(data.get("currency_id", "ARS"))
    property_data["neighborhood"] = data.get("location", {}).get("neighborhood", {}).get("name", "").upper()
    property_data["address"] = data.get("location", {}).get("address_line", "")
    property_data["page"] = Page.MELI

    property_data["pics_urls"] = [pic["url"] for pic in data.get("pictures", [])]

    attributes = data.get("attributes", [])
    for attribute in attributes:
        attr_id = attribute.get("id", "")
        value = to_number(attribute.get("value_name", "0"))
        if attr_id == "ROOMS":
            property_data["rooms"] = value
        elif attr_id == "BEDROOMS":
            property_data["bedrooms"] = value
        elif attr_id == "FULL_BATHROOMS":
            property_data["bathrooms"] = value
        elif attr_id == "TOTAL_AREA":
            property_data["total_area"] = value
        elif attr_id == "COVERED_AREA":
            property_data["covered_area"] = value
        elif attr_id == "MAINTENANCE_FEE":
            property_data["expenses"] = value
        elif attr_id == "PARKING_LOTS":
            property_data["garage"] = value

    return Property(**property_data)

# Get properties by ids
# @param ids list of ids of MercadoLibre properties
# @return of response of the API
def get_by_ids(ids):
    # Split ids in chunks of 20 because the API only allows 20 ids per request
    urls = [f"{MELI_URL}/items?ids={','.join(ids_chunk)}" for ids_chunk in chunks(ids, 20)]
    properties_data = []

    for url in urls:
        try:
            api_response = get_api_response(url)
            response_json = api_response.json()
            properties_data.extend(response_json)
        except Exception as e:
            logger.error(f"Error getting response from MercadoLibre: {e}")

    return properties_data

# Get properties for rent in CABA
# @return set of Property
def get_rent_properties_caba():
    start_time = time.time()
    base_url = f"{MELI_URL}/sites/MLA/search?category=MLA1473"
    urls = [f"{base_url}&q={neighborhood}+capital+federal" for neighborhood in NEIGHBORHOODS_CABA]

    ids = get_ids(urls)

    properties = set()
    ids_response = get_by_ids(ids)
    for prop in ids_response:
        try:
            property_data = parse_properties(prop["body"])
            properties.add(property_data)
        except Exception as e:
            logger.error(f"Error parsing property from MercadoLibre: {e}")
            logger.error(traceback.format_exc())

    elapsed_time = time.time() - start_time
    logger.info(f"Time taken to get properties from MercadoLibre: {elapsed_time:.2f} seconds for {len(properties)} properties")
    return properties
