from aiogram import F, Router, Bot

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from handlers import registration_handlers as hrh
from filter.user_filter import validate_russian_phone_number
from handlers.registration_handlers import process_aristarch
from filter.user_filter import IsChatPrivate


import keyboards.keyboards as kb
import database.requests as rq


router = Router()
router.message.filter(IsChatPrivate())
storage = MemoryStorage()

import logging

class SetProfileFSM(StatesGroup):
    state_set_phone = State()
    state_set_auto1 = State()
    state_set_auto2 = State()
    state_set_fullname = State()

class ChangeGuideNewsFSM(StatesGroup):
    state_set_guide = State()
    state_set_news = State()

class SearchFlatAutoFSM(StatesGroup):
    state_search_flat = State()
    state_search_auto = State()


@router.message(F.text == 'Мой профиль')
async def my_profile(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка нажатия клавиши 'Мой профиль'
    :param message:
    :param state:
    :return:
    """
    logging.info(f'my_profile')
    if not await rq.get_one_user(tg_id=message.chat.id):
        await hrh.process_start_command(message=message, state=state, bot=bot)
        return
    data = await rq.get_one_user(tg_id=message.chat.id)
    await message.answer(text=
                         f"№ дома - {data['house'] if data['house'] else 'нет данных'}\n"
                         f"№ подъезда - {data['doorway'] if data['doorway'] else 'нет данных'}\n"
                         f"№ этажа - {data['stage'] if data['stage'] else 'нет данных'}\n"
                         f"№ квартиры - {data['flat'] if data['flat'] else 'нет данных'}\n"
                         f"Ссылка на пользователя - {data['username'] if data['username'] else 'нет данных'}\n"
                         f"ФИО - {data['fullname'] if data['fullname'] else 'нет данных'}\n"
                         f"Телефон - {data['phone'] if data['phone'] else 'нет данных'}\n"
                         f"1 Автомобиль - {data['auto1'] if data['auto1'] else 'нет данных'}\n"
                         f"2 Автомобиль - {data['auto2'] if data['auto2'] else 'нет данных'}\n",
                         reply_markup=kb.kb_inline_set_my_profile()
                         )

@router.callback_query(F.data.startswith('set_'))
async def process_set_state_to_add_someone(clb: CallbackQuery, state: FSMContext):
    logging.info(f'process_set_state_to_add_someone')
    clb_name = clb.data.split('_')[-1]
    if clb_name == 'phone':
        logging.info(f"process_set_state_to_add_someone --- if clb_name == 'phone':")
        await state.set_state(SetProfileFSM.state_set_phone)
        logging.info(f"process_set_state_to_add_someone --- if clb_name == 'phone': --- AFTER set state")
        await clb.message.answer(text='Введите ваш номер телефона или поделитесь им, воспользовавшись кнопкой внизу 👇',
                                 reply_markup=kb.kb_phone())
        await clb.answer()
        logging.info(f"process_set_state_to_add_someone --- if clb_name == 'phone': --- AFTER set state --- after keyboard")
    elif clb_name == 'auto1':
        logging.info(f"process_set_state_to_add_someone --- if clb_name == 'auto1':")
        await state.set_state(SetProfileFSM.state_set_auto1)
        await clb.message.answer(text='Пришлите государственый регистрационный знак вашего авто')
        await clb.answer()
    elif clb_name == 'auto2':
        logging.info(f"process_set_state_to_add_someone --- if clb_name == 'auto2':")
        await state.set_state(SetProfileFSM.state_set_auto2)
        await clb.message.answer(text='Пришлите государственый регистрационный знак вашего авто')
        await clb.answer()
    elif clb_name == 'fullname':
        logging.info(f"process_set_state_to_add_someone --- if clb_name == 'fullname':")
        await state.set_state(SetProfileFSM.state_set_fullname)
        await clb.message.answer(text='Укажите ваше Фамилию, Имя, Отчество')
        await clb.answer()


@router.message(SetProfileFSM.state_set_phone)
async def process_add_phone(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'process_add_phone')

    # если номер телефона отправлен через кнопку "Поделится"
    if message.contact:
        logging.info(f'process_add_phone --- if message.contact:')
        phone = str(message.contact.phone_number)
        logging.info(f'process_add_phone --- if message.contact: --- phone = {phone}')
    # если введен в поле ввода
    else:
        phone = message.text
        logging.info(f'process_add_phone --- else: phone = message.text = {phone}')
        # проверка валидности отправленного номера телефона, если не валиден просим ввести его повторно
        if not validate_russian_phone_number(phone):
            await message.answer(text=f"Введенный номер не прошел проверку. Номер должен содержать только цифры "
                                 f"(например: +79441234567)\n\n"
                                 f"Введите ваш номер телефона или поделитесь им, воспользовавшись кнопкой внизу 👇")#,reply_markup=kb.kb_phone())
            return




    await rq.set_data_to_profile(tg_id=message.chat.id, name_column='phone', current_value=phone)
    await message.answer(text='Благодарю!', reply_markup=kb.kb_aristarch())
    await state.clear()
    await state.set_state(state=None)
    await my_profile(message=message, state=state, bot=bot)

@router.message(SetProfileFSM.state_set_auto1)
async def process_add_auto1(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'process_add_auto1 --- await state.get_state() = {await state.get_state()}')
    await rq.set_data_to_profile(tg_id=message.chat.id, name_column='auto1', current_value=message.text)
    await state.clear()
    await message.answer(text='Благодарю!', reply_markup=kb.kb_aristarch())
    await my_profile(message=message, state=state, bot=bot)
    await state.set_state(state=None)

@router.message(SetProfileFSM.state_set_auto2)
async def process_add_auto2(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'process_add_auto2')
    await rq.set_data_to_profile(tg_id=message.chat.id, name_column='auto2', current_value=message.text)
    await state.clear()
    await message.answer(text='Благодарю!', reply_markup=kb.kb_aristarch())
    await my_profile(message=message, state=state, bot=bot)
    await state.set_state(state=None)

@router.message(SetProfileFSM.state_set_fullname)
async def process_add_fullname(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'process_add_fullname')
    await rq.set_data_to_profile(tg_id=message.chat.id, name_column='fullname', current_value=message.text)
    await state.clear()
    await message.answer(text='Благодарю!', reply_markup=kb.kb_aristarch())
    await my_profile(message=message, state=state, bot=bot)
    await state.set_state(state=None)


@router.message(lambda message: message.text in ['Новости', 'Справочник'])
async def process_show_guide_news(message: Message, bot: Bot, state: FSMContext):
    logging.info(f'process_show_guide_news')
    if not await rq.get_one_user(tg_id=message.chat.id):
        await hrh.process_start_command(message=message, state=state, bot=bot)
        return
    id_group = await rq.get_id_group()
    user_channel_status = await bot.get_chat_member(chat_id=id_group, user_id=message.from_user.id)
    if user_channel_status.status == 'left':
        data_guide = await rq.get_guide_news(1)
        data_news = await rq.get_guide_news(2)
        logging.info(f"data_guide = {data_guide} --- data_news = {data_news} --- message.chat.id = {message.chat.id}")
        if not data_guide or not data_news:
            await message.answer(text='В разделе нет информации')
            return
        if message.text == 'Справочник':
            if data_guide['photo']:
                if data_guide['text']:# если есть фотография и текст
                    await bot.send_photo(chat_id=message.chat.id, photo=data_guide['photo'], caption=data_guide['text'])
                else: # если есть только фотография
                    await bot.send_photo(chat_id=message.chat.id, photo=data_guide['photo'])
            else:
                if data_guide ['text']: # если есть только текст
                    await message.answer(text=data_guide['text'])
                else: # если нет ничего
                    await message.answer(text='В разделе "Справочник" нет информации')


        if message.text == 'Новости':
            if data_news['photo']:
                if data_news['text']:# если есть фотография и текст
                    await bot.send_photo(chat_id=message.chat.id, photo=data_news['photo'], caption=data_news['text'])
                else: # если есть только фотография
                    await bot.send_photo(chat_id=message.chat.id, photo=data_news['photo'])
            else:
                if data_news ['text']: # если есть только текст
                    await message.answer(text=data_news['text'])
                else: # если нет ничего
                    await message.answer(text='В разделе "Новости" нет информации')

    # id_group = await rq.get_id_group()
    # user_channel_status = await bot.get_chat_member(chat_id=id_group, user_id=message.from_user.id)
    #
    # logging.info(f"user_channel_status.status = {user_channel_status.status}")
    # # Проверил свой статус - 'member'
    # if user_channel_status.status != 'left':
    else:
        if message.text == 'Новости':
            await message.answer(text='Хотите изменить контент в разделе?', reply_markup=kb.kb_inline_yes_no(line_name='news'))

        elif message.text == 'Справочник':
            await message.answer(text='Хотите изменить контент в разделе?', reply_markup=kb.kb_inline_yes_no(line_name='guide'))

    # else:
    #     await message.answer(text='Функционал доступен только администраторам')
    #     await process_aristarch(message=message, state=state, bot=bot)




# нажатие на Инлайн кнопку НЕТ в админ режиме для отказа от редактирования новостей и справочника
@router.callback_query(F.data.startswith('no_'))
async def process_no_change_guide_or_news_go_to_aristarch(clb: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(f'process_no_change_guide_or_news_go_to_aristarch')
    await process_aristarch(message=clb.message, state=state, bot=bot)


# нажатие на Инлайн кнопку ДА в админ режиме для редактирования новостей и справочника
@router.callback_query(F.data.startswith('yes_'))
async def process_yes_change_guide_or_news(clb: CallbackQuery, state: FSMContext):
    logging.info(f'process_yes_change_guide_or_news')
    # из какого раздела пришли нажали на инлайн кнопку ДА: из новостей = _news или из справочника = _guide
    clb_button = clb.data.split('_')[-1]
    if clb_button == 'guide':
        await state.set_state(ChangeGuideNewsFSM.state_set_guide)
    elif clb_button == 'news':
        await state.set_state(ChangeGuideNewsFSM.state_set_news)
    await clb.message.answer(text='Пришлите новый контент для раздела')
    await clb.answer()



# ловим введенные сообщения для изменения новостей или справочника
@router.message(ChangeGuideNewsFSM.state_set_news)
@router.message(ChangeGuideNewsFSM.state_set_guide)
async def process_capture_change_guide_news(message: Message, bot: Bot, state: FSMContext):
    logging.info(f'process_capture_change_guide_news')

    # метод для вывода в терминал апдейта типа message
    #print(message.model_dump_json(indent=4, exclude_none=True))

    logging.info(f"process_capture_change_guide_news --- \n"
                 f"--- message.text {message.text if message.text else 'ОТСУТСТВУЕТ'} ---  \n"
                 f"--- message.photo[-1].file_id = {message.photo[-1].file_id if message.photo else 'ОТСУТСТВУЕТ'} --- \n"
                 f"--- caption = {message.caption if message.caption else 'ОТСУТСТВУЕТ'}"
                 f"state = {await state.get_state()}")

    id_table_guide_news: int = 0
    if await state.get_state() == ChangeGuideNewsFSM.state_set_guide:
        id_table_guide_news = 1
    elif await state.get_state() == ChangeGuideNewsFSM.state_set_news:
        id_table_guide_news = 2

    # если только текст
    if message.text and not message.photo:
        text = message.text
        await rq.set_change_guide_news(id=id_table_guide_news, name_column='text', current_value=text)
        await rq.set_change_guide_news(id=id_table_guide_news, name_column='photo', current_value='')

    # если только фото
    elif message.photo and not message.text:
        photo = message.photo[-1].file_id
        await rq.set_change_guide_news(id=id_table_guide_news, name_column='photo', current_value=photo)
        await rq.set_change_guide_news(id=id_table_guide_news, name_column='text', current_value='')

    # если и текст и фото
    elif message.photo and message.text:
        photo = message.photo[-1].file_id
        text = message.text
        await rq.set_change_guide_news(id=id_table_guide_news, name_column='photo', current_value=photo)
        await rq.set_change_guide_news(id=id_table_guide_news, name_column='text', current_value=text)

    await message.answer(text='Контент в разделе обновлен')
    await state.clear()
    await process_aristarch(message=message, state=state, bot=bot)




@router.message(F.text == 'Поиск')
async def process_search(message: Message, bot: Bot, state: FSMContext):
    logging.info(f'process_search')
    if not await rq.get_one_user(tg_id=message.chat.id):
        await hrh.process_start_command(message=message, state=state, bot=bot)
        return
    # Проверка статуса пользователя
    id_group = await rq.get_id_group()
    user_channel_status = await bot.get_chat_member(chat_id=id_group, user_id=message.from_user.id) #message.chat.id

    logging.info(f"user_channel_status.status = {user_channel_status.status}")
    # Проверил свой статус - 'member'
    if user_channel_status.status != 'left':
        await message.answer(text='Укажите номер квартиры или авто для поика',
                             reply_markup=kb.kb_inline_search())
    else:
        await message.answer(text='Функционал доступен только администраторам')


@router.callback_query(F.data.startswith('search_'))
async def process_push_clb_flat_or_auto(clb: CallbackQuery, state: FSMContext):
    logging.info(f'process_push_clb_flat_or_auto --- clb.data = {clb.data}')
    clb_button = clb.data.split('_')[-1]
    if clb_button == 'flat':
        await state.set_state(SearchFlatAutoFSM.state_search_flat)
        await clb.message.answer(text='Пришлите номер квартиры')
        await clb.answer()

    elif clb_button == 'auto':
        await state.set_state(SearchFlatAutoFSM.state_search_auto)
        await clb.message.answer(text='Пришлите ГРЗ авто')
        await clb.answer()


@router.message(SearchFlatAutoFSM.state_search_flat)
@router.message(SearchFlatAutoFSM.state_search_auto)
async def process_answer_to_search(message: Message, bot: Bot, state: FSMContext):
    logging.info(f'process_capture_change_guide_news')
    list_id_user_flat = [[user.tg_id, user.flat] for user in await rq.get_users()]
    list_id_auto = [[user.tg_id, user.auto1, user.auto2] for user in await rq.get_users()]


    input_data = message.text
    flag = True
    if await state.get_state() == SearchFlatAutoFSM.state_search_flat:
        for item in list_id_user_flat:
            if int(input_data) == item[1]:
                flag = False
                data = await rq.get_one_user(item[0])
                logging.info(f'data = {data}')
                await message.answer(text=
                             f"№ дома - {data['house'] if data['house'] else 'нет данных'}\n"
                             f"№ подъезда - {data['doorway'] if data['doorway'] else 'нет данных'}\n"
                             f"№ этажа - {data['stage'] if data['stage'] else 'нет данных'}\n"
                             f"№ квартиры - {data['flat'] if data['flat'] else 'нет данных'}\n"
                             f"Ссылка на пользователя - {data['username'] if data['username'] else 'нет данных'}\n"
                             f"ФИО - {data['fullname'] if data['fullname'] else 'нет данных'}\n"
                             f"Телефон - {data['phone'] if data['phone'] else 'нет данных'}\n"
                             f"1 Автомобиль - {data['auto1'] if data['auto1'] else 'нет данных'}\n"
                             f"2 Автомобиль - {data['auto2'] if data['auto2'] else 'нет данных'}\n",
                             reply_markup=kb.kb_inline_set_my_profile()
                             )
        if flag:
            await message.answer(text='По вашему запросу данные не найдены')

    elif await state.get_state() == SearchFlatAutoFSM.state_search_auto:
        for item in list_id_auto:
            if input_data == item[1] or input_data == item[2]:
                flag = False
                data = await rq.get_one_user(tg_id=item[0])
                logging.info(f'data = {data}')
                await message.answer(text=
                             f"№ дома - {data['house'] if data['house'] else 'нет данных'}\n"
                             f"№ подъезда - {data['doorway'] if data['doorway'] else 'нет данных'}\n"
                             f"№ этажа - {data['stage'] if data['stage'] else 'нет данных'}\n"
                             f"№ квартиры - {data['flat'] if data['flat'] else 'нет данных'}\n"
                             f"Ссылка на пользователя - {data['username'] if data['username'] else 'нет данных'}\n"
                             f"ФИО - {data['fullname'] if data['fullname'] else 'нет данных'}\n"
                             f"Телефон - {data['phone'] if data['phone'] else 'нет данных'}\n"
                             f"1 Автомобиль - {data['auto1'] if data['auto1'] else 'нет данных'}\n"
                             f"2 Автомобиль - {data['auto2'] if data['auto2'] else 'нет данных'}\n",
                             reply_markup=kb.kb_inline_set_my_profile()
                             )
        if flag:
            await message.answer(text='По вашему запросу данные не найдены')
    await state.set_state(state=None)