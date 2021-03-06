import json
import re
import time

from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

GEOCODER_URL = "https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/utils/geocoder"


def setup_driver() -> WebDriver:
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


def find_locations(site_url: str, driver: WebDriver, search_text: str, sleep: int = 3) -> tuple:
    """Получение координат переданных адресов."""
    driver.get(site_url)
    time.sleep(sleep)
    # строка поиска в которой вводим текст поиска
    driver.find_element(By.ID, "query-input").send_keys(search_text)
    driver.find_element(By.ID, "geocode-button").click()
    time.sleep(sleep)
    # сохраняем полученный результат в файл html
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        result = soup.find("div", class_="active-result").find("p", class_="result-location")
        pattern = re.compile(r"\d+.\d+,\d+.\d+")
        content = result.get_text(strip=True)
        return tuple([float(loc) for loc in re.search(pattern, content).group().split(",")])
    except AttributeError as _err:
        print(_err)


def save_location_page(page_source: str) -> None:
    """Сохранение полученной html разметки в html файл."""
    with open("page.html", "w", encoding="utf-8") as file:
        file.write(page_source)


def soup_from_file(page_name: str) -> BeautifulSoup:
    """Получаем объект BeautifulSoup для работы с html файлом."""
    with open(page_name, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


# def get_coordinates_from_file(page_name: str) -> tuple:
#     """Получаем координаты из html файла."""
#     soup = soup_from_file(page_name)
#     try:
#         result = soup.find("div", class_="active-result").find("p", class_="result-location")
#         pattern = re.compile(r"\d+.\d+,\d+.\d+")
#         content = result.get_text(strip=True)
#         return tuple([float(loc) for loc in re.search(pattern, content).group().split(",")])
#     except AttributeError as _err:
#         print(_err)


def get_locations(dir_path: str) -> list[dict[str, str]]:
    with open(f"{dir_path}/location/locations.json", "r", encoding="utf-8") as file:
        return json.load(file)


class LocationManager(Nominatim):
    user_agent = "usersLocations"

    def __init__(self) -> None:
        super().__init__(user_agent=self.user_agent)

    def coordinates_from_address(self, address: str):
        return self.geocode(address, language="ru")

    def address_from_coordinates(self, latitude: float, longitude: float) -> dict[str, str]:
        """Получаем адреса с координат."""
        return self.reverse(f"{latitude}, {longitude}", language="ru").raw.get("address")

    def get_full_address(self, latitude: float, longitude: float):
        """Создаём полный адрес пользователя."""
        address = self.address_from_coordinates(latitude, longitude)
        data_list = ["house_number", "road", "quarter", "city", "country", ]
        return ", ".join([address.get(item) for item in data_list])


class AddressManager:
    @staticmethod
    def address_to_coordinates(data: list[dict[str, str]]) -> list[str]:
        return [item.get("location") for item in data]
