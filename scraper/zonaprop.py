from bs4 import BeautifulSoup
import cloudscraper
import urllib.request
import json
import gzip
import brotli

from scraper.enums import PropertyType, Currency, Page
from scraper.property import Property
from scraper.utils import to_number

ZONAPROP_API_PATH = "/rplis-api/postings"
URL_ZONAPROP = "https://www.zonaprop.com.ar"


def get_max_page_number(response):
    return response["paging"]["totalPages"]


def get_response_api(pageNumber):
    with open('./scraper/resources/zonapropRequest.json') as file:
        file_contents = file.read()
    requestJson = json.loads(file_contents)
    requestJson["pagina"] = pageNumber
    scraper = cloudscraper.create_scraper()
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-AR,es-US;q=0.9,es;q=0.8,en-US;q=0.7,en;q=0.6,es-419;q=0.5',
        'Content-Type':'application/json',
        'User-Agent':'PostmanRuntime/7.30.0',
        'Postman-Token': 'ca67ce84-f171-4fb3-a5b8-5c5f1a848b37',
        'Connection':'keep-alive',
        'Cache-Control':'no-cache',
        'Host':'www.zonaprop.com.ar'
         }
    response = scraper.post(URL_ZONAPROP+ZONAPROP_API_PATH,json=requestJson)
    return response


def read_property_zonaprop(data):
    property = Property(page=Page.ZONAPROP)

    property.url = URL_ZONAPROP + data["url"]
    property.title = data["title"]
    property.description = data["description"]

    # Set data of price (precio, moneda, expensas)
    operation_types = data["priceOperationTypes"]
    for operation_type in operation_types:
        if operation_type["operationType"]["name"] == "Alquiler":
            price = operation_type["prices"][0]
            property.price = price["amount"] if "amount" in price else 0
            property.set_currency(price["currency"] if "currency" in price else "ARS")

    property.expenses = data["expenses"]["amount"] if "expenses" in data and "amount" in data["expenses"] else 0

    # Set data of features (superficie, ambientes, dormitorios, banios, cochera)
    features = data["mainFeatures"]
    keys = features.keys()

    for key in keys:
        value = to_number(features[key]["value"]) if "value" in features[key] else 0

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
    property.address = post_location["address"]["name"] if "address" in post_location and "name" in post_location["address"] else ""

    if "location" in post_location and "label" in post_location["location"] and post_location["location"]["label"] == "BARRIO":
        property.neighborhood = post_location["location"]["name"]
    else:
        property.neighborhood = post_location["location"]["parent"]["name"] if "location" in post_location and "parent" in post_location["location"] and "name" in post_location["location"]["parent"] else ""

    return property

def zonaprop():

    page = 1
    totalPages = 1
    properties = set()

    while page <= totalPages:
        response = get_response_api(page).json()
        totalPages = response["paging"]["totalPages"]
        postings = response["listPostings"]
        for post in postings:
            properties.add(read_property_zonaprop(post))
