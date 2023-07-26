import re

def to_number(s):
    number = re.sub(r'[^0-9]', '', s)
    try: return int(number)
    except ValueError: return 0