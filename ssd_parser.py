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
    
def getSSDName(soup):
    raw_name_data = soup.find_all('a')
    name_data_table = [val.text.strip() for val in raw_name_data]
    name_data = []
    for value in name_data_table:
        if(value != ''):
            name_data.append(value)
    del name_data[0:14]
    del name_data[-6:]
    return name_data

def getSSDBenchmark(soup):
    green_benchmark_data = soup.find_all('td', class_ = "text-success")
    green_benchmark_data_table = [val.text.strip() for val in green_benchmark_data]
    
    green_data = []
    for val in green_benchmark_data_table:
        if(val != '✓ Yes' and '$' not in val and val != 'MLC'):
            green_data.append(val)

    yellow_benchmark_data = soup.find_all('td', class_ = "text-warning")
    yellow_benchmark_data_table = [val.text.strip() for val in yellow_benchmark_data]
    
    yellow_data = []
    for val in yellow_benchmark_data_table:
        if(val != '✓ Yes' and '$' not in val ):
            yellow_data.append(val)
    
    red_benchmark_data = soup.find_all('td', class_ = "text-danger")
    red_benchmark_data_table = [val.text.strip() for val in red_benchmark_data]
    red_data = []
    for val in red_benchmark_data_table:
        if(val != 'No' and '$' not in val and val != 'QLC' ):
            red_data.append(val)
    benchmark_data = green_data + yellow_data +red_data
    return benchmark_data
    
def getSSDPrice(soup):
    price_data = soup.find_all('td')
    price_data_table = [val.text.strip() for val in price_data]
    cleaned_data = []
    for value in price_data_table:
        if('$' in value):
            cleaned_val = value.replace('\xa0','')
            cleaned_data.append(cleaned_val)

    final_price_data = []
    
    for i in range(len(cleaned_data)):
        if(i%2 == 0):
            final_price_data.append(cleaned_data[i][:-1])

    return final_price_data 

def combineData(names, benchmarks,prices):
    cpudata = []
    for i in range(len(names)):
        temp = [names[i],benchmarks[i],prices[i]]
        cpudata.append(temp)
    
    return cpudata

def writeCSV(cpudata):
    with open('ssddata.csv', 'w') as cpufile:
        writer = csv.writer(cpufile, delimiter=',')
        writer.writerow(["CPU Name", "Benchmark Score", "Price"]) 
        writer.writerows(cpudata)



def main():
    url = "https://ssd-tester.com/top_ssd.php"
    soup = getPage(url)
    if(not soup):
        print("Can not access the page!")
    else:
        names = getSSDName(soup)
        benchmarks = getSSDBenchmark(soup)
        prices = getSSDPrice(soup)
        
        ssddata = combineData(names,benchmarks,prices)
        writeCSV(ssddata)


if __name__ == "__main__":
    main()