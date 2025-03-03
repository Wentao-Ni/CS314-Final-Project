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
    return result

def getMotherboardBrand(soup):
    motherboard_name = soup.find_all(class_ = "BarsItem__name___My7de")
    motherboard_name_table = [name.text.strip() for name in motherboard_name]
    brand_list = []
    for name in motherboard_name_table:
        brand = name.split()[0]
        brand_list.append(brand)
    return brand_list

def flatList(two_d_list):
    result = []
    for one_d_list in two_d_list:
        for val in one_d_list:
            result.append(val)

    return result

def combineDataData(name, brand, score,price):
    final = []
    for i in range(len(name)):
        temp = [name[i],brand[i],score[i],price[i]]
        final.append(temp)
    return final

def writeCSV(motherboarddata):
    with open('motherboarddata.csv', 'w') as cpufile:
        writer = csv.writer(cpufile, delimiter=',')
        writer.writerow(["Motherboard Name","Brand" "Score", "Price"]) 
        writer.writerows(motherboarddata)
    
    
def main():
    bast_url = "https://versus.com/en/motherboard?page={}&sort=priceHighest"
    names = []
    prices = []
    brands = []
    scores = []
    for page in range(1,8):
        cur_url = bast_url.format(page)
        soup = getPage(cur_url)
        if(not soup):
            print("Can not access the page!")
        else:
            prices.append(getMotherboardPrice(soup))
            names.append(getMotherboardName(soup))
            brands.append(getMotherboardBrand(soup))
            scores.append(getMotherboardScore(soup))
    
    brands = flatList(brands)
    names = flatList(names)
    prices = flatList(prices)
    scores = flatList(scores)
    motherboard_data = combineDataData(names,brands,scores,prices)
    writeCSV(motherboard_data)
if __name__ == "__main__":
    main()