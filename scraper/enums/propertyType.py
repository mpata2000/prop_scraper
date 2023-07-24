from enum import Enum

class PropertyType(Enum):
    DEPARTMENT = "DEPARTAMENTO"
    HOUSE = "CASA"
    PH = "PH"

    @staticmethod
    def from_str(str):
        str = str.upper()
  
        if str == "CASA":
            return PropertyType.HOUSE
        elif str == "PH":
            return PropertyType.PH
        
        return PropertyType.DEPARTMENT