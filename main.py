import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import registration_handlers, other_handlers, users_handlers, admin_handlers
from handlers.registration_handlers import storage
from database.models import async_main


logger = logging.getLogger(__name__)



async def main():
    await async_main()


    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')


    logger.info('Starting bot')


    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    dp.include_router(registration_handlers.router)
    dp.include_router(users_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())