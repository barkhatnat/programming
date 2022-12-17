import csv
from operator import attrgetter
import string
from product import *


class ShoppingList:
    __instance = None
    main_file_name = 'data.csv'
    SECTIONS = ["Номер", "Название", "Цена", "Дата покупки", "Категория"]

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.product_list = []
        self.chosen_category = None
        with open(self.main_file_name, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                y, m, d = map(int, row[2].split('-'))
                new_product = Product(row[0], int(row[1]), str(f'{d}.{m}.{y}'), Product.REVERSE_CATEGORIES[row[3]])
                self.add_product(new_product)

    def add_product(self, new_product: Product()) -> None:
        self.product_list.append(new_product)

    def show_product_list(self) -> None:
        print('\n' + "{:^135}".format("СПИСОК ПОКУПОК") + '\n')
        print("".join(["{:<30}".format(str(value)) for value in self.SECTIONS]) + '\n')
        line_number = 1
        for row in self.product_list:
            row = row.get_list_of_args()
            category_flag = True
            if self.chosen_category:
                category_flag = row[-1] == Product.CATEGORIES[self.chosen_category]
            if category_flag:
                if not (set(row[0]) <= set(string.digits)):
                    row.insert(0, str(line_number))
                print("".join(["{:<30}".format(str(value)) for value in row]) + '\n')
                line_number += 1

    def __rebuild_csv(self) -> None:
        with open(self.main_file_name, 'w') as file:
            writer = csv.writer(file)
            for row in self.product_list:
                row = row.get_list_of_args()
                writer.writerow(row)

    def set_sorting_category(self) -> None:
        has_number_of_category = False
        while not has_number_of_category:
            new_number_of_category = input(f"Введите категорию товара. Выберите одну из "
                                 f"следующего перечня:\n{', '.join([f'{key} - {Product.CATEGORIES[key]}' for key in Product.CATEGORIES])} \n")
            if set(new_number_of_category) <= set(string.digits):
                new_number_of_category = int(new_number_of_category)
                if new_number_of_category in range(1, len(Product.CATEGORIES) + 1):
                    self.chosen_category = new_number_of_category
                    has_number_of_category = True
                else:
                    print("\nТакой категории не существует\n")
            else:
                print("\nКатегория задается целым числом\n")

    def unset_sorting_category(self) -> None:
        self.chosen_category = None

    def remove_product(self, number_of_product: str) -> None:
        if number_of_product in [str(i) for i in range(1, len(self.product_list) + 1)]:
            self.product_list.remove(self.product_list[int(number_of_product) - 1])
            self.__rebuild_csv()
            print("\nТовар успешно удалён\n")
        else:
            print("\nТовара с таким номером не существует\n")

    def create_new_product(self) -> list:
        has_name = has_price = has_date = has_category = False
        new_product = Product()
        while not has_name:
            new_product.product_name = input("Введите название товара ")
            if new_product.product_name == Product.DEFAULT_NAME:
                print("\nИмя товара может содержать только английский алфавит, русский алфавит, цифры и пробел\n")
            else:
                has_name = True
        while not has_price:
            new_price = input("Введите цену товара ")
            if set(new_price) <= set(string.digits):
                new_product.product_price = int(new_price)
                if new_product.product_price == Product.DEFAULT_PRICE:
                    print("\nЦена должна быть больше 0\n")
                else:
                    has_price = True
            else:
                print("\nЦена должна являться целым числом\n")

        while not has_date:
            new_product.product_date = input("Введите дату покупки ")
            if new_product.product_date == date(1, 1, 1):
                print(
                    "\nДанной даты не существует или она задана в неверном формате. Дата должна быть в формате дд.мм.гггг\n")
            else:
                has_date = True
        while not has_category:
            new_category = input(f"К какой категории относится данный товар? Выберите одну из "
                                 f"следующего перечня:\n{', '.join([f'{key} - {Product.CATEGORIES[key]}' for key in Product.CATEGORIES])} \n")
            if set(new_category) <= set(string.digits):
                new_product.product_category = int(new_category)
                if new_product.product_category == Product.CATEGORIES[Product.DEFAULT_CATEGORY]:
                    print("\nКатегории под данным номером не существует\n")
                    new_product.product_category = input(
                        f"К какой категории относится данный товар? Выберите одну из "
                        f"следующего перечня:\n{', '.join([f'{key} - {Product.CATEGORIES[key]}' for key in Product.CATEGORIES])} \n")
                else:
                    has_category = True
            else:
                print("\nКатегория задается целым числом\n")
        self.add_product(new_product)
        self.__rebuild_csv()
        return new_product.get_list_of_args()


SL = ShoppingList()

print(SL.product_list)
SL.show_product_list()
while True:
    action = input("Что вы хотите сделать?\n"
                   "1 - просмотр списка товаров\n"
                   "2 - добавить новый товар\n"
                   "3 - отсортировать по алфавиту\n"
                   "4 - отсортировать по возрастанию цены\n"
                   "5 - отсортировать по убыванию цены\n"
                   "6 - отсортировать по возрастанию даты\n"
                   "7 - отсортировать по убыванию даты\n"
                   "8 - отсортировать по категории\n"
                   "9 - убрать сортировку по категории\n"
                   "10 - удалить товар\n"
                   "0 - выход\n")
    match action:
        case '1':
            SL.show_product_list()

        case '2':
            SL.create_new_product()
        case '3':
            SL.product_list = sorted(SL.product_list, key=attrgetter('product_name'))
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '4':
            SL.product_list = sorted(SL.product_list, key=attrgetter('product_price'))
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '5':
            SL.product_list = sorted(SL.product_list, key=attrgetter('product_price'), reverse=True)
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '6':
            SL.product_list = sorted(SL.product_list, key=attrgetter('product_date'))
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '7':
            SL.product_list = sorted(SL.product_list, key=attrgetter('product_date'), reverse=True)
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '8':
            SL.set_sorting_category()
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '9':
            SL.unset_sorting_category()
            print("\nСписок успешно отсортирован\n")
            SL.show_product_list()
        case '10':
            number_of_product = input("Введите номер товара, который вы хотите удалить ")
            SL.remove_product(number_of_product)
        case '0':
            break
        case _:
            print("\nДанной комманды не существует\n")
