import requests
import json
import gzip
import brotli

def zonaprop():
    url = "https://www.zonaprop.com.ar/rplis-api/postings"
    with open('./scraper/resources/zonapropRequest.json') as file:
        file_contents = file.read()
    requestJson = json.loads(file_contents)
    headers = {
        'Accept':'*/*',
        "Cookie":"__cf_bm=k_v7.SKHIdCK2dH_DfbdEmzxrFcQpB4RPSi7gY1a3JQ-1689988470-0-AdOD9mBfkMGtemxV13QXsGZ7JjOHovLuktDXUSsUFoj+VsvFSuGfvECa7ZeMmug2ZJvXjHsxbm6hAgMO6Kd36hFDunU4kNWb1Iaa9bxJydy1; JSESSIONID=B8843FB2163A2E1D138248EC6B9136C2",
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'es-AR,es-US;q=0.9,es;q=0.8,en-US;q=0.7,en;q=0.6,es-419;q=0.5',
        'Content-Length':'940',
        'Content-Type':'application/json',
        'User-Agent':'PostmanRuntime/7.30.0',
        'Connection':'keep-alive',
        'Cache-Control':'no-cache',
        'Host':'www.zonaprop.com.ar',
         }
    response = requests.post(url,json=requestJson ,headers=headers)
    print(response.status_code)
    print(response.json())
