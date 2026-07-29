from src.classes.RequestPage import Page
from src.controllers.clean_pages import clean_info_page
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from src.models.main import save_in_database
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL")

page = Page()

def process_plant(id):
    with requests.Session() as session:
        html_page_text = page.get_page(
            f"{URL}{id}",
            session=session
        )

        plant_data = clean_info_page(
            html_page_text,
            session,
            f"{URL}{id}"
        )

        save_in_database(plant_data)


with ThreadPoolExecutor(max_workers=30) as executor:
    futures = [
        executor.submit(process_plant, id)
        for id in range(1, 10105)
    ]

    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Erro: {e}")