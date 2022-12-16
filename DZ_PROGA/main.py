import csv

from product import *


class ShoppingList:
    __instance = None
    main_file_name = 'data.csv'
    SECTIONS = ["Название", "Цена", "Дата покупки", "Категория"]
    
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.product_list = []
        with open(self.main_file_name, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    d, m, y = map(int, row[2].split('-'))
                    correct_row = [str(row[0]), int(row[1]), date(d, m, y), row[3]]
                    self.product_list.append(correct_row)

                except ValueError:
                    pass
            with open("main_data.csv", 'w') as new_file:
                writer = csv.writer(new_file)
                for product in self.product_list:
                    writer.writerow(product)
            self.main_file_name = "main_data.csv"

    def add_product(self, new_product: Product) -> None:
        self.product_list.append(new_product)

    @staticmethod
    def __rebuild_csv(file_name, list_of_products: list) -> None:
        with open(file_name, 'w') as file:
            writer = csv.writer(file)
            for row in range(len(list_of_products)):
                writer.writerow(list_of_products[row])

    def show_product_list(self) -> None:
        print('\n' + "{:^100}".format("СПИСОК ПОКУПОК") + '\n')
        print("".join(["{:<30}".format(str(value)) for value in Product.SECTIONS]) + '\n')
        with open(self.main_file_name, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            line_number = 1
            for row in reader:
                row.insert(0, str(line_number))
                print("".join(["{:<30}".format(str(value)) for value in row]))
                line_number += 1
        print('\n')

    def create_product(self) -> None:
        new_product = Product()
        has_name = has_price = has_date = has_category = False
        while not has_name:
            try:
                name = input("Введите название продукта ")
                new_product.set_name(name)
                has_name = True
            except AssertionError as assert_message:
                print(f"ОШИБКА! {assert_message}")
                has_name = False
        while not has_price:
            try:
                price = input("Введите цену продукта ")
                new_product.set_price(int(price))
                has_price = True
            except AssertionError as assert_message:
                print(f"ОШИБКА! {assert_message}")
                has_price = False
            except ValueError:
                print(f"ОШИБКА! Цена должна быть задана целым числом")
                has_price = False
        while not has_date:
            try:
                mydate = input("Введите дату покупки ")
                new_product.set_date(mydate)
                has_date = True
            except AssertionError as assert_message:
                print(f"ОШИБКА! {assert_message}")
                has_date = False
            except ValueError:
                print(
                    f"ОШИБКА! Данной даты не существует или она задана в неверном формате. Дата должна быть в формате дд.мм.гггг")
                has_date = False
        while not has_category:
            try:
                category = input(f"К какой категории относится данный продукт? Выберите одну из "
                                 f"следующего перечня:\n{', '.join([f'{key} - {Product.CATEGORIES[key]}' for key in Product.CATEGORIES])} \n")
                new_product.set_category(category)
                has_category = True
            except AssertionError as assert_message:
                print(f"ОШИБКА! {assert_message}")
                has_category = False
            except ValueError:
                print(f"ОШИБКА! Укажите число, соответствующее нужной категории")
                has_category = False
        self.product_list.append(list(new_product.__dict__.values()))
        self.__rebuild_csv(self.main_file_name, self.product_list)
        self.__rebuild_csv('data.csv', self.product_list)

    def sort_by_price(self, reverse=False) -> None:
        self.product_list.sort(key=lambda x: x[1], reverse=reverse)
        self.__rebuild_csv(self.main_file_name, self.product_list)

    def sort_by_date(self, reverse=False) -> None:
        self.product_list.sort(key=lambda x: x[2], reverse=reverse)
        self.__rebuild_csv(self.main_file_name, self.product_list)

    def sort_by_category(self, category_number=None) -> None:
        if category_number in [str(number) for number in Product.CATEGORIES.keys()]:
            contain_category = lambda x: x[3] == Product.CATEGORIES[int(category_number)]
            sorted_list = [product for product in self.product_list if contain_category(product)]
            if len(sorted_list) == 0:
                print("В списке продуктов нет продуктов выбранной категории ")
            else:
                self.__rebuild_csv(self.main_file_name, sorted_list)
        elif category_number is None:
            self.__rebuild_csv(self.main_file_name, self.product_list)
        else:
            print("Данной категории не существует")

    def remove_product(self, number_of_product):
        if number_of_product in [str(i) for i in range(1, len(self.product_list) + 1)]:
            self.product_list.remove(self.product_list[int(number_of_product) - 1])
            self.__rebuild_csv(self.main_file_name, self.product_list)
            self.__rebuild_csv("data.csv", self.product_list)
            print("Товар успешно удалён")
        else:
            print("Товара с таким номером не существует")


SL = ShoppingList()
print("Добро пожаловать в приложение!")
sort_done_message = "\nПродукты успешно отсортированы\n"
while True:
    try:
        action = input("Что вы хотите сделать?\n"
                       "1 - просмотр списка покупок\n"
                       "2 - добавить новый продукт\n"
                       "3 - отсортировать по возрастанию цены\n"
                       "4 - отсортировать по убыванию цены\n"
                       "5 - отсортировать по категории\n"
                       "6 - отменить сортироваку по категории\n"
                       "7 - отсортировать по возрастанию даты\n"
                       "8 - отсортировать по убыванию даты\n"
                       "9 - удалить продукт\n"
                       "0 - выход\n")
        action = int(action)
        if action == 1:
            SL.show_product_list()
        elif action == 2:
            SL.create_product()
            print("\nПродукт успешно добавлен\n")
        elif action == 0:
            break
        elif action == 3:
            SL.sort_by_price()
            print(sort_done_message)
            SL.show_product_list()
        elif action == 4:
            SL.sort_by_price(True)
            print(sort_done_message)
            SL.show_product_list()
        elif action == 5:
            number_of_category = input(
                f"Выберите одну категорию из следующего перечня:\n{', '.join([f'{key} - {Product.CATEGORIES[key]}' for key in Product.CATEGORIES])} \n")
            SL.sort_by_category(number_of_category)
            print(sort_done_message)
            SL.show_product_list()
        elif action == 6:
            SL.sort_by_category()
            print("\nКатегория успешно сброшена\n")
            SL.show_product_list()
        elif action == 7:
            SL.sort_by_date()
            print(sort_done_message)
            SL.show_product_list()
        elif action == 8:
            SL.sort_by_date(True)
            print(sort_done_message)
            SL.show_product_list()
        elif action == 9:
            number_of_product = input("Введите номер продукта, который вы хотите удалить ")
            SL.remove_product(number_of_product)
        else:
            raise ValueError
    except ValueError:
        print('ОШИБКА! Вам необходимо выбрать функцию, введя соответствующее ей число')
print("Вы вышли из программы")
