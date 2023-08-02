from scraper import zonaprop,mercadolibre,argenprop
from database import PropertyDatabase
from scraper.property import Property
from scraper.enums import Currency, Page, PropertyType

import logging
import time

# Define the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def main():
    db = PropertyDatabase()
    properties = set()

    #properties.update(zonaprop.get_rent_properties_caba())
    properties.update(mercadolibre.get_rent_properties_caba())
    #properties.update(argenprop.get_rent_properties_caba())

    db_properties = db.get_properties()
    # Get a set of URLs from the list of tuples db_properties
    existing_urls = {url for _, url in db_properties}
    start_time = time.time()
    inserteds = 0
    updateds = 0

    for property in properties:
        if property.url not in existing_urls:
            db.insert_property(property)
            inserteds += 1
        else:
            db.update_property_last_read_date(property.url)
            updateds += 1

    elapsed_time = time.time() - start_time
    logger.info(f"Time taken to update the database: {elapsed_time:.2f} seconds for {len(properties)} properties")
    logger.info(f"There were {inserteds} new properties and {updateds} updated properties")

    db.delete_inactive_properties()



if __name__ == "__main__":
    main()