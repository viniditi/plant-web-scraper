import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://perenual.com/plant-species-database-search-finder?indoor=1"
href = []

def request_url(url: str) -> str | None:
    
    page = requests.get(url)

    if page.status_code != 200:
        print("Status code is different than 200")
        
        return None
    
    return page.text

page_text = request_url(URL)

html_page = BeautifulSoup(page_text, "html.parser")

tag_a = html_page.find_all('a')

for hrefs in tag_a:
    href_value = hrefs.get('href', None)

    if href_value is not None and "https://perenual.com/plant-species-database-search-finder/species/" in href_value:
        href.append(href_value)


page = requests.get("https://perenual.com/plant-species-database-search-finder/species/425").text

info = BeautifulSoup(page, "html.parser")

slas = info.find_all('div', 'flex gap-1 capitalize')

# pprint(slas.h3)

h3 = []
p = []

for sla in slas:
    h3.append(sla.h3.get_text())
    p.append(sla.p.get_text())

pprint()