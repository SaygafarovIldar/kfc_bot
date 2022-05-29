from geopy.geocoders import Nominatim


class LocationManager(Nominatim):
    user_agent = "usersLocations"

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude
        super().__init__(user_agent=self.user_agent)

    def address_from_coordinates(self) -> dict[str, str]:
        """Получаем адреса с координат."""
        return self.reverse(f"{self.latitude}, {self.longitude}", language="ru").raw.get("address")

    def get_full_address(self):
        """Создаём полный адрес пользователя."""
        address = self.address_from_coordinates()
        data_list = ["house_number", "road", "quarter", "city", "country", ]
        return ", ".join([address.get(item) for item in data_list])
