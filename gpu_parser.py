from bs4 import BeautifulSoup
import requests
import csv 

def getPage(url):
    data = requests.get(url)
    if(data.status_code == 200):
        soup = BeautifulSoup(data.text,'lxml')
        return soup
    else:
        return 

def getGPUName(soup):
    gpu_name = soup.find_all('a', class_='OneLinkNoTx')
    gpu_name_table = [name.text.strip() for name in gpu_name]
    return gpu_name_table


def getGPUBenchmark(soup):
    gpu_benchmark = soup.find_all(class_ = "bar-holder performance")
    gpu_benchmark_table = [benchmark.text.strip() for benchmark in gpu_benchmark]
    return gpu_benchmark_table

def getGPUPrice(soup):
    gpu_price = soup.find_all(class_ = 'list-tiny-none')
    gpu_price_table = [price.text.strip() for price in gpu_price]
    gpu_price_table.pop(0)
    return gpu_price_table

def getGPUBrand(names):
    brand_list = []
    for name in names:
        brand = name.split()[0]
        brand_list.append(brand)
    return brand_list

def combineData(names, brand,benchmarks,prices):
    gpudata = []
    for i in range(len(names)):
        temp = [names[i],brand[i],benchmarks[i],prices[i]]
        gpudata.append(temp)
    
    return gpudata



def writeCSV(gpudata):
    with open('gpudata.csv', 'w') as gpufile:
        writer = csv.writer(gpufile, delimiter=',')
        writer.writerow(["GPU Name", "Benchmark Score", "Price"]) 
        writer.writerows(gpudata)
    

def main():
    url = "https://benchmarks.ul.com/compare/best-gpus"
    soup = getPage(url)
    if(not soup):
        print("Can not access the page!")
    else:
        names = getGPUName(soup)
        benchmarks = getGPUBenchmark(soup)
        prices = getGPUPrice(soup)
        brands = getGPUBrand(names)
        gpudata = combineData(names,brands,benchmarks,prices)
        writeCSV(gpudata)

if __name__ == '__main__':
    main()