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

SHOP_URL = f'{WEBSITE_URL}/shop/-|name-False|1'


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


@app.route('/index_2')
def index_2():
    return render_template("index-2.html", url=WEBSITE_URL, levelness="../",
                           cart_data=get_cart_for_base(), categories_for_base=get_categories())

@app.route('/index_3')
def index_3():
    return render_template("index-3.html", url=WEBSITE_URL, levelness="../",
                           cart_data=get_cart_for_base(), categories_for_base=get_categories())


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


@app.route('/shop/<manufacturers_filter>-<category>|<sort_type>-<is_reverse>|<page>')
def shop(manufacturers_filter=None, category=None, sort_type="name", is_reverse=False, page=1):
    print(manufacturers_filter, category, sort_type, is_reverse, page)
    full_url = f"{manufacturers_filter}-{category}|{sort_type}-{is_reverse}"

    manufacturers_filter = '' if manufacturers_filter == "None" else manufacturers_filter
    category = '' if category == "None" else category

    is_reverse = True if is_reverse == "True" else False
    manufacturers_filters_list = manufacturers_filter.split("&") if manufacturers_filter else []

    button_sort_href = f"{manufacturers_filter if manufacturers_filter else 'None'}-{category if category else 'None'}|" \
                       f"{'name' if sort_type == 'price' else 'price'}-{is_reverse}|{page}"
    arrow_sort_href = f"{manufacturers_filter if manufacturers_filter else 'None'}-{category if category else 'None'}|" \
                      f"{sort_type}-{not is_reverse}|{page}"

    page = int(page)

    # ------- MANUFACTURERS -------
    # Производители
    # manufacturers = [(name, n), (name, n), (name, n)] входные данные из списка
    colums_name = "manufacturer"
    manufacturers_list = select_from_db(colums_name=colums_name)
    manufacturers_list = list(map(lambda x: x[0], manufacturers_list))
    manufacturers_non_recurring = list(set(manufacturers_list))
    manufacturers = sorted(list(map(lambda x: (x, manufacturers_list.count(x)), manufacturers_non_recurring)))

    href_end = f"|{sort_type}-{is_reverse}|{page}"

    out_manufacturers = []
    for name, n in manufacturers:
        f = False
        if name in manufacturers_filters_list:
            f = True
            manufacturers_filters_list_copy = manufacturers_filters_list[:]
            manufacturers_filters_list_copy.remove(name)
            href = f"{'&'.join(manufacturers_filters_list_copy) if bool(manufacturers_filters_list_copy) else 'None'}" \
                   f"-{category if category else 'None'}{href_end}"
        else:
            manufacturers_filters_list_copy = manufacturers_filters_list[:]
            manufacturers_filters_list_copy.append(name)
            href = f"{'&'.join(manufacturers_filters_list_copy) if bool(manufacturers_filters_list_copy) else 'None'}" \
                   f"-{category if category else 'None'}{href_end}"

        out_manufacturers.append((name, n, href, f))

    # ------- CATEGORIES -------
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
        if name == category:
            f = True
            href = f"{manufacturers_filter if bool(manufacturers_filter) else 'None'}-None{href_end}"
        else:
            href = f"{manufacturers_filter if bool(manufacturers_filter) else 'None'}-{name}{href_end}"

        out_categories.append((name, n, href, f))

    # ------- RANDOM PRODUCTS -------
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

    # ------- WISHLIST -------
    # На выходе (id, name, img_href, text, price, sale_price, sale)
    wishlist_list = get_wishlist_list()

    filters = ""
    if bool(wishlist_list):
        if len(wishlist_list) > 1:
            filters = f"id in {tuple(wishlist_list)}"
        elif len(wishlist_list) == 1:
            filters = f"id == {wishlist_list[0]}"

    if bool(filters):
        colums_name = "id, name, img_href, price, sale"
        wishlist_product_list = select_from_db(colums_name=colums_name, filters=filters)
    else:
        wishlist_product_list = []

    wishlist_product_list = recycle_list("id, name, img_href, price, sale",
                                         "id, name, img_href, price, price_with_sale, sale",
                                         wishlist_product_list)

    # ------- PRODUCTS -------
    # Все товары
    # products_list = [(id, name, img_href, text, price, sale),
    #                  (id, name, img_href, text, price, sale)]

    filters = ""
    requect_list = []
    if manufacturers_filter:
        if len(manufacturers_filters_list) > 1:
            requect_list.append(f"manufacturer IN {tuple(manufacturers_filters_list)}")
        else:
            requect_list.append(f"manufacturer == '{manufacturers_filters_list[0]}'")

    if category:
        requect_list.append(f"categories == '{category}'")

    filters += " AND ".join(requect_list)

    colums_name = "id, name, img_href, short_description, price, sale"
    products_list = select_from_db(colums_name=colums_name, filters=filters)

    products_list = recycle_list("id, name, img_href, text, price, sale",
                                 "id, name, img_href, text, price, price_with_sale, sale",
                                 products_list)

    max_page = math.ceil(len(products_list) / 12)

    if page > max_page:
        return render_template("404.html", title='Eror 404', levelness="../../../", url=WEBSITE_URL,
                               cart_data=get_cart_for_base(), categories_for_base=get_categories())

    grid_item_list_text = f"Товары {1 + 12 * (page - 1)}-{min(len(products_list), 12 * page)} из {len(products_list)}"

    products_list = sorted(products_list, key=lambda x: (x[1], x[4]) if sort_type == "name" else (x[4], x[1]),
                           reverse=is_reverse)[(page - 1) * 12:page * 12]

    res = make_response(
        render_template('shop.html', title='SoundRepair | Каталог', levelness="../../../", url=WEBSITE_URL,
                        manufacturers=out_manufacturers, categories=out_categories,
                        product_mat=new_random_product_mat, products_list=products_list,
                        grid_item_list_text=grid_item_list_text, sort_type=sort_type, max_page=max_page, page=page,
                        full_url=full_url, next_page_url=f"{full_url}{page + 1}", button_sort_href=button_sort_href,
                        arrow_sort_href=arrow_sort_href, is_reverse=is_reverse, cart_data=get_cart_for_base(),
                        categories_for_base=get_categories(),
                        wishlist_product_list=wishlist_product_list))
    res.set_cookie("last_ssesion", f"/shop/{manufacturers_filter if bool(manufacturers_filter) else 'None'}-"
                                   f"{category if category else 'None'}|{sort_type}-{is_reverse}|{page}")

    return res


@app.route('/contact')
def contact_page():
    return render_template('contact.html', url=WEBSITE_URL, cart_data=get_cart_for_base(),
                           title='SoundRepair | Контакты', categories_for_base=get_categories())


@app.route('/wishlist/<action>$$<product_id>')
def wishlist(action, product_id):
    wishlist_list = get_wishlist_list()

    if action == "add":
        wishlist_list.append(int(product_id))
    elif action == "del" and int(product_id) in wishlist_list:
        wishlist_list.remove(int(product_id))

    filters = ""
    if bool(wishlist_list):
        if len(wishlist_list) > 1:
            filters = f"id in {tuple(wishlist_list)}"
        elif len(wishlist_list) == 1:
            filters = f"id == {wishlist_list[0]}"

    if bool(filters):
        colums_name = "id, name, img_href, price, sale"
        wishlist_product_list = select_from_db(colums_name=colums_name, filters=filters)
    else:
        wishlist_product_list = []

    wishlist_product_list = recycle_list("id, name, img_href, price, sale",
                                         "id, name, img_href, price, price_with_sale_or_price, sale",
                                         wishlist_product_list)

    total_price = sum(list(map(lambda x: x[4] if x[4] else x[3], wishlist_product_list)))
    total_price_with_sale = sum(list(map(lambda x: x[3], wishlist_product_list)))

    last_ssesion = request.cookies.get("last_ssesion")
    res = make_response(
        render_template('wishlist.html', title="SoundRepair | Корзина", url=WEBSITE_URL,
                        product_data=wishlist_product_list,
                        levelness="../../", total_price=total_price, total_price_with_sale=total_price_with_sale,
                        cart_data=get_cart_for_base(), categories_for_base=get_categories(),
                        last_ssesion=last_ssesion))
    res.set_cookie("wishlist", "$".join(list(map(str, wishlist_list))), max_age=60 * 60 * 24 * 365 * 2)

    return res


@app.route('/cart/<action>$$<product_id>')
def cart(action, product_id):
    # Находим все товары с id из wishlist_list
    # product_data = [(id, name, img_href, price, sale)]

    cart_list = get_cart_list()

    if action == "add":
        cart_list.append(int(product_id))
    elif action == "del" and int(product_id) in cart_list:
        cart_list.remove(int(product_id))

    filters = ""
    if bool(cart_list):
        if len(cart_list) > 1:
            filters = f"id in {tuple(cart_list)}"
        elif len(cart_list) == 1:
            filters = f"id == {cart_list[0]}"

    if bool(filters):
        colums_name = "id, name, img_href, price, sale"
        cart_product_list = select_from_db(colums_name=colums_name, filters=filters)
    else:
        cart_product_list = []

    cart_product_list = recycle_list("id, name, img_href, price, sale",
                                     "id, name, img_href, price, price_with_sale_or_price, sale",
                                     cart_product_list)

    total_price = sum(list(map(lambda x: x[4] if x[4] else x[3], cart_product_list)))
    total_price_with_sale = sum(list(map(lambda x: x[3], cart_product_list)))

    last_ssesion = request.cookies.get("last_ssesion")
    res = make_response(
        render_template('cart.html', title="SoundRepair | Корзина", url=WEBSITE_URL, product_data=cart_product_list,
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
    return render_template('blog-details.html', title=f'SoundRepair | {work_data[1]}', url=WEBSITE_URL,
                           cart_data=get_cart_for_base(),
                           categories_for_base=get_categories(), work_data=work_data, random_works=random_works,
                           first=first, last=last,
                           previous_work=previous_work, next_work=next_work)


app.run(host=HOST, port=PORT)
