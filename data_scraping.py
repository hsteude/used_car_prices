'''
Idea:
This script generates a data frame containing all the information
on 911er offers on the "autoscout24" website. This data frame is saved to
a hdf5 file with the current timestamp in the file name.
'''


## import libraries for scarping
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

def create_links():
    '''
    Creates all the links necessary to scrape all the offerings
    (i.e. page 1-20 of all possible soring options)
    Outputs a list of srings (links)
    '''
    links = []
    for k in range(1,21):
        links.append([
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=standard&desc=0&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&'
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=price&desc=0&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=price&desc=1&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=financerate&desc=0&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=financerate&desc=1&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=age&desc=1&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=mileage&desc=0&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=mileage&desc=1&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=power&desc=0&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=power&desc=1&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=year&desc=0&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&',
        'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=year&desc=1&ustate=N%2CU&size=20&page='+str(k)+'&atype=C&'
        ])
    links = [item for sublist in links for item in sublist]
    return links


def car_table_from_quote_page(quote_page):
    '''
    Generates a dataframe containing all the information of the offerings
    available from the summary pages (the parsed html)
    '''
    #download html and generate BuautifulSoup object
    response = requests.get(quote_page)
    soup = BeautifulSoup(response.content, "html.parser")
    offerings = soup.findAll("div", {"data-item-name": "listing-summary-container"})

    #read relevant information from BeautifulSoup object and clean data
    id = []
    headline = []
    price = []
    details = []
    for offering in offerings:
        id.append(offering['id'])
        headline.append(offering.find('div',{'data-item-name':'headline'}).text)
        price.append(offering.find('span',{'data-item-name':'price'}).text)
        details.append(offering.find('ul',{'data-item-name':'vehicle-details'}).text)
    headline = list(map(lambda x: re.sub('\n',' ',x), headline))
    price = list(map(lambda x: re.sub('MwSt. ausweisbar\n','',x), price))
    price = list(map(lambda x: x[3:-3], price))
    details = list(map(lambda x: x.split('\n\n'), details))
    kilometers = list(map(lambda x: x[1][:-3], details))
    build = list(map(lambda x: x[2][2:], details))
    horsepower = list(map(lambda x: x[3][9:-4], details))
    used = list(map(lambda x: x[4][1:], details))
    owners = list(map(lambda x: x[5][1], details))
    gear = list(map(lambda x: x[6][1:], details))

    #summarize information in pd data frame
    df_cars = pd.DataFrame(dict(
        id=id,
        headline = headline,
        price = price,
        kilometers = kilometers,
        build = build,
        horsepower = horsepower,
        used = used,
        owners = owners,
        gear = gear
    ))
    return df_cars

def scrape_data():
    '''
    Loops through all the links and applies the functions above.
    Outputs a data frame with the infos of all the pages (without duplicates).
    '''
    links = create_links()
    df_cars = pd.DataFrame([])
    for k in range(0,len(links)):
        time.sleep(1)
        quote_page = links[k]
        df_cars = df_cars.append(car_table_from_quote_page(quote_page),
                                    ignore_index=True)
    df_cars.drop_duplicates(subset= 'id', keep='first', inplace=True)
    df_cars['scraped'] = pd.Timestamp.today()
    return df_cars


def main():
    '''
    Applies scrape_data function and saves data frame with time stamp in
    file name in hfd5 format
    '''
    df_cars = scrape_data()
    df_cars.to_hdf('data/cars_'+str(pd.Timestamp.today().date())+'.h5',
                     key='df_cars',
                     mode='w')

if __name__ == '__main__':
    main()
