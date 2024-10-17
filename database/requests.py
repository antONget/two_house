from database.models import Users, GuideNews, IdGroup
from database.models import async_session
from sqlalchemy import Column, select
from dataclasses import dataclass
from aiogram.types import Message
import logging


async def add_new_user(data:dict):
    logging.info(f'add_new_user')
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == int(data["tg_id"])))
        if not user:
            session.add(Users(**data))

            await session.commit()


async def get_one_user(tg_id: int) -> dict:
    logging.info(f'get_one_user')
    async with async_session() as session:
        data: Users = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        dict_: dict = {}
        if data:
            dict_ |= {'house': data.house}
            dict_ |= {'doorway': data.doorway}
            dict_ |= {'stage': data.stage}
            dict_ |= {'flat': data.flat}
            dict_ |= {'username': data.username}
            dict_ |= {'fullname': data.fullname}
            dict_ |= {'phone': data.phone}
            dict_ |= {'auto1': data.auto1}
            dict_ |= {'auto2': data.auto2}
        return dict_

async def chek_in_user_tg_id(tg_id: int) -> bool:
    logging.info(f'chek_in_user_tg_id')
    async with async_session() as session:
        data: Users = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        logging.info(f'async def chek_in_user_tg_id(tg_id: int) -> bool: --- chek_in_user_tg_id = {data}')
        if data:
            return True
        return False


async def get_users() -> Users:
    logging.info(f'get_users')
    async with async_session() as session:
        return await session.scalars(select(Users))

async def set_data_to_profile(tg_id: int, name_column: str, current_value: str) -> None:
    logging.info(f'set_data_to_profile {current_value}')
    async with async_session() as session:
        data: Users = await session.scalar(select(Users).where(Users.tg_id == tg_id))

        if name_column == 'phone':
            data.phone = current_value
        elif name_column == 'auto1':
            data.auto1 = current_value
        elif name_column == 'auto2':
            data.auto2 = current_value
        elif name_column == 'fullname':
            data.fullname = current_value
        await session.commit()

"""
async def set_data_to_profile_new_version(tg_id: int, column: Column, current_value: int, ) -> Users:
    logging.info(f'set_data_to_profile_new_version')
    async with async_session() as session:
        session = await Users.update.scalar(select(Users).where(Users.tg_id == tg_id))

        if name_column == 'first_aid_kit':
            cell_1.first_aid_kit = current_value
   """

async def create_guide_news():
    logging.info(f'create_guide_news')
    async with async_session() as session:
        line = await session.scalar(select(GuideNews))
        if not line:
            session.add(GuideNews(**{'id': 1, 'name_line': 'guide', 'text': '', 'photo': ''}))
            session.add(GuideNews(**{'id': 2, 'name_line': 'news', 'text': '', 'photo': ''}))

            await session.commit()

async def get_guide_news(id: int) -> dict:
    logging.info(f'get_guide_news')
    async with async_session() as session:
        data: GuideNews = await session.scalar(select(GuideNews).where(GuideNews.id == id))

        dict_: dict = {}
        dict_ |= {'name_line': data.name_line}
        dict_ |= {'text': data.text}
        dict_ |= {'photo': data.photo}

        return dict_


async def set_change_guide_news(id: int, name_column: str, current_value: str) -> None:
    logging.info(f'set_change_guide_news --- id = {id} --- name_column = {name_column} --- current_value = {current_value}')
    async with async_session() as session:
        data: GuideNews = await session.scalar(select(GuideNews).where(GuideNews.id == id))

        if name_column == 'text':
            data.text = current_value
        elif name_column == 'photo':
            data.photo = current_value

        await session.commit()

async def get_Users() -> Users:
    async with async_session() as session:
        return await session.scalars(select(Users))


async def del_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        if user:
            await session.delete(user)
            await session.commit()

async def get_id_group() -> int:
    logging.info(f'get_id_group')
    async with async_session() as session:
        data: IdGroup = await session.scalar(select(IdGroup).where(IdGroup.id == 1))
        int_ = data.id_group
        return int_

async def set_id_group(current_value: int) -> None:
    logging.info(f'set_id_group(current_value: int) = {current_value}')
    async with async_session() as session:
        data: IdGroup = await session.scalar(select(IdGroup).where(IdGroup.id == 1))
        data.id_group = current_value

        await session.commit()