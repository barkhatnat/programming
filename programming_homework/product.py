from datetime import datetime, date


class Product:
    CATEGORIES = {1: "Продукты питания/напитки", 2: "Одежда и обувь", 3: "Хозтовары", 4: "Лекарства",
                  5: "Интернет-сервисы", 6: "Образование", 7: "Алкоголь и табак", 8: "Товары для детей",
                  9: "Бытовая техника", 10: "Средства по уходу", 11: "Без категории"}
    REVERSE_CATEGORIES = dict(zip(CATEGORIES.values(), CATEGORIES.keys()))
    DEFAULT_NAME = 'product'
    DEFAULT_PRICE = 0
    DEFAULT_DATE = '01.01.0001'
    DEFAULT_CATEGORY = 11

    def __init__(self, name=DEFAULT_NAME, price=DEFAULT_PRICE, mydate=DEFAULT_DATE, category=DEFAULT_CATEGORY):
        self.__product_name = name if self.check_product_name(name) else self.DEFAULT_NAME
        self.__product_price = price if self.check_product_price(price) else self.DEFAULT_PRICE
        if self.check_product_date(mydate):
            d, m, y = map(int, mydate.split('.'))
            self.__product_date = date(y, m, d)
        else:
            self.__product_date = date(1, 1, 1)
        self.__product_category = self.CATEGORIES[category] if self.check_product_category(
            category) else self.DEFAULT_CATEGORY

    @staticmethod
    def check_product_name(name):
        return all([ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z') or ord('а') <= ord(
            char) <= ord('я') or \
                    ord('А') <= ord(char) <= ord('Я') or char.isdigit() or char == ' ' for char in name]) \
            and len(list(name.split())) != 0

    @property
    def product_name(self):
        return self.__product_name

    @product_name.setter
    def product_name(self, name: str) -> None:
        if self.check_product_name(name):
            self.__product_name = name.capitalize()

    @staticmethod
    def check_product_price(price):
        return isinstance(price, int) and price > 0

    @property
    def product_price(self):
        return self.__product_price

    @product_price.setter
    def product_price(self, price):
        if self.check_product_price(price):
            self.__product_price = price

    @staticmethod
    def check_product_date(date):
        try:
            return datetime.strptime(date, '%d.%m.%Y').date() <= datetime.today().date()
        except ValueError:
            return False

    @property
    def product_date(self):
        return self.__product_date

    @product_date.setter
    def product_date(self, mydate):
        if self.check_product_date(mydate):
            d, m, y = map(int, mydate.split('.'))
            self.__product_date = date(y, m, d)

    @classmethod
    def check_product_category(cls, category):
        return isinstance(category, int) and category in list(cls.CATEGORIES.keys())

    @property
    def product_category(self):
        return self.__product_category

    @product_category.setter
    def product_category(self, category):
        if self.check_product_category(category):
            self.__product_category = self.CATEGORIES[category]

    def get_list_of_args(self) -> list:
        return [self.__product_name, self.__product_price, self.__product_date, self.__product_category]
