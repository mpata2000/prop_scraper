import re

NEIGHBORHOODS_CABA = [
        "Agronomia", "Almagro", "Balvanera", "Barracas", "Belgrano", "Boedo", "Caballito",
        "Chacarita", "Coghlan", "Colegiales", "Constitucion", "Flores", "Floresta", "La%20Boca",
        "La%20Paternal", "Liniers", "Mataderos", "Monte%20Castro", "Monserrat", "Nueva%20Pompeya",
        "Nunez", "Palermo", "Parque%20Avellaneda", "Parque%20Chacabuco", "Parque%20Chas",
        "Parque%20Patricios", "Puerto%20Madero", "Recoleta", "Retiro", "Saavedra", "San%20Cristobal",
        "San%20Nicolas", "San%20Telmo", "Velez%20Sarsfield", "Versalles", "Villa%20Crespo",
        "Villa%20del%20Parque", "Villa%20Devoto", "Villa%20General%20Mitre", "Villa%20Lugano",
        "Villa%20Luro", "Villa%20Ortuzar", "Villa%20Pueyrredon", "Villa%20Real", "Villa%20Riachuelo",
        "Villa%20Santa%20Rita", "Villa%20Soldati", "Villa%20Urquiza"
    ]


def to_number(str:str):
    try: return int(re.sub(r'[^0-9]', '', str))
    except: return 0

# Split a list into chunks of the given size
# @return list of chunks
def chunks(input_list: list, chunk_size: int):
    return [input_list[i:i+chunk_size] for i in range(0, len(input_list), chunk_size)]
