import datetime

import pytz

import db


def determine_the_time():
    msk_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    hour = int(msk_time.strftime('%H'))
    if 0 < hour < 12:
        column = 'morning'
    elif 12 <= hour < 18:
        column = 'afternoon'
    else:
        column = 'evening'
    return column

def write_to_db(user: str, date: str, column: str, metering_result: str):
    today_meterings = db.read_meterings_by_date(user, date)
    if not today_meterings:
        db.insert(
            'meterings',
            {
                'user': user,
                'date': date,
                column: metering_result,
            }
        )
        text = f"Результат замера '{metering_result}' записан"
    elif 3 - today_meterings.count(None) == 3:
        text = 'Все данные на сегодня заполнены'
    else:
        db.update_metering(
            user,
            date,
            column,
            metering_result,
        )
        text = f"Результат замера '{metering_result}' записан"
    return text

def show_today_meterings(user: str, date: str):
    meterings = db.read_meterings_by_date(user, date)
    if meterings:
        morning = meterings[0]
        afternoon = meterings[1]
        evening = meterings[2]
        text = (
            f"Дата: {date}\n\n"
            f"Утро: {morning}\n"
            f"День: {afternoon}\n"
            f"Вечер: {evening}"
        )
    else:
        text = "Сегодняшние замеры еще не внесены"
    return text

def show_monthly_meterings(user: str, year: str, month: str):
    this_month = db.read_monthly_meterings(user, year, month)
    text = []
    for metering in this_month:
        text.append(
            f"Дата: {metering[2]}\n"
            f"Утро: {metering[3]}\n"
            f"День: {metering[4]}\n"
            f"Вечер: {metering[5]}\n\n"
        )
    if text:
        return ''.join(text)
    else:
        return "Нет данных"