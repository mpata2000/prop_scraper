from enum import Enum


class Currency(Enum):
    ARS = "ARS"
    USD = "USD"

    @staticmethod
    def from_str(s):
        upper_s = s.upper()
        if upper_s in ["USD", "U$S", "DOLARES", "DÓLARES"]:
            return Currency.USD
        return Currency.ARS
