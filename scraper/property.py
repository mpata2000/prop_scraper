from scraper.enums.propertyType import PropertyType
from scraper.enums.currency import Currency
from scraper.enums.page import Page

class Property:
    def __init__(
        self,
        url="",
        title="",
        description="",
        prop_type=PropertyType.DEPARTMENT,
        price=0,
        currency=Currency.ARS,
        expenses=0,
        totalArea=0,
        coveredArea=0,
        rooms=0,
        bedrooms=0,
        bathrooms=0,
        address="",
        neighborhood="",
        garage=0,
        page=Page.ZONAPROP
    ):
        self.url = url
        self.title = title
        self.description = description
        self.prop_type = prop_type
        self.price = price
        self.currency = currency
        self.expenses = expenses
        self.total_area = totalArea
        self.covered_area = coveredArea
        self.rooms = rooms
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.address = address
        self.neighborhood = neighborhood
        self.garage = garage
        self.page = page
        # TODO: add list of images url

    def __eq__(self, other):
        if not isinstance(other, Property):
            return False
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)
