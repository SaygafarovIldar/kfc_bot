import json
import os


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
