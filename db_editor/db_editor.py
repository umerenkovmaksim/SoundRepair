import sqlite3
import sys

import qtmodern.styles
import qtmodern.windows

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QTime, QDate, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGroupBox, QVBoxLayout, QCheckBox, QWidget, \
    QGridLayout, QDialog, QInputDialog, QSizeGrip


class MainWindow(QMainWindow):
    con = sqlite3.connect("../db/data.db")
    cur = con.cursor()

    def __init__(self):
        super().__init__()
        uic.loadUi('db_editor_ui.ui', self)
        self.setWindowTitle("Редактор db")

        self.pushButton_OK.clicked.connect(self.save)
        self.pushButton_Cancel.clicked.connect(self.cancel)

    def save(self):
        name = self.lineEdit_name.text().strip().lower().capitalize()
        short_description = self.lineEdit_short_description.text().strip().lower().capitalize()
        description = self.textEdit_description.toPlainText()
        price = int(self.lineEdit_price.text())
        sale = int(self.lineEdit_sale.text()) if self.lineEdit_sale.text() else 0
        manufacturer = self.lineEdit_manufacturer.text().strip().lower().capitalize()
        categories = "&".join(
            list(map(lambda x: x.strip().lower().capitalize(), self.textEdit_categories.toPlainText().split("\n"))))

        # Потом преределать
        img_href = "static/img/products/1.jpg"

        MainWindow.cur.execute(f"""INSERT INTO 
            products(name, short_description, description, img_href, manufacturer, categories, price, sale) 
             VALUES('{name}', '{short_description}', '{description}', '{img_href}', '{manufacturer}', '{categories}',
                    {price}, {sale})""")
        self.con.commit()

        self.cancel()

    def cancel(self):
        self.lineEdit_name.setText("")
        self.lineEdit_short_description.setText("")
        self.textEdit_description.setPlainText("")
        self.lineEdit_price.setText("")
        self.lineEdit_sale.setText("")
        self.lineEdit_manufacturer.setText("")
        self.textEdit_categories.setPlainText("")

        # Потом преределать
        img_href = "static/img/products/1.jpg"


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()

    qtmodern.styles.dark(app)

    mw = qtmodern.windows.ModernWindow(ex)
    mw.move(200, 200)

    mw.show()
    sys.excepthook = except_hook
    app.exec_()
