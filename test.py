from bs4 import BeautifulSoup
import requests
import json


def getStoreProduct():
    try:
        # Product List
        productsNames = []
        productPrices = []

        # Clear all lists
        productsNames.clear()
        productPrices.clear()

        # Request website
        storeUrl = "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/"
        reqStore = requests.get(storeUrl)

        # BS4 parser
        bsParser = BeautifulSoup(reqStore.content, 'html.parser')

        # Get all product nodes
        products = bsParser.find(
            'div', attrs={'class': 'wrapper-product wrapper-product--list-page clearfix'})

        # Get product content
        for productName in products.find_all('div', attrs={'class': 'product-list__content'}):
            productsNames.append(productName.h3.text)

        for productPrice in products.find_all('span', attrs={'class': 'product-list__price'}):
            productPrices.append(str(productPrice.text + "TL"))

        # Check list length
        if len(productsNames) and len(productPrices) == 0:
            print("Warring, products list is empty !!")
        else:
            # Zip two list and create dict
            productDict = dict(zip(productsNames, productPrices))

            # Dump file Json
            with open("result.json", 'w', encoding='utf8') as createJson:
                json.dump(productDict, createJson, ensure_ascii=False)
                print("Json file created")
    except Exception:
        print("Error, products data not fetched !")


def CountryCodes():
    apiUrl = "https://v6.exchangerate-api.com/v6/d654e61f7e5398a2d6ae3a9a/latest/TRY"
    getCountry = requests.get(apiUrl)

    data = getCountry.json()

    rates = dict(data['conversion_rates'])

    for value in rates.keys():
        if value != "TRY":
            print(f"{value}:{round(rates[value] * 7500, 3)}\n")

    
    
   

CountryCodes()
