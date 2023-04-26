import datetime

from functions import select_from_db, recycle_list


def order(name, phone_number, list_id):
    message_text = f"{name} хочет совершить заказ.\n\n"

    total_price = 0
    for product_id in list_id:
        colums_name = "name, price, short_description, sale"
        filters = f"id == {product_id}"

        product_data = select_from_db(colums_name=colums_name, filters=filters)

        product_data = recycle_list("name, price, short_description, sale",
                                    "name, short_description, price_with_sale_or_price, price, sale",
                                    product_data)

        product_name, product_description, product_price, price_out_sale, sale = product_data[0]
        message_text += f"{product_name}\n" \
                        f"{product_description}\n" \
                        f"{product_price}₽" \
                        f"{f' ({price_out_sale}₽, {sale}%)' if price_out_sale != product_price else ''}\n\n"


        total_price += product_price
    message_text += f"Итого: {total_price}₽\n"
    message_text += f"Номер {name} {phone_number}\nВремя заказа {datetime.datetime.now().strftime('%H:%M %d.%m.%Y')}"

    print(message_text)
