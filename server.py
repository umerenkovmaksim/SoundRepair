from flask import Flask, render_template

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000/'


@app.route('/')
def main_page():
    # Случайные товары
    # random_product = [(id, name, img_href, text), (name, img_href, text), (id, name, img_href, text)]
    random_product = [(1, "Product 1", "static/img/blog/1.jpg", "text 1"),
                      (2, "Product 2", "static/img/blog/2.jpg", "text 2"),
                      (3, "Product 3", "static/img/blog/3.jpg", "text 3")]
    return render_template('index.html', title='SoundRepair', url=WEBSITE_URL, random_product=random_product)


@app.route('/product/')
def product():
    return render_template('product.html', title='SoundRepair')


@app.route('/shop')
def shop():
    # Производители
    # manufacturers = [(name, n), (name, n), (name, n)]
    manufacturers = [("Богдан", 3), ("Андрей", 6), ("Максим", 1)]

    # Максимальная/минимальная цены
    # prices = (max, min)
    prices = (100, 1)

    # Тип товара
    # categories = [(name, n), (name, n), (name, n)]

    # Случайные товары
    # random_product_mat = [[(id, name, img_href, text, price), (id, name, img_href, text, price)],
    #                       [(id, name, img_href, text, price), (id, name, img_href, text, price)],
    #                       [(id, name, img_href, text, price), (id, name, img_href, text, price)]]
    random_product_mat = [[(1, "Product 1", "static/img/blog/1.jpg", "text 1", 100),
                          (2, "Product 2", "static/img/blog/2.jpg", "text 2", 250),
                          (3, "Product 3", "static/img/blog/3.jpg", "text 3", 890)],
                          [(1, "Product 1", "static/img/blog/1.jpg", "text 1", 100),
                           (2, "Product 2", "static/img/blog/2.jpg", "text 2", 250),
                           (3, "Product 3", "static/img/blog/3.jpg", "text 3", 890)],
                          [(1, "Product 1", "static/img/blog/1.jpg", "text 1", 100),
                           (2, "Product 2", "static/img/blog/2.jpg", "text 2", 250),
                           (3, "Product 3", "static/img/blog/3.jpg", "text 3", 890)]
                          ]

    categories = [("Бам-бам громко", 10), ("Бам-бам громко, но не очень", 5), ("Бам-бам не очень громко", 13)]
    return render_template('shop.html', title='SoundRepair', url=WEBSITE_URL, manufacturers=manufacturers,
                           categories=categories, product_mat=random_product_mat)


app.run(host=HOST, port=PORT)
