import logging
import re
from aiogram.filters import BaseFilter
from aiogram.types import Message



def validate_russian_phone_number(phone_number):
    logging.info(f'validate_russian_phone_number')
    # Паттерн для российских номеров телефона
    # Российские номера могут начинаться с +7, 8, или без кода страны
    pattern = re.compile(r'^(\+7|8|7)?(\d{10})$')
    # Проверка соответствия паттерну
    match = pattern.match(phone_number)
    return bool(match)


async def type_chat(message: Message) -> bool:
    logging.info('check_manager')
    if message.chat.type == 'private':
        return True
    else:
        return False


class IsChatPrivate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await type_chat(message=message)