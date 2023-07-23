import requests
import json
import gzip
import brotli

def mercadolibre():
    url = "https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&limit=50&offset=0"
