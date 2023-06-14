import math
import sqlite3
import random
import json

from flask import Flask, render_template, request, make_response, url_for

from functions import *
from telegram_bot_functions import *
from constants_data import *

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000'

SHOP_URL = f'{WEBSITE_URL}/shop/None-None&name-False&1'


@app.errorhandler(404)
@app.route('/Error<e>')
def handle_bad_request(e):
    return render_template("404.html", title='Error 404', levelness="../../../", url=WEBSITE_URL,
                           all_categories=ALL_CATEGORIES)


@app.route('/old_index')
def main_page():
    # Случайные товары
    colums_name = "id, name, description"
    random_product_list = select_from_db(colums_name=colums_name)

    random.shuffle(random_product_list)
    random_product_list_new = random.sample(random_product_list, 3)

    # Товары по скидке
    colums_name = "id, name, description, price, sale"
    filters = "sale != 0"
    upsell_product = select_from_db(colums_name=colums_name, filters=filters)

    random.shuffle(upsell_product)
    upsell_product = random.sample(upsell_product, min(7, len(upsell_product)))

    upsell_product = recycle_list("id, name, description, price, sale",
                                  "id, name, description, price, price_with_sale, sale",
                                  upsell_product)

    last_manufacturer_and_categories = request.cookies.get("last_manufacturer_and_categories")
    related_product = []
    if last_manufacturer_and_categories:
        manufacturer, categories = tuple(last_manufacturer_and_categories.split("$"))

        colums_name = "id, name, description, price, sale"
        filters = f"manufacturer == '{manufacturer}' or category like '%{categories}%'"

        related_product = select_from_db(colums_name=colums_name, filters=filters)

        random.shuffle(related_product)
        related_product = random.sample(related_product, min(7, len(related_product)))

        related_product = recycle_list("id, name, text, price, sale",
                                       "id, name, text, price, price_with_sale, sale",
                                       related_product)

    return render_template('index.html', title='SoundRepair | Главная страница', url=WEBSITE_URL,
                           random_product=random_product_list_new, upsell_product=upsell_product,
                           is_upsell_product=bool(upsell_product), is_related_product=len(related_product) >= 4,
                           related_product=related_product, all_categories=ALL_CATEGORIES)


@app.route('/index_2')
def index_2():
    return render_template("index-2.html", url=WEBSITE_URL, levelness="../",
                           all_categories=ALL_CATEGORIES)


@app.route('/')
def index_3():
    colums_name = "id, name, price, sale"

    top_products = recycle_list("id, name, price, sale",
                                "id, name, price, price_with_sale, sale",
                                random.sample(select_from_db(colums_name=colums_name), 15))
    top_products_mat = [top_products[:5], top_products[5:10], top_products[10:]]

    filters = "quantity = 1"
    last_products = recycle_list("id, name, price, sale",
                                 "id, name, price, price_with_sale, sale",
                                 random.sample(select_from_db(colums_name=colums_name, filters=filters), 5))

    category = random.choice(list(ALL_CATEGORIES.keys()))
    filters = f"category = '{category}'"
    category_products = select_from_db(colums_name=colums_name, filters=filters)
    category_products = recycle_list("id, name, price, sale",
                                     "id, name, price, price_with_sale, sale",
                                     random.sample(category_products, min(5, len(category_products))))

    manufacturer = random.choice(list(set(map(lambda x: x[0], select_from_db(colums_name="manufacturer")))))
    filters = f"manufacturer = '{manufacturer}'"
    manufacturer_products = select_from_db(colums_name=colums_name, filters=filters)
    manufacturer_products = recycle_list("id, name, price, sale",
                                         "id, name, price, price_with_sale, sale",
                                         random.sample(manufacturer_products, min(5, len(manufacturer_products))))

    works_list = [1, 2, 3, 4, 5]
    colums_name = "id, title, description, date"
    table_name = "our_works"
    filters = f"id IN {tuple(works_list)}"

    works = select_from_db(colums_name=colums_name, table_name=table_name, filters=filters)

    products_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    p_list = recycle_list("id, name, price, sale",
                          "id, name, price, price_with_sale, sale",
                          select_from_db(colums_name="id, name, price, sale",
                                         filters=f"id IN {tuple(products_id_list)}"))
    products_mat = [[p_list[0], p_list[1]],
                    [p_list[2], p_list[3]],
                    [p_list[4], p_list[5]],
                    [p_list[6], p_list[7]],
                    [p_list[8], p_list[9]],
                    [p_list[10], p_list[11]]]

    return render_template("index-3.html", url=WEBSITE_URL, last_products=last_products,
                           all_categories=ALL_CATEGORIES, top_products_mat=top_products_mat, works=works,
                           category_products=category_products, category=category, works_list=works_list,
                           manufacturer_products=manufacturer_products, manufacturer=manufacturer,
                           products_mat=products_mat)


@app.route('/product/<product_id>')
def product(product_id):
    # Берется по id товар
    colums_name = "id, name, description, manufacturer, category, sale, price"
    filters = f"id == {product_id}"

    product_data = select_from_db(colums_name=colums_name, filters=filters)
    print(product_data)

    product_data = recycle_list(
        "id, name, description, manufacturer, category, sale, price",
        "id, name, description, manufacturer, category, sale, price_with_sale_or_price, price",
        product_data)

    product_data = tuple(product_data[0])

    # related_product - 7шт

    colums_name = "id, name, description, price, sale"
    filters = f"manufacturer == '{product_data[3]}' OR category == '{product_data[4]}'"
    print(filters)

    related_product = select_from_db(colums_name=colums_name, filters=filters)

    random.shuffle(related_product)
    related_product = random.sample(related_product, min(7, len(related_product)))

    related_product = recycle_list("id, name, text, price, sale",
                                   "id, name, text, price, price_with_sale, sale",
                                   related_product)

    # upsell_product - товары по скидке (Рандомные со скидкой)
    colums_name = "id, name, description, price, sale"
    filters = "sale != 0"
    upsell_product = select_from_db(colums_name=colums_name, filters=filters)

    random.shuffle(upsell_product)
    upsell_product = random.sample(upsell_product, min(7, len(upsell_product)))

    upsell_product = recycle_list("id, name, description, price, sale",
                                  "id, name, description, price, price_with_sale, sale",
                                  upsell_product)
    print(product_data)
    res = make_response(
        render_template('product.html', title=f"SoundRepair | {product_data[1]}", product_data=product_data,
                        levelness="../", url=WEBSITE_URL, related_product=related_product,
                        upsell_product=upsell_product, product_id=product_id,
                        is_upsell_product=bool(upsell_product), all_categories=ALL_CATEGORIES,
                        is_related_product=bool(related_product)))

    res.set_cookie("last_manufacturer_and_categories", f"{product_data[5]}${product_data[6]}")
    return res


@app.route('/shop')
def shop():
    kwargs = {**{'page': 1, 'is_reverse': 0, 'sort_type': 'name'}, **dict(request.args)}

    manufactures = kwargs.get('manufacturer').split(',') if kwargs.get('manufacturer') else []
    category = kwargs.get('category') if kwargs.get('category') else []
    subcategory = kwargs.get('subcategory') if kwargs.get('subcategory') else []
    price = tuple(map(float, kwargs.get('price').split('-'))) if kwargs.get('price') else []

    filters = []
    if manufactures:
        filters.append(
            f'''manufacturer IN {tuple(manufactures) if len(manufactures) > 1 else f"('{manufactures[0]}')"}''')

    if subcategory:
        filters.append(f"""subcategory == '{subcategory}'""")
    elif category:
        filters.append(f"""category == '{category}'""")

    #  PRODUCTS ---------------------------------------------------------------------------------------------------
    products = select_from_db(colums_name="id, name, description, price, sale",
                              filters=' AND '.join(filters))

    products = recycle_list("id, name, text, price, sale",
                            "id, name, text, price, price_with_sale_or_price, sale",
                            products)

    products = sorted(products, key=lambda x: (x[1], x[4]) if kwargs.get('sort_type') == "name" else (x[4], x[1]),
                      reverse=int(kwargs.get('is_reverse')))

    products = list(filter(lambda x: price[0] <= x[4] and (price[1] >= x[4] if price[1] != 'inf' else True),
                           products)) if price else products
    #  RANDOM PRODUCTS --------------------------------------------------------------------------------------------
    random_product_list = select_from_db(colums_name="id, name, price, sale")
    random_product_list = random.sample(random_product_list, 9)
    random_product_mat = [random_product_list[:3], random_product_list[3:6], random_product_list[6:]]

    new_random_product_mat = []
    for product_list in random_product_mat:
        new_product_list = recycle_list("id, name, price, sale",
                                        "id, name, price, price_with_sale_or_price, sale",
                                        product_list)
        new_random_product_mat.append(new_product_list)

    #  WISHLIST --------------------------------------------------------------------------------------------------
    wishlist_list = get_wishlist_list()

    filters = ""
    if wishlist_list:
        if len(wishlist_list) > 1:
            filters = f"id in {tuple(wishlist_list)}"
        elif len(wishlist_list) == 1:
            filters = f"id == {wishlist_list[0]}"

    if filters:
        colums_name = "id, name, price, sale"
        wishlist_product_list = select_from_db(colums_name=colums_name, filters=filters)
    else:
        wishlist_product_list = []

    wishlist_product_list = recycle_list("id, name, price, sale",
                                         "id, name, price, price_with_sale_or_price, sale",
                                         wishlist_product_list)

    #  OTHER ------------------------------------------------------------------------------------------------------

    max_page = math.ceil(len(products) / 12)
    page = int(kwargs.get('page'))

    grid_item_list_text = f"Товары {1 + 12 * (page - 1) if len(products) > 0 else 0}-" \
                          f"{min(len(products), 12 * page)} из {len(products)}"

    all_categories = sorted(list(set(select_from_db(colums_name="category"))), key=lambda x: x[0])
    categories = []
    for category_l in all_categories:
        kwargs_copy = kwargs.copy()
        kwargs_copy["category"] = category_l[0]
        kwargs_copy["page"] = 1
        href = url_for('shop', **kwargs_copy)

        categories.append((category, href))
    if category:
        filter_list = {}
        for elem in ALL_CATEGORIES[category]:
            filter_list.update(FILTERS_LIST[elem])
    else: 
        filter_list = FILTERS_LIST[subcategory] if subcategory else []

    all_manufacturers = sorted(list(set(select_from_db(colums_name='manufacturer'))), key=lambda x: x[0])

    filter_price = kwargs.get('price').split('-') if kwargs.get('price') else ['', 'inf']

    price_sorted = sorted(products, key=lambda x: x[4])
    min_price, max_price = (price_sorted[0][4], price_sorted[-1][4]) if price_sorted else ('', '')

    if page > max_page and len(products) != 0:
        return render_template("404.html", title='Eror 404', levelness="../../../", url=WEBSITE_URL,
                               all_categories=ALL_CATEGORIES)
    res = make_response(
        render_template('shop.html', title='SoundRepair | Каталог', url=WEBSITE_URL, kwargs=kwargs,
                        categories=list(ALL_CATEGORIES.keys()), filter_price=filter_price,
                        all_categories=ALL_CATEGORIES,
                        product_mat=new_random_product_mat, products_list=products[(page - 1) * 12:page * 12],
                        grid_item_list_text=grid_item_list_text, max_price=max_price, filters_list=filter_list,
                        max_page=max_page, page=page, subcategories=subcategory, min_price=min_price,
                        wishlist_product_list=wishlist_product_list, is_reverse=int(kwargs.get('is_reverse')),
                        all_manufacturers=all_manufacturers))

    href = url_for('shop', **kwargs)
    res.set_cookie("last_ssesion", href)

    return res


@app.route('/contact')
def contact_page():
    return render_template('contact.html', url=WEBSITE_URL,
                           title='SoundRepair | Контакты', all_categories=ALL_CATEGORIES)


@app.route('/wishlist')
def wishlist():

    return render_template('wishlist.html', title="SoundRepair | Понравившиеся", url=WEBSITE_URL,
                        all_categories=ALL_CATEGORIES)


@app.route('/cart', methods=['post', 'get'])
def cart():
    return render_template('cart.html', title="SoundRepair | Корзина", url=WEBSITE_URL, all_categories=ALL_CATEGORIES)


@app.route('/about_us')
def about():
    return render_template('about.html', title='SoundRepair | О нас', url=WEBSITE_URL,
                           all_categories=ALL_CATEGORIES)


@app.route('/our_works/<page>')
def our_works(page):
    colums_name = "id, title, description, date"
    table_name = "our_works"

    works = select_from_db(colums_name=colums_name, table_name=table_name)

    works_count = len(works)
    pages_count = math.ceil(works_count / 12)

    return render_template('blog.html', title='SoundRepair | Наши работы', url=WEBSITE_URL,
                           all_categories=ALL_CATEGORIES,
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

                           all_categories=ALL_CATEGORIES, work_data=work_data, random_works=random_works,
                           first=first, last=last,
                           previous_work=previous_work, next_work=next_work)


@app.route('/services')
def services():
    return render_template('services.html', title='SoundRepair | Услуги', url=WEBSITE_URL,
                           all_categories=ALL_CATEGORIES, pages_count=1, page=1)

@app.route('/mobile_catalog')
def mobile_catalog():
    return render_template('mobile-catalog.html', title='SoundRepair | Каталог', url=WEBSITE_URL,
                           all_categories=ALL_CATEGORIES)

app.run(host=HOST, port=PORT)
