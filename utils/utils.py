import json
import os

from .db_api.main import User


class DataManager:
    @staticmethod
    def data_from_file(dir_path: str):
        """Получаем данные из json файлов."""
        res = []
        for file_name in os.listdir(dir_path):
            if file_name != "location":
                with open(f"{dir_path}/{file_name}", "r", encoding="utf-8") as file:
                    res.append(json.load(file))
        return res

    def get_categories(self, dir_path: str) -> list[str | None]:
        """Получаем все категории."""
        data = self.data_from_file(dir_path)
        return [item.get("category") for item in data]

    @staticmethod
    def get_locations(dir_path: str) -> list[dict[str, str]]:
        with open(f"{dir_path}/location/locations.json", "r", encoding="utf-8") as file:
            return json.load(file)


async def check_user_exists(user_id: int) -> bool:
    """Проверяем есть ли пользователь в базе данных"""
    return await User.get(user_id)


async def add_user(user_id: int, name: str, phone_number: int, location: str) -> None:
    """Добавляем пользователя в базу данных."""
    if not await check_user_exists(user_id):
        await User.create(
            id=user_id,
            name=name,
            phone_number=phone_number,
            location=location
        )
