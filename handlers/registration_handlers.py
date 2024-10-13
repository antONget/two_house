from aiogram import F, Router, Bot

from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, default_state, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove



import keyboards.keyboards as kb
import database.requests as rq


router = Router()

storage = MemoryStorage()

import logging

class RegistrationFSM(StatesGroup):

    state_set_doorway = State()
    state_set_stage = State()
    state_set_flat = State()
    state_end_registration = State()

class UsersFSM(StatesGroup):
    state_aristarch = State()




@router.message(CommandStart())
async def process_start_command(message: Message,  state: FSMContext):
    logging.info(f'process_start_command')
    #await message.answer(text='Приветствие и краткий рассказ для чего нужен бот')
    #user_tg_id = [user.tg_id for user in await rq.get_users()]
    #tg_id = message.chat.id

    # Тут будет проверка на наличие пользователя в базе данных


    chek_in_user_tg_id = await rq.chek_in_user_tg_id(tg_id=message.chat.id)
    await rq.create_guide_news()

    logging.info(f'process_start_command --- chek_in_user_tg_id = {chek_in_user_tg_id}')

    if not chek_in_user_tg_id: # Если пользователя нет в БД
        await message.answer(text='Выберите ваш дом', reply_markup=kb.kb_hause())
        await state.set_state(default_state)
        current_state = await state.get_state()
        logging.info(f'current_state = {current_state}')

    else:
        await process_aristarch(message=message, state=state)

@router.message(F.text.startswith('дом '))
async def set_house(message: Message, state: FSMContext):
    logging.info(f'set_house')
    await state.update_data(house = int(message.text.split(' ')[-1]))
    await message.answer(text=f"Ваш {message.text}?", reply_markup=kb.kb_yes_no())


# ДА ДА ДА
@router.message(F.text.startswith('Да'))
async def yes(message: Message, state: FSMContext):

    current_state = await state.get_state()
    logging.info(f"yes --- current_state = {current_state}")

    if current_state == None: # Если нет состояния, переходим в выбор ПОДЪЕЗДА
        #await state.update_data(house = message.text) # Можно и без этого, тоьлко через меесадж.текст, но для примера
        data_ = await state.get_data()
        number_house = data_['house']
        await message.answer(text=f"№ дома {number_house}\nВыберите номер вашего подъезда", reply_markup=kb.kb_doorway())
        await state.set_state(RegistrationFSM.state_set_doorway)
        logging.info(f"yes --- if current_state == None: --- data_ = {data_} --- current_state = {current_state}")

    elif current_state == RegistrationFSM.state_set_doorway:
        #
        data_ = await state.get_data()
        number_house = data_['house']
        number_doorway = data_['doorway']
        await state.set_state(RegistrationFSM.state_set_stage)
        await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\nВыберете этаж", reply_markup=kb.kb_stage())
        logging.info(f"yes --- elif current_state == RegistrationFSM.state_set_doorway: --- data_ = {data_} --- current_state = {current_state}")

    elif current_state == RegistrationFSM.state_set_stage:

        data_ = await state.get_data()
        number_house = data_['house']
        number_doorway = data_['doorway']
        number_stage = data_['stage']
        await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\n№ этажа {number_stage}\n\nВведите номер квартиры",
                             reply_markup=ReplyKeyboardRemove()) # ожидание ввода данных от пользователя (чило от 1 до 410)
        await state.set_state(RegistrationFSM.state_set_flat)

        logging.info(f"yes --- elif current_state == RegistrationFSM.state_set_doorway: --- data_ = {data_} --- current_state = {current_state}")


# НЕТ НЕТ НЕТ
@router.message(F.text.startswith('Нет'))
async def no(message: Message, state: FSMContext):
    logging.info(f'no')
    #await state.update_data(house = message.text)
    #await message.answer(text=f"Ваш {message.text}?", reply_markup=kb.kb_yes_no())
    current_state = await state.get_state()
    logging.info(f'current_state = {current_state}')

    if current_state == None:
        logging.info(f'if current_state == None: ')
        await state.update_data(house = None)
        await process_start_command(message = message,  state = state)

    elif current_state == RegistrationFSM.state_set_doorway:
        logging.info(f'elif current_state == RegistrationFSM.state_set_doorway: ')
        data_ = await state.get_data()
        number_house = data_['house']
        await state.update_data(doorway = None) # ЗДЕСЬ делаю state.update_data = None
        await message.answer(text=f"№ дома {number_house}\nВыберите номер вашего подъезда", reply_markup=kb.kb_doorway())

    elif current_state == RegistrationFSM.state_set_stage:
        logging.info(f'elif current_state == RegistrationFSM.state_set_stage: ')
        data_ = await state.get_data()
        number_house = data_['house']
        number_doorway = data_['doorway']
        await state.update_data(stage = None) # ЗДЕСЬ делаю state.update_data = None
        await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\nВыберите этаж", reply_markup=kb.kb_stage())

# Этот хэндлер тут вообще не нужен, т.к. нет кнопки НЕТ !!!!!!!!!!!!!А ВОТ И НУЖЕН ЭТО ДРУГАЯ КНОПКА НЕТ, КОТОРАЯ ЕСТЬ!!!!!!!!!!!!!!
    elif current_state == RegistrationFSM.state_end_registration:    ####state_set_flat:# Эта кнопка НЕТ в клавиатуре "НЕТ - ОТПРАВИТЬ"
        logging.info(f"elif current_state == RegistrationFSM.state_set_flat:")
        await state.clear()
        await state.set_state(default_state)
        await process_start_command(message = message, state = state)


@router.message(lambda message: message.text in ('1 подъезд', '2 подъезд', '3 подъезд', '4 подъезд',))
async def set_doorway(message: Message, state: FSMContext):
    logging.info(f'set_doorway')
    current_state = await state.get_state()
    await state.update_data(doorway = int(message.text.split(' ')[0])) # ЗДЕСЬ делаю state.update_data
    data_ = await state.get_data()
    number_hause = data_['house']
    await message.answer(text=f"№ дома {number_hause}\nВаш {message.text}?", reply_markup=kb.kb_yes_no())

    logging.info(f'set_doorway --- state.get_data() = {await state.get_data()}')


@router.message(lambda massage: massage.text in ['1 этаж', '2 этаж', '3 этаж', '4 этаж', '5 этаж', '6 этаж', '7 этаж', '8 этаж',])
async def set_stage(message: Message, state: FSMContext):
    logging.info(f'set_stage')

    await state.update_data(stage = message.text.split(' ')[0])
    data_ = await state.get_data()
    number_house = data_['house']
    number_doorway = data_['doorway']
    await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\nВаш {message.text}?", reply_markup=kb.kb_yes_no())

    logging.info(f'set_doorway --- state.get_data() = {await state.get_data()}')



@router.message(RegistrationFSM.state_set_flat)
async def set_flat(message: Message, state: FSMContext):
    logging.info(f'set_flat')
    data_ = await state.get_data()
    number_house = data_['house']
    number_doorway = data_['doorway']
    number_stage = data_['stage']
    #await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\n№ этажа {number_stage}\nВведите номер квартиры") # ожидание ввода данных от пользователя (чило от 1 до 410)
    if message.text in map(str, list(range(1, 411))):
        await state.update_data(flat = int(message.text.split(' ')[0]))

        await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\n№ этажа {number_stage}\nНомер квартиры {message.text}", reply_markup=kb.kb_no_send())

        logging.info(f'set_flat --- state.get_data() = {await state.get_data()}')
        await state.set_state(RegistrationFSM.state_end_registration)

    else:
        await message.answer(text=f"№ дома {number_house}\n№ подъезда {number_doorway}\n№ этажа {number_stage}\n\n"
                             f"К сожалению в вашем доме такой квартиры нет. \nПовторите ввод")


@router.message(F.text == 'Отправить')
#@router.message(UsersFSM.state_aristarch)
async def process_aristarch(message: Message, bot: Bot, state: FSMContext):
    logging.info(f"process_aristarch")

    data = await state.get_data()
    data_state = await state.get_state()

# Если пользователя нет в БД
    chek_in_user_tg_id = await rq.chek_in_user_tg_id(tg_id=message.chat.id)
    if not chek_in_user_tg_id:
        data |= {'tg_id': message.chat.id}
        if message.chat.username:
            data |= {'username': message.chat.username}
        else:
            data |= {'username': ''}
        logging.info(f"process_aristarch --- data AFTER ADD = {data} --- data_state = {data_state}" )
        await rq.add_new_user(data=data)

    if data_state == RegistrationFSM.state_end_registration: # Состояние после регистрации
        await message.answer(text=f"Спасибо за регистрацию, скоро вас добавят в чат нашего ЖК. Пока вы можете заполнить данные о себе, "
                            f"если посчитаете нужным (для этого необходимо выбрать определенный пункт в меню).\n "
                            f"Также вы можете узнать важные события и новости.")
        #await message.answer(text='Аристарх Вениаминович слушает Вас', reply_markup=kb.kb_aristarch())

    # После регистрации в группу отправляются данные о пользователе
    data_id_group = await rq.get_id_group()
    try:
        await bot.send_message(chat_id=data_id_group, text=f"Пользователь @{message.from_user.username}/{message.chat.id} зарегистрировался в боте")
    except:
        pass



    #data_state == UsersFSM.state_aristarch: # Состояние НЕ ПОСЛЕ регистрации
    await message.answer(text='Аристарх Вениаминович слушает Вас', reply_markup=kb.kb_aristarch())
    if data_state == RegistrationFSM.state_end_registration:
        #await state.set_state(UsersFSM.state_aristarch)
        await state.clear()
