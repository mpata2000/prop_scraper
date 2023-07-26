import requests
import json
import gzip
import brotli

from scraper.enums import PropertyType, Currency, Page
from scraper.property import Property

MELI_URL = "https://api.mercadolibre.com"

def get_ids(data):
    return [x.get("id", "") for x in data]

def get_value_from_attribute(attribute):
    value = attribute.get("value_name", "0")
    try:
        return int("".join(filter(str.isdigit, value)))
    except ValueError:
        return 0

# Parse a property from the given data
# @param data json data from the API response
# @return Property
def parse_properties(data):
    property_data = {}
    property_data["url"] = data.get("permalink", "")
    property_data["title"] = data.get("title", "")
    property_data["price"] = int(data.get("price", 0))
    property_data["currency"] = Currency.from_string(data.get("currency_id", "ARS"))
    property_data["neighborhood"] = data.get("location", {}).get("neighborhood", {}).get("name", "")
    property_data["address"] = data.get("location", {}).get("address_line", "")
    property_data["page"] = Page.MELI

    attributes = data.get("attributes", [])
    for attribute in attributes:
        attr_id = attribute.get("id", "")
        if attr_id == "ROOMS":
            property_data["rooms"] = get_value_from_attribute(attribute)
        elif attr_id == "BEDROOMS":
            property_data["bedrooms"] = get_value_from_attribute(attribute)
        elif attr_id == "FULL_BATHROOMS":
            property_data["bathrooms"] = get_value_from_attribute(attribute)
        elif attr_id == "TOTAL_AREA":
            property_data["total_area"] = get_value_from_attribute(attribute)
        elif attr_id == "COVERED_AREA":
            property_data["covered_area"] = get_value_from_attribute(attribute)
        elif attr_id == "MAINTENANCE_FEE":
            property_data["expenses"] = get_value_from_attribute(attribute)
        elif attr_id == "PARKING_LOTS":
            property_data["garage"] = get_value_from_attribute(attribute)

    return Property(**property_data)

# Get properties by ids
# @param ids list of ids of MercadoLibre properties
# @return of response of the API
def get_by_ids(ids):
    urls = [f"{MELI_URL}/items?ids={','.join(ids_chunk)}" for ids_chunk in chunks(ids, 20)]
    properties_data = []

    for url in urls:
        api_response = get_api_response(url)
        if api_response is not None and api_response.status_code == 200:
            response_json = api_response.json()
            properties_data.extend(response_json)

    return properties_data

# Split a list into chunks of the given size
# @return list of chunks
def chunks(input_list, chunk_size):
    return [input_list[i:i+chunk_size] for i in range(0, len(input_list), chunk_size)]

# Make a GET request to the given url
# @return response or None if failed
def get_api_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve API response: {e}")
        return None

# Get properties for rent in CABA
# @return set of Property
def get_rent_properties_caba():
    # Get neighborhoods from wikipedia?
    neighborhoods = [
        "Agronomia", "Almagro", "Balvanera", "Barracas", "Belgrano", "Boedo", "Caballito",
        "Chacarita", "Coghlan", "Colegiales", "Constitucion", "Flores", "Floresta", "La%20Boca",
        "La%20Paternal", "Liniers", "Mataderos", "Monte%20Castro", "Monserrat", "Nueva%20Pompeya",
        "Nunez", "Palermo", "Parque%20Avellaneda", "Parque%20Chacabuco", "Parque%20Chas",
        "Parque%20Patricios", "Puerto%20Madero", "Recoleta", "Retiro", "Saavedra", "San%20Cristobal",
        "San%20Nicolas", "San%20Telmo", "Velez%20Sarsfield", "Versalles", "Villa%20Crespo",
        "Villa%20del%20Parque", "Villa%20Devoto", "Villa%20General%20Mitre", "Villa%20Lugano",
        "Villa%20Luro", "Villa%20Ortuzar", "Villa%20Pueyrredon", "Villa%20Real", "Villa%20Riachuelo",
        "Villa%20Santa%20Rita", "Villa%20Soldati", "Villa%20Urquiza"
    ]

    base_url = f"{MELI_URL}/sites/MLA/search?category=MLA1473"
    urls = []
    for neighborhood in neighborhoods:
        urls.append(f"{base_url}&q={neighborhood}")

    properties = set()

    for url in urls:
        offset = 0
        max_results = 1
        while offset <= max_results:
            api_response = get_api_response(url + f"&offset={offset}")
            json_data = api_response.json()

            max_results = min(json_data["paging"]["total"], 1000) if max_results == 1 else max_results
            ids = get_ids(json_data["results"])
            ids_response = get_by_ids(ids)
            for prop in ids_response:
                property_data = parse_properties(prop["body"])
                properties.add(property_data)
            offset += 50

    return properties
