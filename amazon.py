from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime


class Amazon:

    # TODO: 1-Add More Country(OK) ,2-Add Curency Converter, 3-Add Extractor(JSON, CSV) 4-Improve UI and create more funcable menu
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }

    # Testing only 4 country
    CountryUrls = {
        'us': 'https://www.amazon.com/s?k=',
        'nl': 'https://www.amazon.nl/s?k=',
        'de': 'https://www.amazon.de/s?k=',
        'ae': 'https://www.amazon.ae/s?k=',
        'tr': 'https://www.amazon.com.tr/s?k='
    }
    data = None

    # Collected Product List
    productUrlList = []

    # Transfer BS Method and Create Object
    productBs = None
    selectedCountry = None
    currencyRates = None

    def __init__(self):
        self.GetCurrencyRate()

    # Get Currency Rates

    def GetCurrencyRate(self):
        headerBanner = """
                         _                                      ____      _ _           _             
                        / \   _ __ ___   __ _ _______  _ __    / ___|___ | | | ___  ___| |_ ___  _ __ 
                       / _ \ | '_ ` _ \ / _` |_  / _ \| '_ \  | |   / _ \| | |/ _ \/ __| __/ _ \| '__|
                      / ___ \| | | | | | (_| |/ / (_) | | | | | |__| (_) | | |  __/ (__| || (_) | |   
                     /_/   \_\_| |_| |_|\__,_/___\___/|_| |_|  \____\___/|_|_|\___|\___|\__\___/|_|   """

        print(headerBanner + "\n")

        # Count Country
        countCountry = 0

        # Country List Temp
        countryList = {}

        # Clear Country Dict
        countryList.clear()

        # API Url
        baseApi = "https://v6.exchangerate-api.com/v6/d654e61f7e5398a2d6ae3a9a/latest/"

        currencyAPI = ""

        print("---------------Available Country List-----------------")

        # List Available County
        for country in self.CountryUrls.keys():
            countCountry += 1
            print(f"{countCountry} - {country.upper()}")

            # Add Available Country List
            countryList[countCountry] = country.upper()

        selectCountry = str(input("Select Your Country : "))

        if selectCountry == "1":
            currencyAPI = baseApi + "USD"
            self.selectedCountry = "US"
            print(f"Info: Selected country {self.selectedCountry}")

        elif selectCountry == "2" or selectCountry == "3":
            currencyAPI = baseApi + "EUR"

        if selectCountry == "2":
            self.selectedCountry = "NL"
            print(f"Info: Selected country {self.selectedCountry}")

        elif selectCountry == "3":
            self.selectedCountry = "DE"
            print(f"Info: Selected country {self.selectedCountry}")

        elif selectCountry == "4":
            currencyAPI = baseApi + "AED"
            
            self.selectedCountry = "UAE"
            print(f"Info: Selected country {self.selectedCountry}")

        elif selectCountry == "5":
            currencyAPI = baseApi + "TRY"
            self.selectedCountry = "TR"
            print(f"Info: Selected country {self.selectedCountry}")

        elif int(selectCountry) >= countCountry:
            print(f"Error: Country not found, please try again !")

        getCurrency = requests.get(currencyAPI)

        if getCurrency.status_code == 200:
            # Extract rates
            self.currencyRates = dict(getCurrency.json()['conversion_rates'])

            nowTime = datetime.now()
            print(f"Info: Currency rates fetched.{nowTime.strftime('%H:%M:%S')}")

            print(self.currencyRates.keys())
        elif getCurrency.status_code == 404:
            print("Error: Country not found !")

      

    # Get Product Name

    def GetProductName(self):

        getName = self.productBs.find('span',
                                      attrs={'class': 'a-size-large product-title-word-break'}).getText().strip()
        if getName is None or "":
            return ""
        else:
            return getName

    # Get Product Price
    def GetProductPrice(self):

        getPrice = self.productBs.find('span',
                                       attrs={'class': 'a-price-whole'}).getText().strip().replace(",", "")
        if getPrice is None or "":
            return ""
        else:
            return getPrice + " TL"

    # Get Product Rating Rate
    def GetProductRating(self):
        getRating = self.productBs.find('span',
                                        attrs={'class': 'a-icon-alt'}).getText().strip()
        if getRating is None or "":
            return ""
        else:
            return getRating

    def SearchProduct(self, productName):

        # Only country TR
        searchUrl = "https://www.amazon.com.tr/s?k="

        try:
            # Collect all url's
            reqData = requests.get(
                (searchUrl + productName), headers=self.HEADERS)

            # Check website return code
            if reqData.status_code == 200:

                bs = BeautifulSoup(reqData.content, 'html.parser')

                getProductUrl = bs.find_all('a', attrs={
                    'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

                # Clear list for new search
                self.productUrlList.clear()
                for product in getProductUrl:
                    self.productUrlList.append(
                        ("https://www.amazon.com.tr" + product.get('href')))

                # TODO: Fix url counter, 47 product found but showed 60 ! This is a problem dude ! :)
                print(f"Info : {len(self.productUrlList)} Products Founded ")
                print(f"Warning: Items will be collected 1.5 second delays!")
                print("\n")

                # Check list status
                if len(self.productUrlList) != 0:

                    productCount = 0

                    for datas in self.productUrlList:
                        productData = requests.get(datas, headers=self.HEADERS)
                        time.sleep(1.5)

                        if productData.status_code == 200:
                            try:
                                self.productBs = BeautifulSoup(
                                    productData.content, 'html.parser')
                                pName = self.GetProductName()
                                pPrice = self.GetProductPrice()

                                pRating = self.GetProductRating()
                                pUrl = datas
                                productCount += 1

                                print(
                                    f"{productCount}-Product Name :{pName}\n\tProduct Price : {pPrice}\n\tProduct Rating: {pRating}\n\tProduct Url :{pUrl}\n")
                            except Exception as exp:

                                # Catch error and fix !
                                print("Error, product info not getting : " + datas)
                                break

                        else:
                            print(
                                "Error, product page is not available or reachable, check Headers !")
                            break
            else:
                print(reqData.status_code)
                print("Error data is not requested, check headers")
        except requests.exceptions.RequestException as reqExp:
            print("Error, request is failed !\n")
            print(reqExp.response)

    def UIMenu(self):
        while True:
            try:
                headerBanner = """
                         _                                      ____      _ _           _             
                        / \   _ __ ___   __ _ _______  _ __    / ___|___ | | | ___  ___| |_ ___  _ __ 
                       / _ \ | '_ ` _ \ / _` |_  / _ \| '_ \  | |   / _ \| | |/ _ \/ __| __/ _ \| '__|
                      / ___ \| | | | | | (_| |/ / (_) | | | | | |__| (_) | | |  __/ (__| || (_) | |   
                     /_/   \_\_| |_| |_|\__,_/___\___/|_| |_|  \____\___/|_|_|\___|\___|\__\___/|_|   """

                print(headerBanner + "\n")
                print(f"--> Selected Country : {self.selectedCountry} ")

                cmds = str(input("Enter_Product:"))

                if cmds is None:
                    pass
                else:
                    print("Colector starting .... !")
                    self.SearchProduct(productName=cmds)
            except:
                print("Error, wrong command !")
                break


# Initalize app
app = Amazon()
app.UIMenu()
