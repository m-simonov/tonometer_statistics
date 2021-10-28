import db


def determine_the_time(hour: int):
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