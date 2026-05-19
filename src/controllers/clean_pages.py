from bs4 import BeautifulSoup
from pprint import pprint
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def find_all_anchors(page_text):
    href = []

    html_page = BeautifulSoup(page_text, "html.parser")
    tag_a = html_page.find_all('a')

    for hrefs in tag_a:
        href_value = hrefs.get('href', None)

        if href_value is not None and "https://perenual.com/plant-species-database-search-finder/species/" in href_value:
            href.append(href_value)

    return href

def get_title_and_subtitle(plant_info: BeautifulSoup, info: dict[str, str]):
    info["name"]=plant_info.find('h1').get_text()
    info["scientific_name"] = plant_info.find('h2').get_text().strip()

    return info

def clean_pruning_whater_sunlight(plant_info: BeautifulSoup, info: dict[str]):

    pruning_whater_sunlight_title = plant_info.find_all('h3', class_='font-bold text-xl capitalize')
    pruning_whater_sunlight_text = plant_info.find_all('p', class_='line-clamp-2 whitespace-pre-wrap break-words')

    for paragraph, h3 in zip(pruning_whater_sunlight_text, pruning_whater_sunlight_title):
        title = h3.get_text()
        description = paragraph.get_text()

        info[title] = description

    return info

def plant_features(plant_info: BeautifulSoup, info):
    features = plant_info.find_all('div', 'flex gap-1 capitalize')
    
    temp_dict = {}

    for feature in features:
        title = features[feature].h3.get_text()
        value = feature[feature].p.get_text()
        temp_dict[title] = value
    
    return []

def get_season(plant_info: BeautifulSoup, info):
    page_text = plant_info.find_all('div', class_='grid grid-cols-2 md:grid-cols-4 gap-1 text-center text-xs')
    


def clean_info_page(pages: list[str]):

    all_info = []

    with requests.Session() as session:
        for page in pages:

            info = {}
        
            plant_id = page.split('/')[-1]
            info['id'] = plant_id
        
            page_text = session.get(url=page, headers=HEADERS).text    
        
            plant_info = BeautifulSoup(page_text, "html.parser")
            
            get_title_and_subtitle(plant_info, info)

            clean_pruning_whater_sunlight(plant_info, info)

            all_info.append(info)

    return all_info

