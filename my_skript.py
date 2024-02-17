import requests
import json
import time
from bs4 import BeautifulSoup


class Parser:
    URL = "https://berserk.ru/?route=lib/feed/cards"

    def __call__(self):
        return self.__get_cards()

    @staticmethod
    def __get_body(page_number: int) -> dict:
        return {
            "saveState": True,
            "state": {"sort": "name", "order": "ASC", "page": page_number},
        }

    def __get_cards(self) -> list:
        page_number = 1
        storage = []
        with requests.Session() as s:
            while True:
                response = s.post(
                    self.URL, data=json.dumps(self.__get_body(page_number))
                )
                if response.status_code == 200:
                    data = response.json()
                    if data["rendered"] == "":
                        break
                    soup = BeautifulSoup(data["rendered"], "html.parser")
                    storage.extend(self.__parse_card(soup))
                    page_number += 1
                    continue
                raise Exception(f"Статус страницы: {response.status_code}")
        return storage

    @staticmethod
    def __parse_card(soup: BeautifulSoup) -> list:
        return [
            {"card_link": card.get("href"), "image_link": card.img["src"]}
            for card in soup.find_all("a")
        ]


if __name__ == "__main__":
    start_time = time.perf_counter()
    parser = Parser()()
    with open("config.json", "w", encoding="UTF-8") as config_file:

        json.dump(parser, config_file, indent=4, ensure_ascii=False)
    print(time.perf_counter() - start_time)
