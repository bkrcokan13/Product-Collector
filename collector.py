from bs4 import BeautifulSoup
import requests
import json


def getStoreProduct():
    try:
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
            pass
        else:
            # Zip two list and create dict
            productDict = dict(zip(productsNames, productPrices))

            # Dump file Json
            with open("result.json", 'w', encoding='utf8') as createJson:
                json.dump(productDict, createJson, ensure_ascii=False)
                print("Json file created")
    except Exception:
        print("Error, products data not fetched !")


getStoreProduct()
