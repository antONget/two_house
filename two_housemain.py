import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import registration_handlers, other_handlers, users_handlers, admin_handlers
from handlers.registration_handlers import storage
from database.models import async_main

from aiogram.types import ErrorEvent
from aiogram.types import FSInputFile
import traceback

logger = logging.getLogger(__name__)



async def main():
    await async_main()


    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')


    logger.info('Starting bot')


    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
    )
    dp = Dispatcher(storage=storage)

    dp.include_router(registration_handlers.router)
    dp.include_router(users_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)

    @dp.error()
    async def error_handler(event: ErrorEvent):
        logger.critical("Критическая ошибка: %s", event.exception, exc_info=True)
        await bot.send_message(chat_id=config.tg_bot.support_id,
                               text=f'{event.exception}')
        formatted_lines = traceback.format_exc()
        text_file = open('error.txt', 'w')
        text_file.write(str(formatted_lines))
        text_file.close()
        await bot.send_document(chat_id=config.tg_bot.support_id,
                                document=FSInputFile('error.txt'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
