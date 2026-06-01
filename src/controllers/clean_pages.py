from bs4 import BeautifulSoup, Comment
from bs4.element import NavigableString
import requests
import re

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
    names = plant_info.find('div', class_='mb-2 capitalize').get_text('\n',strip=True).split('\n')
    
    info["name"] = names[0]
    info["scientific_name"] = names[1]

    if len(names) == 3:
        info["other_names"] = list(names[2].removeprefix('Also Known As - ').split(','))

    return info

def clean_pruning_water_sunlight(plant_info: BeautifulSoup, info: dict[str, str]):

    pruning_water_sunlight_title = plant_info.find_all('h3', class_='font-bold text-xl capitalize')
    pruning_water_sunlight_text = plant_info.find_all('p', class_='line-clamp-2 whitespace-pre-wrap break-words')

    for paragraph, h3 in zip(pruning_water_sunlight_text, pruning_water_sunlight_title):
        title = h3.get_text()
        description = paragraph.get_text()

        info[title] = description

    return info

def get_season_flowering_and_harvest(plant_info: BeautifulSoup, info: dict[str, str]):
    season = ['Fall', 'Winter', 'Spring', 'Summer']
    info['seasons'] = {}
    counter = 0
    
    try:
        elements = plant_info.find('div',  class_='grid grid-cols-2 md:grid-cols-4 gap-1 text-center pt-1').children

        for element in elements:
            element_div = element.find_next()
            text = ''

            if '\n' == element.get_text():
                continue

            elif element_div.find_all('div', class_='tooltips inline-block relative'):
                harvest_or_fruit = element.get_text()
                text = re.sub(r'\n+', '\n', harvest_or_fruit).strip().split('\n')
                
            else:
                text = None

            info['seasons'][season[counter]] = text
            counter += 1
    except AttributeError:
        return info

    return info
            


def plant_features(plant_info: BeautifulSoup, info: dict[str, str]):
    features = plant_info.find('div', class_='text-xs grid md:grid-cols-2 gap-2 bg-gray-100 rounded p-3').children

    info['features'] = {}

    for feature in features:
        
        if not isinstance(feature, (Comment, NavigableString)):
            title = feature.h3.get_text().removesuffix(':')
            value = feature.p.get_text()
            info['features'][title] = value
    
    return info

def get_months_flowering_and_harvest(plant_info: BeautifulSoup, info: dict[str, str]):
    months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    info['months'] = {}
    
    try:
        all_month_divs = plant_info.find('div', class_='grid grid-cols-2 md:grid-cols-4 gap-1 text-center text-xs')
        sla = all_month_divs.find_all('div', class_='py-3')

        for month in range(len(months)):
            class_color = sla[month].get('class', None)[0]
            info['months'][months[month]] = class_color.split('-')[1]
    except AttributeError:
        return info

    return info



def clean_info_page(pages: list[str]):

    all_info = []

    with requests.Session() as session:
        for page in pages:

            info = {}
        
            plant_id = page.split('/')[-1]
            info['id'] = int(plant_id)
        
            page_text = session.get(url=page, headers=HEADERS).text    
        
            plant_info = BeautifulSoup(page_text, "html.parser")
            
            get_title_and_subtitle(plant_info, info)

            clean_pruning_water_sunlight(plant_info, info)

            get_season_flowering_and_harvest(plant_info, info)

            get_months_flowering_and_harvest(plant_info, info)        

            all_info.append(info)

    return all_info

