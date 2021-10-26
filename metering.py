import datetime

import pytz
import db


msk_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
hour = int(msk_time.strftime('%H'))
date_now = msk_time.date()

def determine_the_time():
    if 0 < hour < 12:
        column = 'morning'
    elif 12 < hour < 18:
        column = 'afternoon'
    else:
        column = 'evening'
    return column

def write_to_db(user: str, metering_result: str, column: str):
    number_of_meterings = db.count_meterings(user, date_now)
    if number_of_meterings == 3:
        text = 'Все данные на сегодня заполнены'
    elif number_of_meterings == 0:
        db.insert(
            'meterings',
            {
                'user': user,
                'date': date_now,
                column: metering_result,
            }
        )
        text = f"Результат утреннего замера '{metering_result}' записан"
    else:
        db.update_metering(
            user,
            date_now,
            column,
            metering_result,
        )
        text = f"Результат замера '{metering_result}' записан"
    return text