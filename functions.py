import sqlite3

from flask import request


def select_from_db(table_name="products", colums_name="*", filters=None):
    # print("select_from_db")
    # print(table_name, colums_name, filters)
    #
    # % select_from_db нужен для получения данных из db %
    #
    # table_name - str
    # table_name имя таблицы из которой брать данные
    #
    # colums_name = str
    # colums_name список столбцов для получения через ', '
    #
    # filters - str
    # filters филтры по которым выбираються значения (в формате SQL)
    #

    colums_name = colums_name.replace("short_description", "description")
    colums_name = colums_name.replace("categories", "category")

    con = sqlite3.connect("db/data.db")
    cur = con.cursor()

    request = f"""SELECT {colums_name} FROM {table_name}"""
    if filters:
        request += f" WHERE {filters}"

    print(request)
    # print()

    res = cur.execute(request).fetchall() if 'None' not in request else []

    # Вывод list содержащий tuple со значениями
    return res


def get_wishlist_list():
    #
    # % get_wishlist_list нужен для получения списка id товаров в хотелках %
    #

    wishlist_list = request.cookies.get("wishlist")
    if wishlist_list:
        wishlist_list = wishlist_list.split("&")
        wishlist_list = list(map(int, wishlist_list))
        return wishlist_list
    return []

    # Если в карзине пусто вывод tuple (None, None, None)
    # Иначе list с id товаров


def recycle_list(inp, out, data_list):
    # print("recycle_list")
    # print(inp, out, data_list)
    # print()
    #
    # % recycle_list нужен для преоброзования списка tuple по заданному принципу %
    #
    # inp - str
    # inp = Наименования элементов через ', ' (Пример (id, name, price, sale)
    # inp описывает каие элементы нам подаються
    #
    # out - str
    # out = Наименования элементов через ', ' (Пример (id, name, price, sale)
    # out описывает каие элементы нам надо вывести и как
    #
    # data_list - list
    # В data_list находяться элементы типа tuple которые описываються inp
    #
    out_data_list = []
    inp = inp.split(", ")
    out = out.split(", ")
    for data in data_list:

        data_dict = {}
        for key in inp:
            data_dict[key] = data[inp.index(key)]

        out_list = []
        for key in out:
            if key == "description":
                out_list.append(data_dict[key].split("\n"))

            elif key in data_dict.keys():
                out_list.append(data_dict[key])

            elif key == "price_with_sale":
                if data_dict["sale"] != 0:
                    out_list.append(int((data_dict["price"]) * (1 - int(data_dict["sale"]) * 0.01)))
                else:
                    out_list.append(None)

            elif key == "price_with_sale_or_price":
                if data_dict["sale"] != 0:
                    out_list.append(int(data_dict["price"] * (1 - data_dict["sale"] * 0.01)))
                else:
                    out_list.append(int(data_dict["price"]))

        out_data_list.append(out_list)

    # вывод list с изменеными tuple
    return out_data_list


def get_categories():
    colums_name = "categories"

    categories_list = select_from_db(colums_name=colums_name)
    all_categories_list = []
    for categories_str in categories_list:
        all_categories_list += categories_str[0].split("&")

    categories_non_recurring = list(set(all_categories_list))

    return categories_non_recurring
