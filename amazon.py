from bs4 import BeautifulSoup
import requests


class Amazon:

    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    data = None
    productUrlList = []



    def GetProductName(self):
        pass

    def GetProductPrice(self):
        pass

    def GetProductRating(self):
        pass

    def SearchProduct(self, productName):
        searchUrl = "https://www.amazon.com.tr/s?k="

        try:
            reqData = requests.get((searchUrl + productName), headers=self.HEADERS)

            if reqData.status_code == 200:

                # Clear prev data
                self.data = None

                bs = BeautifulSoup(reqData.content, 'html.parser')

                getProductUrl = bs.find_all('a', attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

                for product in getProductUrl:
                    print(("https://www.amazon.com.tr" + product.get('href')))
                    self.productUrlList.append(("https://www.amazon.com.tr" + product.get('href')))

                print(f"Product List Added's")


            else:
                print("Error data is not requested, check headers")
        except requests.exceptions.RequestException as reqExp:
            print("Error, request is failed !\n")
            print(reqExp.response)

    def UIMenu(self):
        pass


app = Amazon()
app.SearchProduct("iPhone 11")