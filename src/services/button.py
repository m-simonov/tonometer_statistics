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
            measurement_repository = MeasurementRepository(self.session)
            for i in range(0, len(months), 2):
                pair = months[i:i + 2]
                first_month_number = str(months.index(pair[0]) + 1).zfill(2)
                first_month_number_count = await measurement_repository.count_month_measurements(tid, year, first_month_number)

                second_month_number = str(months.index(pair[1]) + 1).zfill(2)
                second_month_number_count = await measurement_repository.count_month_measurements(tid, year, second_month_number)

                pairs.append(
                    [
                        [
                            pair[0] + f" ({str(first_month_number_count)})",
                            first_month_number,
                        ],
                        [
                            pair[1] + f" ({str(second_month_number_count)})",
                            second_month_number,
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
