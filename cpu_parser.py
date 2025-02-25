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

def getCPUName(soup):
    cpu_name = soup.find_all('a', class_='OneLinkNoTx')
    cpu_name_table = [name.text.strip() for name in cpu_name]
    return cpu_name_table


def getCPUBenchmark(soup):
    cpu_benchmark = soup.find_all(class_ = "bar-holder performance")
    cpu_benchmark_table = [benchmark.text.strip() for benchmark in cpu_benchmark]
    return cpu_benchmark_table

def getCPUPrice(soup):
    cpu_price = soup.find_all(class_ = 'list-tiny-none')
    cpu_price_table = [price.text.strip() for price in cpu_price]
    cpu_price_table.pop(0)
    return cpu_price_table

def combineData(names, benchmarks,prices):
    cpudata = []
    for i in range(len(names)):
        temp = [names[i],benchmarks[i],prices[i]]
        cpudata.append(temp)
    
    return cpudata


def writeCSV(cpudata):
    with open('cpudata.csv', 'w') as cpufile:
        writer = csv.writer(cpufile, delimiter=',')
        writer.writerow(["CPU Name", "Benchmark Score", "Price"]) 
        writer.writerows(cpudata)
    

def main():
    url = "https://benchmarks.ul.com/compare/best-cpus"
    soup = getPage(url)
    if(not soup):
        print("Can not access the page!")
    else:
        names = getCPUName(soup)
        benchmarks = getCPUBenchmark(soup)
        prices = getCPUPrice(soup)

        cpudata = combineData(names,benchmarks,prices)
        writeCSV(cpudata)

if __name__ == '__main__':
    main()