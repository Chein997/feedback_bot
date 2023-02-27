import logging
from db_main import BotDB
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

API_TOKEN = ('5681470528:AAHak50w9-H-ySryd_gfoH0rXUmDfh8X5TI')

bot = Bot(token=API_TOKEN)
db = BotDB('feedbacks.db')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    word = State()
    word1 = State()

@dp.message_handler(commands='start')
async def menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    add_feed_markup = KeyboardButton('/Написать_отзыв')
    all_feeds_markup = KeyboardButton('/Все_отзывы')
    markup.add(add_feed_markup, all_feeds_markup)
    await message.answer('menu', reply_markup=markup)

@dp.message_handler(commands='Написать_отзыв')
async def add_word(message: types.Message):
    await Form.word.set()
    await message.reply("Напишите ваш отзыв ниже")


@dp.message_handler(state=Form.word)
async def add_word1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['word'] = message.text
    await Form.next()
    db.add_words(data['word'])
    await message.answer('Отзыв успешно добавлен. Спасибо)')
    await state.finish()

def construct_keyboard(data: tuple, page: int) -> types.InlineKeyboardMarkup:
    length=len(data)
    kb={'inline_keyboard': []}
    buttons=[]
    if page > 1:
        buttons.append({'text':'<-', 'callback_data':f'page_{page-1}'})
    buttons.append({'text':f'{page}/{length}', 'callback_data':'none'})
    if page < length:
        buttons.append({'text':'->', 'callback_data':f'page_{page+1}'})
    kb['inline_keyboard'].append(buttons)
    return kb

@dp.message_handler(commands='Все_отзывы')
async def all_words(message:types.Message):
    data=db.get_words()
    feedback=data[0]
    await message.answer(feedback, reply_markup=construct_keyboard(data, 1))

@dp.callback_query_handler(text_startswith='page_')
async def page(call: types.CallbackQuery):
    page=int(call.data.split('_')[1])
    data=db.get_words()
    feedback=data[page-1]
    await bot.send_message(call.message.chat.id, feedback, reply_markup=construct_keyboard(data, page))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
