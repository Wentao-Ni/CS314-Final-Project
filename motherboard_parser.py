from bs4 import BeautifulSoup
import requests
import csv 

def getPage(url):
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"} 
    data = requests.get(url, headers=HEADERS)
    if(data.status_code == 200):
        soup = BeautifulSoup(data.text,'lxml')
        return soup
    else:
        return 

def getMotherboardScore(soup):
    raw_name_data = soup.find_all(class_ = "pointsText")
    name_data_table = [val.text.strip() for val in raw_name_data]
    name_data = []
    for val in name_data_table:
        name_data.append(val[0:2])
    
    return name_data

def getMotherboardName(soup):
    motherboard_name = soup.find_all(class_ = "BarsItem__name___My7de")
    motherboard_name_table = [name.text.strip() for name in motherboard_name]
    return motherboard_name_table

def getMotherboardPrice(soup):
    motherboard_price = soup.find_all(class_ = "BarsItem__price___W1Vjm")
    motherboard_price_table = [price.text.strip() for price in motherboard_price]
    result = []
    for val in motherboard_price_table:
        val = val[1:]
        if(',' in val):
            temp = val[:1] + val[2:]
            result.append(temp)
        else:
            result.append(val)
    return len(result)

def main():
    #TODO: iterate through the pages to get the full list of the motherboard information
    url = "https://versus.com/en/motherboard?page=7&sort=priceHighest"
    soup = getPage(url)
    if(not soup):
        print("Can not access the page!")
    else:
        print(getMotherboardName(soup))

if __name__ == "__main__":
    main()