from scraper.enums.propertyType import PropertyType
from scraper.enums.currency import Currency
from scraper.enums.page import Page

class Property:
    def __init__(
        self,
        url="",
        prop_type=PropertyType.DEPARTMENT,
        price=0,
        currency=Currency.ARS,
        expenses=0,
        total_area=0,
        covered_area=0,
        rooms=0,
        bedrooms=0,
        bathrooms=0,
        address="",
        neighborhood="",
        garage=0,
        page=Page.ZONAPROP,
        pics_urls:list[str]=[]
    ):
        self.url: str = url
        self.prop_type: PropertyType = prop_type
        self.price: int = price
        self.currency: Currency = currency
        self.expenses: int = expenses
        self.total_area: int = total_area
        self.covered_area: int = covered_area
        self.rooms: int = rooms
        self.bedrooms: int = bedrooms
        self.bathrooms: int = bathrooms
        self.address: int = address
        self.neighborhood: int = neighborhood
        self.garage: int = garage
        self.page: Page = page
        self.images: list[str] = pics_urls

    def __eq__(self, other):
        if not isinstance(other, Property):
            return False
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)
    
    def setPropertyType(self,str):
        self.prop_type = PropertyType.from_str(str)

    def set_currency(self, str):
        self.currency = Currency.from_str(str)

    def set_property_type(self, str):
        self.prop_type = PropertyType.from_str(str)
