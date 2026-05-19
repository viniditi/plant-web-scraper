import requests


class Page():
    def get_page(self, url: str) -> str:
        """Returns an HTML page as string"""
        try:
            # session = requests.Session()

            page = requests.get(url=url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
            if page.status_code != 200:
                return f"Status code for '{url}' is different than 200, Status Code: {page.status_code}"
            return page.text

        except Exception as err:
            return f"An error had occurred. \nError: {err}"
        

    def get_pages(self, urls: tuple[str] | list[str]) -> list[str]:
        """Returns a list of HTML pages as string"""
        pages = []
        # ids = []
        with requests.Session() as session: 
            for url in urls:
                # plant_id = url.split('/')[-1]
                try:
                    session = requests.Session()
                    page = session.get(url=url)
                    if page.status_code != 200:
                        return f"Status code for '{urls}' is different than 200, Status Code: {page.status_code}"
                    pages.append(page.text)
                    # ids.append(plant_id)
                except Exception as err:
                    return f"An error had occurred. \nError: {err}"
        
        return pages