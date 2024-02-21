from datetime import datetime
from aiogram.types.inline_keyboard import (InlineKeyboardButton,
                                           InlineKeyboardMarkup)

from db.repositories.measurement import MeasurementRepository
from keyboards.inline.callback_data import by_month_callback
from services.base import AbstractService


class ButtonService(AbstractService):
    async def get_by_month_reply_markup(self, tid: int):
        year = datetime.now().year
        months = [
            "Январь", "Февраль", "Март", "Апрель",
            "Май", "Июнь", "Июль", "Август",
            "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]

        pairs = []
        async with self.session.begin():
            year_stats = await MeasurementRepository(self.session).count_months_measurements_all(tid, year)
            month_count_mapping = {i["month"]: i["count"] for i in year_stats}
            for i in range(0, len(months), 2):
                pair = months[i:i + 2]
                first_month_number = months.index(pair[0]) + 1
                first_month_number_count = month_count_mapping.get(first_month_number, 0)

                second_month_number = months.index(pair[1]) + 1
                second_month_number_count = month_count_mapping.get(second_month_number, 0)

                pairs.append(
                    [
                        [
                            pair[0] + f" ({str(first_month_number_count)})",
                            str(first_month_number).zfill(2),
                        ],
                        [
                            pair[1] + f" ({str(second_month_number_count)})",
                            str(second_month_number).zfill(2),
                        ]
                    ]
                )

        keyboard = [
            [
                InlineKeyboardButton(text=pair[0][0], callback_data=by_month_callback.new(month=pair[0][1])),
                InlineKeyboardButton(text=pair[1][0], callback_data=by_month_callback.new(month=pair[1][1])),
            ] for pair in pairs
        ]

        return InlineKeyboardMarkup(inline_keyboard=keyboard)
