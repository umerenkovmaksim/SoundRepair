from flask import Flask, render_template

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000
WEBSITE_URL = 'http://127.0.0.1:5000/'


@app.route('/')
def main_page():
    return render_template('index.html', title='SoundRepair')


app.run(host=HOST, port=PORT)
