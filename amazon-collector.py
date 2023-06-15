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
        
          
collectComputer()
