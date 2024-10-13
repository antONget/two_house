from aiogram import F, Router, Bot

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from handlers.registration_handlers import RegistrationFSM, UsersFSM
from filter.user_filter import validate_russian_phone_number
from handlers.registration_handlers import process_aristarch


import keyboards.keyboards as kb
import database.requests as rq
import requests as r
from config_data.config import Config, load_config
config: Config = load_config()


router = Router()

storage = MemoryStorage()

import logging



def get_telegram_user(user_id, bot_token):# user_id id группы
    url = f'https://api.telegram.org/bot{bot_token}/getChat'
    data = {'chat_id': user_id}
    response = r.post(url, data=data)
    return response.json()




@router.message(F.text.startswith('/del_user'))
async def del_user_in_admin_modetg(message: Message, bot: Bot):
    logging.info(f'del_user_in_admin_mode')

    id_group = await rq.get_id_group()
    user_channel_status = await bot.get_chat_member(chat_id=id_group, user_id=message.from_user.id)

    logging.info(f"user_channel_status.status = {user_channel_status.status}")
    # Проверил свой статус - 'member'
    if user_channel_status.status != 'left':
        tg_id = message.text.split(' ')[-1]
        await rq.del_user(tg_id=tg_id)
        await message.answer(text=f"Пользователь с tg_id = {tg_id} удален из базы данных")
    else:
        await message.answer(text='Вам недоступен это функционал')





@router.message(F.text.startswith('/set_group'))
async def change_id_group(message: Message, bot: Bot):
    logging.info(f'change_id_group')

    id_group = message.text.split(' ')[-1]

    user_channel_status = await bot.get_chat_member(chat_id=id_group, user_id=message.from_user.id)

    logging.info(f"user_channel_status.status = {user_channel_status.status}")
    # Проверил свой статус - 'member'
    if user_channel_status.status != 'left':

        try:
            channel_id = int(id_group)
        except:
            await message.answer(text='Пришлите id канала.  ID должно быть целым числом')
            return
        channel = get_telegram_user(channel_id, config.tg_bot.token)# состоит ли бот в это группе
        if 'result' in channel:
            await rq.set_id_group(current_value=channel_id)
            await message.answer(text=f'Вы установили id={channel_id}'
                                    )
        else:
            await message.answer(text=f'id={channel_id} не корректен, или бот не состоит в группе')

    else:
        await message.answer(text='Вам недоступен это функционал')