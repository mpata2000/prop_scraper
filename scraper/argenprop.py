
from bs4 import BeautifulSoup
import cloudscraper
import json
import logging
import time
import traceback
from .enums import Page
from .property import Property
from .utils import to_number

URL_ARGENPROP="https://www.argenprop.com"
logger = logging.getLogger()


def scrape_property_argenprop(element):
    property = Property(page=Page.ARGENPROP)

    property.url = URL_ARGENPROP + element.find('a')['href']
    property.setPropertyType(property.url.split("/")[3].split("-")[0])

    card_price = element.select_one('p.card__price')
    if card_price.select_one('.card__noprice') is None:
        property.set_currency(card_price.select_one('.card__currency').text.strip())
        property.price = to_number(card_price.contents[2])

    property.address = element.select_one('.card__address').get_text().strip()
    property.neighborhood = element.select('.card__title--primary')[-1].get_text().split(",")[0].upper()
    property.expenses = to_number(element.select_one('.card__expenses').get_text()) if element.select_one('.card__expenses') else 0


    # Extract the URLs of the images
    property.pics_urls = [img["data-src"] for img in element.select("ul.card__photos li img[data-src]") if img["data-src"]]


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

    return property

def get_rent_properties_caba():
    start_time = time.time()
    properties = set()
    scraper = cloudscraper.create_scraper()
    url = URL_ARGENPROP + "/departamento-y-casa-alquiler-localidad-capital-federal"
    while url != "":
        try:
            response = scraper.get(url)
            doc = BeautifulSoup(response.content, "html.parser")
            elements = doc.select("div.listing__item")
            properties.update(scrape_property_argenprop(e) for e in elements)
            url = (URL_ARGENPROP+doc.select_one(".pagination__page-next>a")["href"]) if doc.select_one(".pagination__page-next>a") else ""
        except Exception as e:
            logger.error(f"Error getting response from Argenprop at {url} : {e}")
            logger.error(traceback.format_exc())

    elapsed_time = time.time() - start_time
    logger.info(f"Time taken to get properties from Argenprop: {elapsed_time:.2f} seconds for {len(properties)} properties")
    return properties
