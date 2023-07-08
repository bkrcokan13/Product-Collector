from bs4 import BeautifulSoup
import requests
import time


class Amazon:
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    data = None
    productUrlList = []

    productBs = None

    def GetProductName(self):

        getName = self.productBs.find('span',
                                      attrs={'class': 'a-size-large product-title-word-break'}).getText().strip()
        if getName is None or "":
            return ""
        else:
            return getName

    def GetProductPrice(self):

        getPrice = self.productBs.find('span',
                                       attrs={'class': 'a-price-whole'}).getText().strip().replace(",", "")
        if getPrice is None or "":
            return ""
        else:
            return "TL " + getPrice

    def GetProductRating(self):
        getRating = self.productBs.find('span',
                                        attrs={'class': 'a-icon-alt'}).getText().strip()
        if getRating is None or "":
            return ""
        else:
            return getRating

    def SearchProduct(self, productName):
        searchUrl = "https://www.amazon.com.tr/s?k="

        try:
            reqData = requests.get((searchUrl + productName), headers=self.HEADERS)

            if reqData.status_code == 200:

                # Clear prev data
                self.data = None

                bs = BeautifulSoup(reqData.content, 'html.parser')

                getProductUrl = bs.find_all('a', attrs={
                    'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

                for product in getProductUrl:
                    self.productUrlList.append(("https://www.amazon.com.tr" + product.get('href')))

                print("Info : Product urls collected !")

                if len(self.productUrlList) != 0:
                    for datas in self.productUrlList:
                        productData = requests.get(datas, headers=self.HEADERS)

                        if productData.status_code == 200:
                            try:
                                self.productBs = BeautifulSoup(productData.content, 'html.parser')
                                pName = self.GetProductName()
                                pPrice = self.GetProductPrice()

                                pRating = self.GetProductRating()
                                pUrl = datas

                                print(
                                    f"Product Name :{pName}\nProduct Price : {pPrice}\n Product Rating: {pRating}\n Product Url : {pUrl}\n")
                            except Exception as exp:
                                pass


                        else:
                            print("Error, product page is not available or reachable, check Headers !")
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

                print(headerBanner)

                cmds = str(input(">>"))

                if cmds is None:
                    pass
                else:
                    print("Colector starting .... !")
                    self.SearchProduct(productName=cmds)
            except:
                print("Error, wrong command !")
                break


app = Amazon()
app.UIMenu()
