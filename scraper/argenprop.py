
import re
from bs4 import BeautifulSoup
import requests

from scraper.enums import Page,PropertyType
from scraper.property import Property
from scraper.utils import to_number

URL_ARGENPROP="https://www.argenprop.com"



def scrape_property_argenprop(element):
    property = Property(page=Page.ARGENPROP)

    property.url = URL_ARGENPROP + element.find('a')['href']
    property.setPropertyType(property.url.split("/")[3].split("-")[0])

    card_price = element.select_one('p.card__price')
    if card_price.select_one('.card__noprice') is None:
        property.currency = card_price.select_one('.card__currency').text.strip()
        property.price = to_number(card_price.contents[2])

    property.address = element.select_one('.card__address').get_text().strip()
    property.neighborhood = element.select('.card__title--primary')[-1].get_text().split(",")[0]
    property.expenses = to_number(element.select_one('.card__expenses').get_text())

    # Extract the description
    description = element.select_one("p.card__info").text.strip()

    # Extract the URLs of the images
    image_urls = [img["data-src"] for img in element.select("ul.card__photos li img[data-src]") if img["data-src"]]


    features = element.select('.card__main-features>li')

    for feature in features:
        value = to_number(feature.get_text())

        icon_class = feature.select_one('i')['class'][0]
        if icon_class == "icono-superficie_total":
            property.totalArea = value
        elif icon_class == "icono-superficie_cubierta":
            property.coveredArea = value
        elif icon_class == "icono-cantidad_ambientes":
            property.rooms = value
        elif icon_class == "icono-cantidad_dormitorios":
            property.bedrooms = value
        elif icon_class == "icono-cantidad_banos":
            property.bathrooms = value
        elif icon_class == "icono-ambiente_cochera":
            property.garage = value
        else:
            pass

    return property

def get_urls_argenprop():
    url = URL_ARGENPROP + "/departamento-y-casa-alquiler-localidad-capital-federal"
    response = requests.get(url)
    doc = BeautifulSoup(response.content, "html.parser")
    href = doc.select(".pagination__page>a")
    max_pages = min(to_number(href[-2].get_text()), 99)
    URLs = [url + (f"-pagina-{i}" if i != 1 else "") for i in range(1, max_pages + 1)]
    return URLs

def get_rent_properties_caba():
    urls = get_urls_argenprop()
    properties = set()

    for url in urls:
        try:
            response = requests.get(url)
            doc = BeautifulSoup(response.content, "html.parser")
            elements = doc.select("div.listing__item")
            properties.update(scrape_property_argenprop(e) for e in elements)
        except Exception as e:
            print(f"Error reading URL. Error message: {str(e)}")

    return properties