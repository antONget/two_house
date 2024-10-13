from aiogram import Router
from aiogram.types import Message



router = Router()



# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    if message.chat.type == 'private':
        await message.answer(text=f'❌ <b>Неизвестная команда!</b>')
                            #f'<i>Вы отправили сообщение напрямую в чат бота,</i>\n'
                            #f'<i>или структура меню была изменена Админом.</i>\n\n'
                            #f'ℹ️ Не отправляйте прямых сообщений боту\n'
                            # f'или обновите Меню, нажав /start')
        if message.video:
            print(message.video.file_id)
        if message.photo:
            print(message.photo[-1].file_id)
