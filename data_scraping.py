## import libraries for scarping
import urllib3
from bs4 import BeautifulSoup
import requests


# specify the url
quote_page = 'https://www.autoscout24.de/lst/porsche/911er-(alle)?sort=standard&desc=0&ustate=N%2CU&size=20&page=1&cy=D&atype=C&'

# query the website and return the html to the variable ‘page’
response = requests.get(quote_page)
soup = BeautifulSoup(response.content, "html.parser")

offerings = soup.findAll("div", {"data-item-name": "listing-summary-container"})


headline = []
price = []
for offering in offerings:
    headline.append(offering.find('div',{'data-item-name':'headline'}).text)
    price.append(offering.find('span',{'data-item-name':'price'}).text)

headline

'''
html verstehen:
oberste ebene fuer die liste der karren: 'div class = "cl-list-elemets" > == $0'
danach kommen die einzelnen angebote mit id:'cl-list-elemet'
'''
