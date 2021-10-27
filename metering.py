import db


def determine_the_time(hour: int):
    if 0 < hour < 12:
        column = 'morning'
    elif 12 < hour < 18:
        column = 'afternoon'
    else:
        column = 'evening'
    return column

def write_to_db(user: str, date: str, column: str, metering_result: str):
    number_of_meterings = 3 - db.read_meterings_by_date(user, date).count(None)
    if number_of_meterings == 3:
        text = 'Все данные на сегодня заполнены'
    elif number_of_meterings == 0:
        db.insert(
            'meterings',
            {
                'user': user,
                'date': date,
                column: metering_result,
            }
        )
        text = f"Результат утреннего замера '{metering_result}' записан"
    else:
        db.update_metering(
            user,
            date,
            column,
            metering_result,
        )
        text = f"Результат замера '{metering_result}' записан"
    return text