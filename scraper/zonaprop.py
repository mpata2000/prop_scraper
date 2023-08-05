import cloudscraper
import json
import logging
import time
import traceback

from .property import Property
from .utils import to_number

ZONAPROP_API_PATH = "/rplis-api/postings"
URL_ZONAPROP = "https://www.zonaprop.com.ar"
logger = logging.getLogger()

# Makes a request to the API and returns the response
# @param pageNumber number of the page to request
# @return response of the request
def get_response_api(pageNumber:int):
    with open('./scraper/resources/zonapropRequest.json') as file:
        file_contents = file.read()
    requestJson = json.loads(file_contents)
    requestJson["pagina"] = pageNumber
    scraper = cloudscraper.create_scraper()
    response = scraper.post(URL_ZONAPROP+ZONAPROP_API_PATH,json=requestJson)
    response.raise_for_status()
    return response


def read_property_zonaprop(data:dict):
    property = Property()

    property.url = URL_ZONAPROP + data["url"]

    # Set data of price (precio, moneda, expensas)
    operation_types = data["priceOperationTypes"]
    for operation_type in operation_types:
        if operation_type["operationType"]["name"] == "Alquiler":
            price = operation_type["prices"][0]
            property.price = price.get("amount",0)
            property.set_currency(price.get("currency", "ARS"))

    if data["visiblePictures"] is not None and data["visiblePictures"].get("pictures") is not None:
        pics = data["visiblePictures"].get("pictures", [])
        property.pics_urls = [pic["resizeUrl1200x1200"] for pic in pics]

    property.expenses = data["expenses"].get("amount", 0) if data["expenses"] is not None else 0

    features = data["mainFeatures"]

    for key in features:
        value = to_number(features[key].get("value",0))

        if key == "CFT100":
            property.totalArea = value
        elif key == "CFT101":
            property.coveredArea = value
        elif key == "CFT1":
            property.rooms = value
        elif key == "CFT2":
            property.bedrooms = value
        elif key == "CFT3":
            property.bathrooms = value
        elif key == "CFT7":
            property.garage = value

    # Set data of property type
    property.set_property_type(data["realEstateType"]["name"])

    # Set data of location (barrio, direccion, coordenadas)
    post_location = data["postingLocation"]
    property.address = post_location["address"].get("name", "") if post_location["address"] is not None else ""

    location = post_location.get("location", {})
    if location.get("label") == "BARRIO":
        property.neighborhood = location.get("name", "")
    else:
        parent_location = location.get("parent", {})
        property.neighborhood = parent_location.get("name", "")

    property.neighborhood = property.neighborhood.upper()

    return property

# Get all the properties for rent in CABA from Zonaprop
# @return set of properties
def get_rent_properties_caba():
    page = 1
    totalPages = 1
    properties = set()
    start_time = time.time()

    while page <= totalPages:
        try:
            response = get_response_api(page).json()
            totalPages = response["paging"]["totalPages"] if page == 1 else totalPages
            postings = response["listPostings"]
            for post in postings:
                properties.add(read_property_zonaprop(post))
        except Exception as e:
            logger.error(f"Error getting properties from Zonaprop at page {page}: {e}")
            logger.error(traceback.format_exc())

        page += 1

    elapsed_time = time.time() - start_time
    logger.info(f"Time taken to get properties from Zonaprop: {elapsed_time:.2f} seconds for {len(properties)} properties")
    return properties
