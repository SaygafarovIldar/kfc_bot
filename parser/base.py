import json
import re

import requests
from bs4 import BeautifulSoup

# type aliases
MenuItems = list[dict[str, str]]
ProductItems = list[dict[str, MenuItems]]

# Константы
BASE_URL = "https://www.kfc.com.uz"
BASE_URL_RU = "https://www.kfc.com.uz/ru/main"


class Parser:
    ru_url = "https://www.kfc.com.uz/ru/main"

    @staticmethod
    def __get_content(url: str) -> bytes:
        """Получаем контент страницы по переданной ссылке."""
        return requests.get(url).content

    def __get_soup(self, url: str) -> BeautifulSoup:
        """Получаем разметку страницы."""
        html = self.__get_content(url)
        return BeautifulSoup(html, "html.parser")

    def get_menu_items(self, url: str) -> MenuItems:
        """Получаем все категории."""
        soup = self.__get_soup(url)
        menu_wrapper = soup.find("li", class_="menu")
        return [{
            "name": item.get_text(strip=True),
            "link": BASE_URL + item.a.get("href")
        } for item in menu_wrapper.find_all("li")]

    @staticmethod
    def to_tuple_menu_items(data: MenuItems) -> tuple[str | None]:
        """Получаем только названия категорий в виде кортежа."""
        return tuple([category.get("name") for category in data])

    def get_category_items(self, url: str) -> ProductItems:
        """Получаем все продукты категории."""
        res = []
        menu_items = self.get_menu_items(url)
        for menu_item in menu_items:
            soup = self.__get_soup(menu_item.get("link"))
            product_wrapper = soup.find("ul", class_="products-detail-list")
            res.append({
                "category": menu_item.get("name"),
                "products": [{
                    "name": product.find("h4").get_text(strip=True),
                    "description": self.__get_product_description(BASE_URL + product.find("a").get("href")),
                    "link": BASE_URL + product.find("a").get("href"),
                    "image_url": product.find("img").get("src"),
                    "price": self.__get_product_price(BASE_URL + product.find("a").get("href")),
                    "category": menu_item.get("name")
                } for product in product_wrapper.find_all("li")]
            })

        self.__write_to_json(dir_name="../data", items=res)

        return res

    def __get_product_price(self, url: str) -> str:
        """Получаем цену каждого товара."""
        soup = self.__get_soup(url)
        return soup.find("h3", class_="price").get_text(strip=True)

    def __get_product_description(self, url: str) -> str:
        """Получаем полное описание каждого товара."""
        soup = self.__get_soup(url)
        return soup.find(id="product_description").find("em").get_text(strip=True)

    def get_restaurants_info(self, url: str) -> list[dict[str, str]]:
        """Получаем информацию о ресторанах в городе."""
        res = []
        soup = self.__get_soup(url)
        content_wrapper = soup.find("ul", class_="content-list")
        for item in content_wrapper.find_all("li", class_="restaurant-info"):
            name = item.find("div", class_="content-list-name").get_text(strip=True)
            info_wrapper = item.find("div", class_="content-list-main").find_all("p")
            location = info_wrapper[0].get_text(strip=True)
            phone_number = info_wrapper[1].find("a").get_text(strip=True)
            working_time = item.find("p", class_="highlight").get_text(strip=True)
            time = re.match(r"^\d+:\d+ — \d+:\d+", working_time).group()
            res.append({
                "name": name,
                "location": location,
                "phone_number": phone_number,
                "working_time": time
            })

        return res

    @staticmethod
    def __write_to_json(dir_name: str, items: ProductItems | MenuItems) -> None:
        """Записываем полученные данные в json."""
        for item in items:
            with open(f"{dir_name}/{item.get('category')}.json", "w", encoding="utf-8") as file:
                json.dump(item, file, indent=4, ensure_ascii=False)
