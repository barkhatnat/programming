import string
from datetime import datetime, date


class Product:
    VALID_CHARACTERS = string.ascii_letters + "йцукенгшщзхъфывапролджэячсмитьбю" + "йцукенгшщзхъфывапролджэячсмитьбю".upper() + string.digits + ' '
    CATEGORIES = {1: "Продукты питания/напитки", 2: "Одежда и обувь", 3: "Хозтовары", 4: "Лекарства",
                  5: "Интернет-сервисы", 6: "Образование", 7: "Алкоголь и табак", 8: "Товары для детей",
                  9: "Бытовая техника", 10: "Средства по уходу"}

    def __init__(self):
        self.product_name = self.product_price = self.product_date = self.product_category = None

    def set_name(self, product_name: str) -> None:
        assert set(product_name) <= set(
            self.VALID_CHARACTERS), "Имя продукта может содержать только английский алфавит, русский алфавит, цифры и пробел"
        assert len(list(product_name.split())) != 0, "Имя продукта не может состоять только из пробелов"
        self.product_name = product_name.capitalize()

    def set_price(self, product_price: int) -> None:
        assert product_price > 0, "Цена должна быть больше 0"
        self.product_price = product_price

    def set_date(self, product_date: str) -> None:
        get_date_status = lambda data: datetime.strptime(data, '%d.%m.%Y').date() <= datetime.today().date()
        assert get_date_status(product_date), "Нельзя поставить не наступившую дату"
        d, m, y = map(int, product_date.split('.'))
        self.product_date = date(y, m, d)

    def set_category(self, product_category) -> None:
        assert int(product_category) in range(1, len(self.CATEGORIES) + 1), "Категории под данным номером не существует"
        self.product_category = self.CATEGORIES[int(product_category)]
