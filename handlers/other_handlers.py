from aiogram import Router
from aiogram.types import Message
from config_data.config import Config, load_config
from aiogram.types import FSInputFile
config: Config = load_config()
import logging

router = Router()



# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    if message.chat.type == 'private':
        await message.answer(text=f'❌ <b>Неизвестная команда!</b>',
                             parse_mode='html')
                            #f'<i>Вы отправили сообщение напрямую в чат бота,</i>\n'
                            #f'<i>или структура меню была изменена Админом.</i>\n\n'
                            #f'ℹ️ Не отправляйте прямых сообщений боту\n'
                            # f'или обновите Меню, нажав /start')
        if message.video:
            print(message.video.file_id)
        if message.photo:
            print(message.photo[-1].file_id)


        logging.info(f'all_message message.admin')
        if message.text == '/get_logfile':
            logging.info(f'all_message message.admin./get_logfile')
            file_path = "py_log.log"
            await message.answer_document(FSInputFile(file_path))

        elif message.text == '/get_dbfile':
            logging.info(f'all_message message.admin./get_dbfile')
            file_path = "database/db.sqlite3"
            await message.answer_document(FSInputFile(file_path))