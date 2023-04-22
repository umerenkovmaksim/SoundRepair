import math
import sqlite3

from flask import Flask, render_template, request, make_response


def get_cart_for_base(cart_list=None):
    con = sqlite3.connect("db/data.db")
    cur = con.cursor()

    if not cart_list:
        cart_list = request.cookies.get("cart")
        if cart_list:
            cart_list = cart_list.split("$")
        else:
            return None, None, None

    if len(cart_list) > 1:
        product_data = cur.execute(
            f"""SELECT id, name, img_href, price, sale FROM products WHERE id in {tuple(cart_list)}""")
    else:
        product_data = cur.execute(
            f"""SELECT id, name, img_href, price, sale FROM products WHERE id == {cart_list[0]}""")

    new_product_data = []
    for id, name, img_href, price, sale in product_data:
        product_list = [id, name, img_href, price]
        if sale != 0:
            product_list.append(int(price * (1 - sale * 0.01)))
            product_list.append(sale)
        else:
            product_list.append(price)
            product_list.append(None)

        new_product_data.append(tuple(product_list))

    total_price_with_sale = sum(list(map(lambda x: x[4], new_product_data)))

    con.close()
    return (len(new_product_data), new_product_data, total_price_with_sale)


app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000'


@app.errorhandler(404)
@app.route('/Error<e>')
def handle_bad_request(e):
    return render_template("404.html", title='Eror 404', levelness="../../../", url=WEBSITE_URL,
                           cart_data=get_cart_for_base())


@app.route('/')
def main_page():
    # Случайные товары
    # random_product = [(id, name, img_href, text), (name, img_href, text), (id, name, img_href, text)]
    random_product = [(1, "Product 1", "static/img/products/1.jpg", "text 1"),
                      (2, "Product 2", "static/img/products/2.jpg", "text 2"),
                      (3, "Product 3", "static/img/products/3.jpg", "text 3")]
    # print(get_cart_for_base()[0])
    # for n, products_cart_list, total_price in get_cart_for_base():
    #     print(n, products_cart_list, total_price)
    return render_template('index.html', title='SoundRepair', url=WEBSITE_URL, random_product=random_product,
                           cart_data=get_cart_for_base())


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

    return render_template('product.html', title=f"SoundRepair | {product_data[0][1]}", product_data=product_data,
                           levelness="../", url=WEBSITE_URL, price_with_sale=price_with_sale, text_2=text_2,
                           related_product=related_product, upsell_product=upsell_product, product_id=product_id,
                           cart_data=get_cart_for_base())


@app.route('/shop/<product_filter>$$<sorting_settings>$$<page>')
def shop(product_filter, sorting_settings, page):
    con = sqlite3.connect("db/data.db")
    cur = con.cursor()

    page = int(page)
    full_url = f"{product_filter}$${sorting_settings}$$"

    # product_filter это все фильтры для поиска
    # категории и производителя делит знак $
    # Это текст где фильтры делит знак &
    manufacturer_filter, categories_filter = tuple(product_filter.split("$"))
    manufacturer, categories_filter_list = manufacturer_filter, categories_filter.split("&")

    categories_filter_list = [] if categories_filter_list == [""] else categories_filter_list

    for i in range(categories_filter_list.count('')):
        categories_filter_list.remove('')

    print(manufacturer, categories_filter_list)

    # is_reverse это реверсивный поиск или нет
    # sort_type это тип сортировки по названию, или по цене
    sort_type, is_reverse_text = tuple(sorting_settings.split("$"))
    is_reverse = False if is_reverse_text == "up" else True

    button_sort_href = f"{manufacturer}${'&'.join(categories_filter_list)}$${'name' if sort_type == 'price' else 'price'}${is_reverse_text}$${page}"
    arrow_sort_href = f"{manufacturer}${'&'.join(categories_filter_list)}$${sort_type}${'up' if is_reverse else 'down'}$${page}"

    # Производители
    # manufacturers = [(name, n), (name, n), (name, n)] входные данные из списка
    manufacturers_list = cur.execute(f"""SELECT manufacturer FROM products""").fetchall()
    manufacturers_list = list(map(lambda x: x[0], manufacturers_list))
    manufacturers_non_recurring = list(set(manufacturers_list))
    manufacturers = sorted(list(map(lambda x: (x, manufacturers_list.count(x)), manufacturers_non_recurring)))

    href_end = f"$${sorting_settings}$${page}"

    out_manufacturers = []
    for name, n in manufacturers:
        f = False
        if name == manufacturer:
            f = True
            href = f"${'&'.join(categories_filter_list)}{href_end}"
        else:
            href = f"{name}${'&'.join(categories_filter_list)}{href_end}"

        out_manufacturers.append((name, n, href, f))

    # Тип товара
    # categories = [(name, n), (name, n), (name, n)]
    categories_list = cur.execute(f"""SELECT categories FROM products""").fetchall()
    all_categories_list = []
    print(categories_list)
    for categories_str in categories_list:
        all_categories_list += categories_str[0].split("&")

    categories_non_recurring = list(set(all_categories_list))
    categories = sorted(list(map(lambda x: (x, all_categories_list.count(x)), categories_non_recurring)))

    out_categories = []
    for name, n in categories:
        f = False
        if name in categories_filter_list:
            f = True

            categories_filter_list_copy = categories_filter_list[:]
            categories_filter_list_copy.remove(name)
            href = f"{manufacturer}${'&'.join(categories_filter_list_copy)}{href_end}"
        else:
            categories_filter_list_copy = categories_filter_list[:]
            categories_filter_list_copy.append(name)
            href = f"{manufacturer}${'&'.join(categories_filter_list_copy)}{href_end}"

        out_categories.append((name, n, href, f))

    # Максимальная/минимальная цены
    # prices = (max, min)
    prices = (100, 1)

    # Случайные товары
    # random_product_mat =
    # [[(id, name, img_href, text, price, sale), (id, name, img_href, text, price, sale)],
    #  [(id, name, img_href, text, price, sale), (id, name, img_href, text, price, sale)],
    #  [(id, name, img_href, text, price, sale), (id, name, img_href, text, price, sale)]]
    random_product_mat = [[(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, 10),
                           (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, None),
                           (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, 50)],
                          [(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, 10),
                           (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, None),
                           (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, 50)],
                          [(1, "Product 1", "static/img/products/1.jpg", "text 1", 100, 10),
                           (2, "Product 2", "static/img/products/2.jpg", "text 2", 250, None),
                           (3, "Product 3", "static/img/products/3.jpg", "text 3", 890, 50)]]

    new_random_product_mat = []
    for product_list in random_product_mat:
        new_product_list = []
        for id, name, img_href, text, price, sale in product_list:
            new_product = [id, name, img_href, text, price]
            if sale:
                sale_price = int(price * (1 - sale * 0.01))
                new_product.append(sale_price)
            else:
                new_product.append(None)
            new_product.append(sale)

            new_product_list.append(tuple(new_product))
        new_random_product_mat.append(new_product_list)
    # На выходе (id, name, img_href, text, price, sale_price, sale)

    # Все товары
    # products_list = [(id, name, img_href, text, price, sale),
    #                  (id, name, img_href, text, price, sale)]
    request = ""
    if manufacturer or categories_filter_list:
        request += "WHERE"
        requect_list = []
        if manufacturer:
            requect_list.append(f"manufacturer == {manufacturer}")

        if len(categories_filter_list) > 1:
            requect_list.append(f"categories IN {tuple(categories_filter_list)}")
        elif categories_filter_list:
            requect_list.append(f"categories == {categories_filter_list}")

        request += "AND".join(requect_list)



    print(f"""SELECT id, name, img_href, short_description, price, sale FROM products {request}""")
    products_list = cur.execute(
        f"""SELECT id, name, img_href, short_description, price, sale FROM products {request}""").fetchall()

    print(products_list)

    new_products_list = []
    for id, name, img_href, text, price, sale in products_list:
        new_product = [id, str(name), img_href, text, price]
        print(name)
        if sale != 0:
            new_product.append(int(price * (1 - sale * 0.01)))
            new_product.append(sale)
        else:
            new_product.append(None)
            new_product.append(None)

        new_products_list.append(tuple(new_product))

    # На выходе (id, name, img_href, text, price, sale_price, sale)

    max_page = math.ceil(len(products_list) / 12)

    if page > max_page:
        return render_template("404.html", title='Eror 404', levelness="../../../", url=WEBSITE_URL,
                               cart_data=get_cart_for_base())

    grid_item_list_text = f"Товары {1 + 12 * (page - 1)}-{min(len(products_list), 12 * page)} из {len(products_list)}"

    new_products_list = sorted(new_products_list, key=lambda x: (x[1], x[4]) if sort_type == "name" else (x[4], x[1]),
                               reverse=is_reverse)[(page - 1) * 12:page * 12]

    print(new_products_list)

    return render_template('shop.html', title='SoundRepair | Shop', levelness="../../../", url=WEBSITE_URL,
                           manufacturers=out_manufacturers, categories=out_categories,
                           product_mat=new_random_product_mat, products_list=new_products_list,
                           grid_item_list_text=grid_item_list_text, sort_type=sort_type, max_page=max_page, page=page,
                           full_url=full_url, next_page_url=f"{full_url}{page + 1}", button_sort_href=button_sort_href,
                           arrow_sort_href=arrow_sort_href, is_reverse=is_reverse, cart_data=get_cart_for_base())


@app.route('/contact')
def contact_page():
    return render_template('contact.html', url=WEBSITE_URL, cart_data=get_cart_for_base(),
                           title='SoundRepair | Contact')


@app.route('/wishlist/<action>$$<product_id>')
def wishlist(action, product_id):
    wishlist_list = request.cookies.get("wishlist", 0)
    if wishlist_list:
        wishlist_list = wishlist_list.split("$")
        wishlist_list = list(map(int, wishlist_list))
        if action == "add":
            wishlist_list.append(int(product_id))
        elif action == "del" and int(product_id) in wishlist_list:
            wishlist_list.remove(int(product_id))
    else:
        wishlist_list = []
        if action == "add":
            wishlist_list.append(int(product_id))

    wishlist_list = list(set(wishlist_list))

    # Находим все товары с id из wishlist_list
    # product_data = [(id, name, img_href, price, sale)]
    product_data = [(1, "Product 1", "static/img/products/1.jpg", 200, 20),
                    (2, "Product 2", "static/img/products/2.jpg", 500, None)]
    for product_id in wishlist_list:
        product_data.append((product_id, f"Product {product_id}", f"static/img/products/{product_id}.jpg", 10, 10))

    new_product_data = []
    for id, name, img_href, price, sale in product_data:
        product_list = [id, name, img_href]
        if sale:
            product_list.append(int(price * (1 - sale * 0.01)))
        else:
            product_list.append(price)

        new_product_data.append(tuple(product_list))

    # По выходу получиться new_product_data = [(id, name, img_href, price)]

    res = make_response(
        render_template('wishlist.html', title='SoundRepair | Wishlist', levelness="../../", url=WEBSITE_URL,
                        new_product_data=new_product_data, cart_data=get_cart_for_base()))

    print(wishlist_list)
    res.set_cookie("wishlist", "$".join(list(map(str, wishlist_list))), max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/cart/<action>$$<product_id>')
def cart(action, product_id):
    cart_list = request.cookies.get("cart")
    if cart_list:
        cart_list = cart_list.split("$")
        cart_list = list(map(int, cart_list))
        if action == "add":
            cart_list.append(int(product_id))
        elif action == "del" and int(product_id) in cart_list:
            cart_list.remove(int(product_id))
    else:
        cart_list = []
        if action == "add":
            cart_list.append(int(product_id))

    cart_list = list(set(cart_list))

    product_data = []
    for product_id in cart_list:
        product_data.append((product_id, f"Product {product_id}", f"static/img/products/{product_id}.jpg", 10, 10))

    print(type(product_data))
    print(product_data)

    new_product_data = []
    sale_f = False
    for id, name, img_href, price, sale in product_data:
        product_list = [id, name, img_href, price]
        if sale:
            sale_f = True
            product_list.append(int(price * (1 - sale * 0.01)))
        else:
            product_list.append(price)

        product_list.append(sale)

        new_product_data.append(tuple(product_list))

    if sale_f:
        total_price_with_sale = sum(list(map(lambda x: x[4], new_product_data)))
    else:
        total_price_with_sale = None

    if bool(new_product_data):
        total_price = sum(list(map(lambda x: x[3], new_product_data)))
    else:
        total_price = 0

    res = make_response(
        render_template('cart.html', title="SoundRepair | Cart", url=WEBSITE_URL, product_data=new_product_data,
                        levelness="../../", total_price=total_price, total_price_with_sale=total_price_with_sale,
                        cart_data=get_cart_for_base(cart_list)))
    res.set_cookie("cart", "$".join(list(map(str, cart_list))), max_age=60 * 60 * 24 * 365 * 2)

    return res


app.run(host=HOST, port=PORT)
