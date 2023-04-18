import math

from flask import Flask, render_template

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000/'


@app.route('/')
def main_page():
    # Случайные товары
    # random_product = [(id, name, img_href, text), (name, img_href, text), (id, name, img_href, text)]
    random_product = [(1, "Product 1", "static/img/products/1.jpg", "text 1"),
                      (2, "Product 2", "static/img/products/2.jpg", "text 2"),
                      (3, "Product 3", "static/img/products/3.jpg", "text 3")]
    return render_template('index.html', title='SoundRepair', url=WEBSITE_URL, random_product=random_product)


@app.route('/product/<product_id>')
def product(product_id):
    # Берется по id товар
    # product = (id, name, img_href, text, price, is_sale, sale)
    product_data = (1, "Product 1", "static/img/products/1.jpg", "text", 200, True, 20)
    print(product_data)
    return render_template('product.html', title='SoundRepair', product_data=product_data)


@app.route('/shop/<product_filter>/<sorting_settings>/<page>')
def shop(product_filter, sorting_settings, page):
    page = int(page)
    full_url = WEBSITE_URL + f"shop/{product_filter}/{sorting_settings}/"

    # product_filter это все фильтры для поиска
    # категории и производителя делит знак $
    # Это текст где фильтры делит знак &
    manufacturer_filter, categories_filter = tuple(product_filter.split("$"))
    manufacturer, categories_filter_list = manufacturer_filter, categories_filter.split("&")

    categories_filter_list = [] if categories_filter_list == [""] else categories_filter_list

    # is_reverse это реверсивный поиск или нет
    # sort_type это тип сортировки по названию, или по цене
    sort_type, is_reverse = tuple(sorting_settings.split("$"))
    is_reverse = False if is_reverse == "up" else True

    # Производители
    # manufacturers = [(name, n), (name, n), (name, n)] входные данные из списка
    manufacturers = [("Богдан", 3), ("Андрей", 6), ("Максим", 1)]

    href_end = f"/{sorting_settings}/{page}"
    out_manufacturers = []
    for name, n in manufacturers:
        f = False
        if name == manufacturer:
            f = True
            href = f"${'&'.join(categories_filter_list)}{href_end}"
        else:
            href = f"{name}${'&'.join(categories_filter_list)}{href_end}"

        out_manufacturers.append((name, n, href, f))
        print(out_manufacturers)

    # Тип товара
    # categories = [(name, n), (name, n), (name, n)]
    categories = [("Бам-бам громко", 10), ("Бам-бам громко, но не очень", 5), ("Бам-бам не очень громко", 13)]

    href_end = f"/{sorting_settings}/{page}"
    out_categories = []
    for name, n in categories:
        f = False
        if name in categories_filter_list:
            f = True
            print(categories_filter_list)
            print(name)
            categories_filter_list_copy = categories_filter_list[:]
            categories_filter_list_copy.remove(name)
            href = f"{manufacturer}${'&'.join(categories_filter_list_copy)}{href_end}"
        else:
            categories_filter_list_copy = categories_filter_list[:]
            categories_filter_list_copy.append(name)
            href = f"{manufacturer}${'&'.join(categories_filter_list_copy)}{href_end}"

        out_categories.append((name, n, href, f))
        print(out_categories)

    # Максимальная/минимальная цены
    # prices = (max, min)
    prices = (100, 1)

    # Случайные товары
    # random_product_mat =
    # [[(id, name, img_href, text, price, is_sale, sale), (id, name, img_href, text, price, is_sale, sale)],
    #  [(id, name, img_href, text, price, is_sale, sale), (id, name, img_href, text, price, is_sale, sale)],
    #  [(id, name, img_href, text, price, is_sale, sale), (id, name, img_href, text, price, is_sale, sale)]]
    random_product_mat = [[(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                           (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, False, None),
                           (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50)],
                          [(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                           (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, False, None),
                           (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50)],
                          [(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                           (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, False, None),
                           (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50)]]

    # Все товары
    # products_list = [(id, name, img_href, text, price, is_in_wishlist, is_in_cart, is_in_compare, is_sale, sale),
    #                  (id, name, img_href, text, price, is_in_wishlist, is_in_cart, is_in_compare, is_sale, sale)]
    products_list = [(1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, False, None),
                     ]

    max_page = math.ceil(len(products_list) / 12)
    print(max_page)
    if page > max_page:
        return render_template("404.html", title='SoundRepair', levelness="../../../", url=WEBSITE_URL)

    grid_item_list_text = f"Товары {1 + 12 * (page - 1)}-{min(len(products_list), 12 * page)} из {len(products_list)}"

    products_list = sorted(products_list, key=lambda x: (x[1], x[4]) if sort_type == "name" else (x[4], x[1]),
                           reverse=is_reverse)[(page - 1) * 12:page * 12]

    return render_template('shop.html', title='SoundRepair', levelness="../../../", url=WEBSITE_URL,
                           manufacturers=out_manufacturers, categories=out_categories, product_mat=random_product_mat,
                           products_list=products_list, grid_item_list_text=grid_item_list_text, sort_type=sort_type,
                           max_page=max_page, page=page, full_url=full_url, next_page_url=f"{full_url}{page + 1}")


app.run(host=HOST, port=PORT)
