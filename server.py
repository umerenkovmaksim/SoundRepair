import math
import sqlite3
import random
import json

from flask import Flask, render_template, request, make_response

from functions import *

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000'

SHOP_URL = f'{WEBSITE_URL}/shop/$$$name$up$$1'


@app.errorhandler(404)
@app.route('/Error<e>')
def handle_bad_request(e):
    return render_template("404.html", title='Error 404', levelness="../../../", url=WEBSITE_URL,
                           cart_data=get_cart_for_base(), categories_for_base=get_categories())


@app.route('/')
def main_page():
    # Случайные товары
    colums_name = "id, name, img_href, short_description"
    random_product_list = select_from_db(colums_name=colums_name)

    random.shuffle(random_product_list)
    random_product_list_new = random.sample(random_product_list, 3)

    # Товары по скидке
    colums_name = "id, name, img_href, short_description, price, sale"
    filters = "sale != 0"
    upsell_product = select_from_db(colums_name=colums_name, filters=filters)

    random.shuffle(upsell_product)
    upsell_product = random.sample(upsell_product, min(7, len(upsell_product)))

    upsell_product = recycle_list("id, name, img_href, short_description, price, sale",
                                  "id, name, img_href, short_description, price, price_with_sale, sale",
                                  upsell_product)

    #
    last_manufacturer_and_categories = request.cookies.get("last_manufacturer_and_categories")
    related_product = []
    if last_manufacturer_and_categories:
        manufacturer, categories = tuple(last_manufacturer_and_categories.split("$"))

        colums_name = "id, name, img_href, short_description, price, sale"
        filters = f"manufacturer == '{manufacturer}' or categories like '%{categories}%'"

        related_product = select_from_db(colums_name=colums_name, filters=filters)

        random.shuffle(related_product)
        related_product = random.sample(related_product, min(7, len(related_product)))

        related_product = recycle_list("id, name, img_href, text, price, sale",
                                       "id, name, img_href, text, price, price_with_sale, sale",
                                       related_product)

    return render_template('index.html', title='SoundRepair | Главная страница', url=WEBSITE_URL,
                           random_product=random_product_list_new, upsell_product=upsell_product,
                           is_upsell_product=bool(upsell_product), is_related_product=len(related_product) >= 4,
                           related_product=related_product, cart_data=get_cart_for_base(),
                           categories_for_base=get_categories())


@app.route('/product/<product_id>')
def product(product_id):
    # Берется по id товар
    filters = f"id == {product_id}"

    product_data = [select_from_db(filters=filters)[0]]

    product_data = recycle_list(
        "id, name, short_description, description, img_href, manufacturer, categories, sale, price",
        "id, name, short_description, description, img_href, manufacturer, categories, price_with_sale, price",
        product_data)

    product_data = tuple(product_data[0])

    # related_product - 7шт
    colums_name = "id, name, img_href, short_description, price, sale"
    filters = f"manufacturer == '{product_data[5]}' or categories like '%{product_data[6]}%'"

    related_product = select_from_db(colums_name=colums_name, filters=filters)

    random.shuffle(related_product)
    related_product = random.sample(related_product, min(7, len(related_product)))

    related_product = recycle_list("id, name, img_href, text, price, sale",
                                   "id, name, img_href, text, price, price_with_sale, sale",
                                   related_product)

    # upsell_product - товары по скидке (Рандомные со скидкой)
    colums_name = "id, name, img_href, short_description, price, sale"
    filters = "sale != 0"
    upsell_product = select_from_db(colums_name=colums_name, filters=filters)

    random.shuffle(upsell_product)
    upsell_product = random.sample(upsell_product, min(7, len(upsell_product)))

    upsell_product = recycle_list("id, name, img_href, short_description, price, sale",
                                  "id, name, img_href, short_description, price, price_with_sale, sale",
                                  upsell_product)

    res = make_response(
        render_template('product.html', title=f"SoundRepair | {product_data[1]}", product_data=product_data,
                        levelness="../", url=WEBSITE_URL, related_product=related_product,
                        upsell_product=upsell_product, product_id=product_id, cart_data=get_cart_for_base(),
                        categories_for_base=get_categories(), is_upsell_product=bool(upsell_product),
                        is_related_product=bool(related_product)))

    res.set_cookie("last_manufacturer_and_categories", f"{product_data[5]}${product_data[6]}")
    return res


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
    colums_name = "manufacturer"
    manufacturers_list = select_from_db(colums_name=colums_name)
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
    colums_name = "categories"
    categories_list = select_from_db(colums_name=colums_name)

    all_categories_list = []
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
    colums_name = "id, name, img_href, price, sale"
    random_product_list = select_from_db(colums_name=colums_name)
    random.shuffle(random_product_list)
    random_product_list_new = random.sample(random_product_list, 9)
    random_product_mat = [random_product_list_new[:3], random_product_list_new[3:6], random_product_list_new[6:]]

    new_random_product_mat = []
    for product_list in random_product_mat:
        new_product_list = recycle_list("id, name, img_href, price, sale",
                                        "id, name, img_href, price, price_with_sale, sale",
                                        product_list)
        new_random_product_mat.append(new_product_list)

    # На выходе (id, name, img_href, text, price, sale_price, sale)
    wishlist_list = request.cookies.get("wishlist")
    if wishlist_list:
        wishlist_list = wishlist_list.split("$")
        wishlist_list = list(map(int, wishlist_list))
        wishlist_list = wishlist_list[:3]
        if len(wishlist_list) > 1:
            wishlist_product_list = cur.execute(
                f"""SELECT id, name, img_href, price, sale FROM products WHERE id in {tuple(wishlist_list)} """).fetchall()
        else:
            wishlist_product_list = cur.execute(
                f"""SELECT id, name, img_href, price, sale FROM products WHERE id == {wishlist_list[0]} """).fetchall()
    else:
        wishlist_product_list = []

    wishlist_product_list_new = []
    for id, name, img_href, price, sale in wishlist_product_list:
        new_product = [id, name, img_href, price]
        if sale:
            sale_price = int(price * (1 - sale * 0.01))
            new_product.append(sale_price)
        else:
            new_product.append(None)
        new_product.append(sale)
        wishlist_product_list_new.append(new_product)

    print(wishlist_product_list_new)

    # Все товары
    # products_list = [(id, name, img_href, text, price, sale),
    #                  (id, name, img_href, text, price, sale)]
    manufacturer_request = ""
    if manufacturer or categories_filter_list:
        manufacturer_request += "WHERE "
        requect_list = []
        if manufacturer:
            requect_list.append(f"manufacturer == '{manufacturer}'")

        if len(categories_filter_list) > 1:
            requect_list.append(f"categories IN {tuple(categories_filter_list)}")
        elif categories_filter_list:
            requect_list.append(f"categories == '{categories_filter_list[0]}'")

        manufacturer_request += " AND ".join(requect_list)

    print(f"""SELECT id, name, img_href, short_description, price, sale FROM products {manufacturer_request}""")
    products_list = cur.execute(
        f"""SELECT id, name, img_href, short_description, price, sale FROM products {manufacturer_request}""").fetchall()

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
        con.close()
        return render_template("404.html", title='Eror 404', levelness="../../../", url=WEBSITE_URL,
                               cart_data=get_cart_for_base(), categories_for_base=get_categories())

    grid_item_list_text = f"Товары {1 + 12 * (page - 1)}-{min(len(products_list), 12 * page)} из {len(products_list)}"

    new_products_list = sorted(new_products_list, key=lambda x: (x[1], x[4]) if sort_type == "name" else (x[4], x[1]),
                               reverse=is_reverse)[(page - 1) * 12:page * 12]

    print(new_products_list)
    con.close()
    res = make_response(
        render_template('shop.html', title='SoundRepair | Каталог', levelness="../../../", url=WEBSITE_URL,
                        manufacturers=out_manufacturers, categories=out_categories,
                        product_mat=new_random_product_mat, products_list=new_products_list,
                        grid_item_list_text=grid_item_list_text, sort_type=sort_type, max_page=max_page, page=page,
                        full_url=full_url, next_page_url=f"{full_url}{page + 1}", button_sort_href=button_sort_href,
                        arrow_sort_href=arrow_sort_href, is_reverse=is_reverse, cart_data=get_cart_for_base(),
                        categories_for_base=get_categories(),
                        wishlist_product_list=wishlist_product_list_new))
    res.set_cookie("last_ssesion", f"/shop/{product_filter}$${sorting_settings}$${page}")

    return res


@app.route('/contact')
def contact_page():
    return render_template('contact.html', url=WEBSITE_URL, cart_data=get_cart_for_base(),
                           title='SoundRepair | Контакты', categories_for_base=get_categories())


@app.route('/wishlist/<action>$$<product_id>')
def wishlist(action, product_id):
    con = sqlite3.connect("db/data.db")
    cur = con.cursor()

    # Находим все товары с id из wishlist_list
    # product_data = [(id, name, img_href, price, sale)]

    wishlist_list = request.cookies.get("wishlist")
    if wishlist_list:
        wishlist_list = wishlist_list.split("$")
        wishlist_list = list(map(int, wishlist_list))
    else:
        wishlist_list = []

    if action == "add":
        wishlist_list.append(int(product_id))
    elif action == "del" and int(product_id) in wishlist_list:
        wishlist_list.remove(int(product_id))

    if bool(wishlist_list):
        if len(wishlist_list) > 1:
            wishlist_product_list = cur.execute(
                f"""SELECT id, name, img_href, price, sale FROM products WHERE id in {tuple(wishlist_list)} """).fetchall()
        elif len(wishlist_list) == 1:
            wishlist_product_list = cur.execute(
                f"""SELECT id, name, img_href, price, sale FROM products WHERE id == {wishlist_list[0]} """).fetchall()
        else:
            wishlist_product_list = []

    else:
        wishlist_product_list = []

    wishlist_product_list_new = []
    for id, name, img_href, price, sale in wishlist_product_list:
        product_list = [id, name, img_href]
        if sale:
            product_list.append(int(price * (1 - sale * 0.01)))
        else:
            product_list.append(price)

        wishlist_product_list_new.append(tuple(product_list))

    # По выходу получиться new_product_data = [(id, name, img_href, price)]
    con.close()
    print(wishlist_product_list_new)
    res = make_response(
        render_template('wishlist.html', title='SoundRepair | Понравившиеся', levelness="../../", url=WEBSITE_URL,
                        new_product_data=wishlist_product_list_new, cart_data=get_cart_for_base(),
                        categories_for_base=get_categories()))

    res.set_cookie("wishlist", "$".join(list(map(str, wishlist_list))), max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/cart/<action>$$<product_id>')
def cart(action, product_id):
    con = sqlite3.connect("db/data.db")
    cur = con.cursor()

    # Находим все товары с id из wishlist_list
    # product_data = [(id, name, img_href, price, sale)]

    cart_list = request.cookies.get("cart")
    if cart_list:
        cart_list = cart_list.split("$")
        cart_list = list(map(int, cart_list))
    else:
        cart_list = []
    print(cart_list)

    if action == "add":
        cart_list.append(int(product_id))
    elif action == "del" and int(product_id) in cart_list:
        cart_list.remove(int(product_id))

    if bool(cart_list):
        if len(cart_list) > 1:
            cart_product_list = cur.execute(
                f"""SELECT id, name, img_href, price, sale FROM products WHERE id in {tuple(cart_list)} """).fetchall()
        elif len(cart_list) == 1:
            cart_product_list = cur.execute(
                f"""SELECT id, name, img_href, price, sale FROM products WHERE id == {cart_list[0]} """).fetchall()
        else:
            cart_product_list = []

    else:
        cart_product_list = []
    print(cart_list)

    new_cart_product_list = []
    sale_f = False
    for id, name, img_href, price, sale in cart_product_list:
        product_list = [id, name, img_href, price]
        if sale:
            sale_f = True
            product_list.append(int(price * (1 - sale * 0.01)))
        else:
            product_list.append(price)

        product_list.append(sale)

        new_cart_product_list.append(tuple(product_list))

    if sale_f:
        total_price_with_sale = sum(list(map(lambda x: x[4], new_cart_product_list)))
    else:
        total_price_with_sale = None

    if bool(new_cart_product_list):
        total_price = sum(list(map(lambda x: x[3], new_cart_product_list)))
    else:
        total_price = 0

    con.close()

    last_ssesion = request.cookies.get("last_ssesion")
    res = make_response(
        render_template('cart.html', title="SoundRepair | Корзина", url=WEBSITE_URL, product_data=new_cart_product_list,
                        levelness="../../", total_price=total_price, total_price_with_sale=total_price_with_sale,
                        cart_data=get_cart_for_base(cart_list), categories_for_base=get_categories(),
                        last_ssesion=last_ssesion))
    res.set_cookie("cart", "$".join(list(map(str, cart_list))), max_age=60 * 60 * 24 * 365 * 2)

    return res


@app.route('/about_us')
def about():
    return render_template('about.html', title='SoundRepair | О нас', url=WEBSITE_URL, cart_data=get_cart_for_base(),
                           categories_for_base=get_categories())


@app.route('/our_works/<page>')
def our_works(page):
    colums_name = "id, title, description, date, img_href"
    table_name = "our_works"

    works = select_from_db(colums_name=colums_name, table_name=table_name)

    works_count = len(works)
    pages_count = math.ceil(works_count / 12)

    return render_template('blog.html', title='SoundRepair | Наши работы', url=WEBSITE_URL,
                           cart_data=get_cart_for_base(), categories_for_base=get_categories(),
                           works=works[12 * (int(page) - 1):12 * int(page)], page=int(page), pages_count=pages_count)


@app.route('/work/<id>')
def work(id):
    table_name = "our_works"
    filters = f"id == {id}"

    other_works = []
    all_works = select_from_db(table_name=table_name)

    cur_id = 0
    for index, elem in enumerate(all_works):
        if int(elem[0]) != int(id):
            other_works.append(elem)
        else:
            cur_id = index
        
    first, last = int(all_works[0][0]) == int(id), int(all_works[-1][0]) == int(id)
    previous_work, next_work = all_works[cur_id - 1] if not first else None, all_works[cur_id + 1] if not last else None

    random_works = random.sample(other_works, 4)

    work_data = select_from_db(table_name=table_name, filters=filters)[0]
    return render_template('blog-details.html', title=f'SoundRepair | {work_data[1]}', url=WEBSITE_URL, cart_data=get_cart_for_base(), 
                           categories_for_base=get_categories_for_base(), work_data=work_data, random_works=random_works, first=first, last=last,
                             previous_work=previous_work, next_work=next_work)

app.run(host=HOST, port=PORT)
