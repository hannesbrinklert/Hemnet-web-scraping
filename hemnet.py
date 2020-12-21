import requests
import json
from bs4 import BeautifulSoup as bs
from postnumber import getPostNumber

start_url = "https://www.hemnet.se/salda/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=898741&page=1&sold_age=all"

link_list = []
obj_list = []

# Get all links to apartments


def getLinks(str):
    downloaded_html = requests.get(str)
    soup = bs(downloaded_html.text, features="lxml")
    links = soup.find_all('a', {'class': 'item-link-container'}, href=True)
    for link in links:
        link_list.append(link['href'])

# Transforms address to the correct format.


def parseAddress(st):
    index = st.find(",")
    if index != -1:
        return st[:index]
    else:
        return st


# Extract information from a single page regarding an apartment.
def singlePage(xlink):
    downloaded_html2 = requests.get(xlink)
    soup_2 = bs(downloaded_html2.text, features="lxml")
    address = soup_2.select('#page-content > div.column.large > h1')[0].text
    endPrice = soup_2.select(
        '#page-content > div.column.large > div.sold-property.qa-sold-property > div.sold-property__price > span.sold-property__price-value')[0].text
    askPrice = soup_2.select(
        '#page-content > div.column.large > div.sold-property.qa-sold-property > div.sold-property__details > dl.sold-property__price-stats > dd:nth-child(4)')[0].text
    pricePerSquare = soup_2.select(
        '#page-content > div.column.large > div.sold-property.qa-sold-property > div.sold-property__details > dl.sold-property__price-stats > dd:nth-child(2)')[0].text
    rooms = soup_2.select(
        '#page-content > div.column.large > div.sold-property.qa-sold-property > div.sold-property__details > dl.sold-property__attributes > dd:nth-child(2)')[0].text
    size = soup_2.select(
        '#page-content > div.column.large > div.sold-property.qa-sold-property > div.sold-property__details > dl.sold-property__attributes > dd:nth-child(4)')[0].text
    monthlyFee = soup_2.select(
        '#page-content > div.column.large > div.sold-property.qa-sold-property > div.sold-property__details > dl.sold-property__attributes > dd:nth-child(6)')[0].text
    date = soup_2.select(
        '#page-content > div.column.large > p > time', datetime=True)[0]['datetime']
    obj_list.append({
        'address': address[12:-1],
        'endPrice': stringToInt(endPrice[:-3]),
        'askPrice': stringToInt(askPrice[:-3]),
        'pricePerSquare': stringToInt(pricePerSquare[:-6]),
        'rooms': float(rooms.replace(",", ".")[:-4]),
        'size': float(size.replace(",", ".")[:-2]),
        'monthlyFee': stringToInt(monthlyFee[:-7]),
        'date': date,
        'postnumber': getPostNumber(parseAddress(address[12:-1]))
    })


# Converts string to int.
def stringToInt(str):
    return str.replace(u'\xa0', u' ')

# Method to run script


def run():
    for x in range(1, 51):
        getLinks('https://www.hemnet.se/salda/bostader?item_types%5B%5D=bostadsratt&location_ids%5B%5D=898741&page=' + str(x) + "&sold_age=all")

    for i in link_list:
        singlePage(i)


run()


with open("lgh.json", "w", encoding='utf8') as f:
    f.write("[")
    for obj in obj_list:
        json.dump(obj, f, ensure_ascii=False)
        f.write(",\n")

    f.write("]")
    f.close
