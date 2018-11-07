## import libraries for scarping
from bs4 import BeautifulSoup
import requests
import re


# specify the url
quote_page = 'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=standard&desc=0&ustate=N%2CU&size=20&page=1&cy=D&atype=C&'

# query the website and return the html to the variable ‘page’
response = requests.get(quote_page)
soup = BeautifulSoup(response.content, "html.parser")

offerings = soup.findAll("div", {"data-item-name": "listing-summary-container"})


headline = []
price = []
details = []
for offering in offerings:
    headline.append(offering.find('div',{'data-item-name':'headline'}).text)
    price.append(offering.find('span',{'data-item-name':'price'}).text)
    details.append(offering.find('ul',{'data-item-name':'vehicle-details'}).text)

headline = list(map(lambda x: re.sub('\n',' ',x), headline))
price = list(map(lambda x: re.sub('MwSt. ausweisbar\n','',x), price))
price = list(map(lambda x: x[3:-3], price))
price
price[0]
price[0][3:-3]
