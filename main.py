from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from processorMenu import *
from commonData import *
from kbs import *
from testBot import *
from managerQR import *
 
'''
from langchain.chat_models import GigaChat
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Авторизация в сервисе GigaChat
chat = GigaChat(credentials="MTI3YzYzN2ItOGIwOC00NDNiLWJmOGItOGM3N2NmNTYxMjZhOjVjYWYxMjljLWJlMjEtNDQ4Yi05M2Q5LTI1N2ZhMmEzMmU2Mw==", verify_ssl_certs=False)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]
while(True):
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    print("Bot: ", res.content)
'''

bot = Bot(token=mainConst.API_TOKEN)
# storage=MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())
# dp.middleware.setup(LoggingMiddleware())

menu = processorMenu()

class UserState(StatesGroup):
    name = State()
    address = State()

# Начаало
@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message) -> None:
   userCurrent = userDB(True)
   userInfo, isNew = userCurrent.getUserInfo(msg)

   # if userInfo.phone is None:
   #    kb, title, current_menu = kbs.get_kb_phone(menu, msg)
   # else:
   #    kb, title, current_menu = kbs.get_kb(menu, msg, userInfo, isNew)
   kb, title, current_menu = kbs.get_kb(menu, msg, userInfo, isNew)
   
   if kb is not None:
      userInfo.current_menu = current_menu
      userInfo.save()
      await msg.answer(title, reply_markup=kb)

# @dp.message_handler(content_types=types.ContentType.CONTACT, state=Form.contacts)
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contacts(msg: types.Message, state: FSMContext):
   userCurrent = userDB(True)
   userInfo, isNew = userCurrent.getUserInfo(msg)
   userInfo.phone = msg.contact.phone_number
   userInfo.save()
   await kbs.get_kb_by_idmenu(menu, msg, 'Registry')
   # await msg.answer(f"Ваш номер: {msg.contact.phone_number}", reply_markup=types.ReplyKeyboardRemove())

# тестирование 
@dp.message_handler(commands=['test'])
async def cmd_cancel(msg: types.Message) -> None:
   await testBotUtils.testManager(msg)

# остановка процесса
@dp.message_handler(commands=['stop'])
async def cmd_cancel(msg: types.Message) -> None:
   testBotUtils.stop = True

# регистрация ассистента
@dp.message_handler(commands=['reg'])
async def user_register(msg: types.Message):
   await kbs.get_kb_by_idmenu(menu, msg, 'Registry')

# включение режима информирования
@dp.message_handler(commands=['info'])
async def user_infoMode(msg: types.Message):
   await kbs.setInfoMode(msg)

# передача параметров пользователю
@dp.message_handler(commands=['set'])
async def user_setParam(msg: types.Message):
   await kbs.setParam(msg)

# передача чеков на распознание (DOCUMENT)
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def scan_message(msg: types.Message):
   await managerQR.testPhotoAsDocument(msg)
    
# передача чеков на распознание (photo)
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(msg):
   await kbs.sendMediaData(menu, msg)
   # await managerQR.testPhoto(msg)

#     # Перебираем фотографии и обрабатываем их
#     for photo in photos:
#         # Скачиваем фотографию
#         await photo.download()
#         # Обрабатываем фотографию (например, сохраняем ее в базу данных)
#         process_photo(photo.file)       

'''
@dp.message_handler(commands=['reg'])
async def user_register(message: types.Message):
    await message.answer("Введите своё имя")
    await UserState.name.set()
    
@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично! Теперь введите ваш адрес.")
    await UserState.next() # либо же UserState.address.set()
    
@dp.message_handler(state=UserState.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data['username']}\n"
                         f"Адрес: {data['address']}")

    await state.finish()
'''    
# test end
        
# @dp.message_handler(state='*', commands=['setstate'])
# async def process_setstate_command(message: types.Message):
#     argument = message.get_args()
#     state = dp.current_state(user=message.from_user.id)
 
@dp.message_handler()
async def echo(msg: types.Message):
   # userCurrent = userDB(True)
   # userInfo, isNew = userCurrent.getUserInfo(msg)
   # await kbs.get_next_kb(menu, msg, userInfo, isNew)

   # await bot.sendp.send_p.answer(msg.text)

   await kbs.get_next_kb(menu, msg, bot)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)