from bs4 import BeautifulSoup
import requests

# Test
def collectComputer():
    
    productNames = []
    productPrices = []
    url = "https://www.amazon.com/s?rh=n%3A565108%2Cp_72%3A4-&content-id=amzn1.sym.16e37646-73e5-411d-be1c-663080c0b9df&pd_rd_r=e27ee2c7-08d2-490b-812a-270edcc28d25&pd_rd_w=N0GEV&pd_rd_wg=zh0Rt&pf_rd_p=16e37646-73e5-411d-be1c-663080c0b9df&pf_rd_r=P2RARVEW10TAR0YVMAJH&ref=Oct_d_otopr_S"

    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }

    html = requests.get(url, headers=HEADERS)

    bsParser = BeautifulSoup(html.content, 'html.parser')

    productsList = bsParser.find_all('div', attrs={'class': 'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'})

    productPrices.clear()
    productNames.clear()
    for data in productsList:
        bsContent = BeautifulSoup(str(data), 'html.parser')
        
        for productUrl in bsContent.find_all("a", attrs={'class':'a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal'}):
            print(f"Product Name : 'https://www.amazon.com{productUrl.get('href')}\n\t")
            # productNames.append(productName.href)




def ProductName(data):
    bs = BeautifulSoup(data, 'html.parser')
    pName = bs.find('span', attrs={'class':'a-size-large product-title-word-break'}).getText().strip()

    return pName

def ProductPrice(data):
    bs = BeautifulSoup(data, 'html.parser')
    pPrice = bs.find('span', attrs={'class': 'a-price-whole'}).getText().strip().replace(',', " TL")
    return pPrice

def ProductRating(data):
    bs = BeautifulSoup(data, 'html.parser')
    pRating = bs.find('span', attrs={'class': 'a-icon-alt'}).getText().strip()
    return pRating.replace('yıldız üzerinden', "-").strip()
def TestOne():
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/44.0.2403.157 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    getPage = requests.get("https://www.amazon.com.tr/Samsung-SM-A525F-Galaxy-Ak%C4%B1ll%C4%B1-Telefon/dp/B093QC5HGK/ref=sr_1_203?keywords=iPhone%2B11&qid=1688593223&sr=8-203&th=1", headers=HEADERS)

    if getPage.status_code == 200:
        print("Request OK !")

        pName = ProductName(getPage.content)
        pPrice = ProductPrice(getPage.content)
        pRating = ProductRating(getPage.content)

        print("----------------------------------------------------------------------------------------------------------------------------")
        print(f"Product Name :{pName}\n\bProduct Price: {pPrice}\n\bProduct Rating :{pRating}")
        print("----------------------------------------------------------------------------------------------------------------------------")




TestOne()