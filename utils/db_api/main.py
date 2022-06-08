from bot.loader import db


class Category(db.Model):
    """Модель таблицы категорий."""
    __tablename__ = "categories"

    category_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))

    @classmethod
    async def get_categories(cls) -> list[str]:
        categories = [item.to_dict().get("name") for item in await cls.query.gino.all()]
        return categories

    @classmethod
    async def get_category_id(cls, category_name: str):
        return await cls.select("category_id").where(cls.name == category_name).gino.scalar()


class Product(db.Model):
    """Модель таблицы продукта."""
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    link = db.Column(db.String)
    image_url = db.Column(db.String)
    price = db.Column(db.String)
    category = db.Column(db.Integer(), db.ForeignKey(Category.category_id))

    @classmethod
    async def get_products(cls, category_name):
        meals = await cls.query.where(Category.name == category_name).gino.all()
        return [meal.to_dict() for meal in meals]

    @classmethod
    async def get_product(cls, product_name: str):
        product = await cls.query.where(Product.name == product_name).gino.first()
        return product.to_dict()

    @classmethod
    async def set_products(cls, data):
        """Добавляем данные в базу данных."""
        if not await Product.query.gino.all():
            for item in data:
                for product in item.get("products"):
                    cat = await Category.select("category_id").where(
                        Category.name == product.get("category")
                    ).gino.scalar()
                    await Product.create(
                        name=product.get("name"),
                        description=product.get("description"),
                        link=product.get("link"),
                        image_url=product.get("image_url"),
                        price=str(product.get("price")),
                        category=cat
                    )


class Location(db.Model):
    """Модель таблицы местоположения."""
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    phone_number = db.Column(db.String)
    working_time = db.Column(db.VARCHAR(25))
    latitude = db.Column(db.Float, default=0)
    longitude = db.Column(db.Float, default=0)


class User(db.Model):
    """Модель таблицы пользователя."""
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True)
    phone_number = db.Column(db.BigInteger, primary_key=True, default=0)
    location = db.Column(db.String, default="")


class Order(db.Model):
    """Модель таблицы заказа."""
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, primary_key=True)
    product_name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    location = db.Column(db.String)


async def insert_categories(categories: list[str]) -> None:
    """Добавляем категории в базу данных."""
    if not await Category.query.gino.all():
        for category in categories:
            await Category.create(name=category)


async def insert_locations(data: list[dict[str, str]]) -> None:
    """Добавляем локации в базу данных."""
    count = 1
    if not await Location.query.gino.all():
        for item in data:
            await Location.create(
                id=count,
                name=item.get("name"),
                location=item.get("location"),
                phone_number=str(item.get("phone_number")),
                working_time=str(item.get("working_time"))
            )
            count += 1


async def check_user_exists(user_id: int) -> bool:
    """Проверяем есть ли пользователь в базе данных"""
    return await User.get(user_id)


async def add_user(user_id: int, phone_number: int, location: str) -> None:
    """Добавляем пользователя в базу данных."""
    if not await check_user_exists(user_id):
        await User.create(
            id=user_id,
            phone_number=phone_number,
            location=location
        )
