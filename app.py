from src.classes.RequestPage import Page
from src.controllers.clean_pages import find_all_anchors, clean_info_page
from pprint import pprint

URL = "https://perenual.com/plant-species-database-search-finder"
href = []

page = Page()

html_page_text = page.get_page(URL)

anchors = find_all_anchors(html_page_text)

html_pages_texts: list[str] = page.get_pages(anchors[0:2])

pprint(clean_info_page(anchors[0:2]))