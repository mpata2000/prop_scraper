import requests
import json
import gzip
import brotli
import urllib


from scraper.enums import PropertyType, Currency, Page

ZONAPROP_API = "https://www.zonaprop.com.ar/rplis-api/postings"
HEADERS = {
        'Content-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept':'*/*',
        'Cache-Control':'no-cache',
        'Accept-Encoding':'gzip, deflate, br',
        'Host':'www.zonaprop.com.ar',
        'Connection':'keep-alive'
         }

def get_cookies():

    url = "https://www.zonaprop.com.ar/rplis-api/postings"

    payload = json.dumps({
      "q": None,
      "direccion": None,
      "moneda": None,
      "preciomin": None,
      "preciomax": None,
      "services": "",
      "general": "",
      "searchbykeyword": "",
      "amenidades": "",
      "caracteristicasprop": None,
      "comodidades": "",
      "disposicion": None,
      "roomType": "",
      "outside": "",
      "areaPrivativa": "",
      "areaComun": "",
      "multipleRets": "",
      "tipoDePropiedad": "1,2,2001",
      "subtipoDePropiedad": None,
      "tipoDeOperacion": "2",
      "garages": None,
      "antiguedad": None,
      "expensasminimo": None,
      "expensasmaximo": None,
      "habitacionesminimo": 0,
      "habitacionesmaximo": 0,
      "ambientesminimo": 0,
      "ambientesmaximo": 0,
      "banos": None,
      "superficieCubierta": 1,
      "idunidaddemedida": 1,
      "metroscuadradomin": None,
      "metroscuadradomax": None,
      "tipoAnunciante": "ALL",
      "grupoTipoDeMultimedia": "",
      "publicacion": None,
      "sort": "relevance",
      "etapaDeDesarrollo": "",
      "auctions": None,
      "polygonApplied": None,
      "idInmobiliaria": None,
      "excludePostingContacted": "",
      "banks": "",
      "pagina": 4,
      "city": None,
      "province": "6",
      "zone": None,
      "valueZone": None,
      "subZone": None,
      "coordenates": None
    })
    headers = {
      'Content-Type': 'application/json'
    }


    response = requests.request("POST", url, headers=headers, data=payload, proxies=urllib.request.getproxies())

    print(response.text)

    return response.cookies

def get_response(pageNumber,cookies):
    with open('./scraper/resources/zonapropRequest.json') as file:
        file_contents = file.read()
    requestJson = json.loads(file_contents)
    requestJson["pagina"] = pageNumber

    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-AR,es-US;q=0.9,es;q=0.8,en-US;q=0.7,en;q=0.6,es-419;q=0.5',
        'Content-Type':'application/json',
        'User-Agent':'PostmanRuntime/7.30.0',
        'Postman-Token': 'ca67ce84-f171-4fb3-a5b8-5c5f1a848b37',
        'Connection':'keep-alive',
        'Cache-Control':'no-cache',
        'Host':'www.zonaprop.com.ar'
         }
    response = requests.post(ZONAPROP_API,json=requestJson ,headers=HEADERS,cookies=cookies.get_dict())
    return response


def zonaprop():
    cookies = get_cookies()
    test = cookies.get_dict()
    print(test)
    page = 1
    totalPages = 1
    #while page <= totalPages:
       #response = get_response(page,cookies).json()
        #totalPages = response["paging"]["totalPages"]
