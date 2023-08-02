from scraper import zonaprop,mercadolibre,argenprop
from database import insert_property,delete_inactive_properties,get_properties
from scraper.property import Property
from scraper.enums import Currency, Page, PropertyType

#argenprop.get_rent_properties_caba()
prop = Property(url="test",prop_type=PropertyType.DEPARTMENT,price=1000,currency=Currency.ARS,expenses=5,total_area=3,covered_area=2,rooms=0,bedrooms=0,bathrooms=6,address="Guido 300",neighborhood="Belgrano",garage=0,page=Page.ARGENPROP,pics_urls="[]")
#insert_property(prop)
#delete_inactive_properties()
get_properties()
#zonaprop.get_rent_properties_caba()
#mercadolibre.get_rent_properties_caba()
