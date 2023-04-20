import math

from flask import Flask, render_template

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000'


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
    # product = (id, name, img_href_list, text, price, is_sale, sale)
    # text - краткое описание
    # text_2 - полное описание
    # img_href_list = [img_href_1, img_href_2, img_href_3, img_href_4]
    # img_href_1 - основная картинка (Обязательна)
    # img_href_2, img_href_3, img_href_4 - доп. картинки (Необязательны, макс. 3)
    product_data = [(1, "Product 1", ["static/img/products/1.jpg", "static/img/products/2.jpg"], "text", 200, True, 20)]
    text_2 = "text 2"

    # related_product - похожие продукты или которые могут понравиться (На рандом скорее всего)
    # related_product = [(id, name, img_href, text, price, is_sale, sale),
    #                    (id, name, img_href, text, price, is_sale, sale),
    #                    (id, name, img_href, text, price, is_sale, sale)]
    # related_product - 7шт
    related_product = [(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                       (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, False, None),
                       (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50),
                       (1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                       (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, False, None),
                       (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50),
                       (1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10), ]

    # upsell_product - товары по скидке (Рандомные со скидкой)
    # upsell_product = [(id, name, img_href, text, price, is_sale, sale),
    #                    (id, name, img_href, text, price, is_sale, sale),
    #                    (id, name, img_href, text, price, is_sale, sale)]
    # upsell_product - 7шт

    upsell_product = [(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                      (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, True, 250),
                      (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50),
                      (1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10),
                      (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, True, 100),
                      (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, True, 50),
                      (1, "Product 1", "static/img/products/1.jpg", "text 1", 100, True, 10), ]

    price_with_sale = None
    if product_data[0][5]:
        price_with_sale = int(product_data[0][4] * (1 - product_data[0][6] * 0.01))

    print(type(product_data))
    return render_template('product.html', title=f"SoundRepair | {product_data[0][1]}", product_data=product_data,
                           levelness="../", url=WEBSITE_URL, price_with_sale=price_with_sale, text_2=text_2,
                           related_product=related_product, upsell_product=upsell_product, product_id=product_id)


@app.route('/shop/<product_filter>/<sorting_settings>/<page>')
def shop(product_filter, sorting_settings, page):
    page = int(page)
    full_url = f"{product_filter}/{sorting_settings}/"

    # product_filter это все фильтры для поиска
    # категории и производителя делит знак $
    # Это текст где фильтры делит знак &
    manufacturer_filter, categories_filter = tuple(product_filter.split("$"))
    manufacturer, categories_filter_list = manufacturer_filter, categories_filter.split("&")

    categories_filter_list = [] if categories_filter_list == [""] else categories_filter_list

    # is_reverse это реверсивный поиск или нет
    # sort_type это тип сортировки по названию, или по цене
    sort_type, is_reverse_text = tuple(sorting_settings.split("$"))
    is_reverse = False if is_reverse_text == "up" else True
    print(sort_type)

    button_sort_href = f"{manufacturer}${'&'.join(categories_filter_list)}/{'name' if sort_type == 'price' else 'price'}${is_reverse_text}/{page}"
    arrow_sort_href = f"{manufacturer}${'&'.join(categories_filter_list)}/{sort_type}${'up' if is_reverse else 'down'}/{page}"

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
    # products_list = [(id, name, img_href, text, price, is_in_wishlist, is_in_cart, is_sale, sale),
    #                  (id, name, img_href, text, price, is_in_wishlist, is_in_cart, is_sale, sale)]
    products_list = [(1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),

                     (1, "Product 1", "static/img/products/1.jpg", "Text", 450, True, True, True, 50),
                     (2, "Product 2", "static/img/products/2.jpg", "Text", 125, False, False, False, None),
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
                           max_page=max_page, page=page, full_url=full_url, next_page_url=f"{full_url}{page + 1}",
                           button_sort_href=button_sort_href, arrow_sort_href=arrow_sort_href, is_reverse=is_reverse)


@app.route('/about_us')
def contact_page():
    return render_template('contact.html', url=WEBSITE_URL)


app.run(host=HOST, port=PORT)
