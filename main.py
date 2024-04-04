from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from pyowm import OWM
import requests
import asyncio
import datetime


API_TOKEN = '7178835099:AAF6ohabJTm9Fvaw-QZYrLFRBqjjiOXNMzg'
OWM_API_KEY = 'ff46be9524460eda251605d478dc6dad'


HELP_COMMAND = """
/help - список команд
/start - начать работу
/schedule - расписание пар
/weather - прогноз погоды
/rate - курсы валют
"""

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton('/help')
b2 = KeyboardButton('/weather')
b3 = KeyboardButton('/rate')
b4 = KeyboardButton('/schedule')
kb.add(b4).add(b2).insert(b1).insert(b3)



bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

owm = OWM(OWM_API_KEY)
mgr = owm.weather_manager()

class ScheduleStates(StatesGroup):
    day_of_week = State()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Список команд: /help", reply_markup=kb)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text = HELP_COMMAND)
    await message.delete()


@dp.message_handler(commands=['weather'])
async def send_weather(message: types.Message):
    observation = mgr.weather_at_place('Moscow,RU')
    w = observation.weather
    temp = w.temperature('celsius')['temp']
    detailed_status = w.detailed_status
    await message.reply(f"Сейчас в Москве:\n{detailed_status}.\nТемпература: {temp}°C.")

# Обработчик команды /course
@dp.message_handler(commands=['rate'])
async def send_course(message: types.Message):
    usd_rate = get_currency_rate('USD')
    eur_rate = get_currency_rate('EUR')
    gbp_rate = get_currency_rate('GBP')

    response_text = f"Курс валют:\nUSD: {usd_rate} руб.\nEUR: {eur_rate} руб.\nGBP: {gbp_rate} руб."

    await message.answer(response_text, parse_mode=ParseMode.HTML)


@dp.message_handler(commands='schedule')
async def schedule_command(message: types.Message):
    today = datetime.datetime.today().weekday()  # current day of the week (0 - Monday, 6 - Sunday)
    image_number = today + 1  # (1 - Monday, 7 - Sunday)
    if (image_number == 2) or (image_number == 4) or (image_number == 7):
        if image_number == 2:
            await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/JmyyjHR")
        elif image_number == 4:
            await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/XkUGj69")
        elif image_number == 7:
            await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/uaIpUUO")
    else:
        day = datetime.datetime.now()
        week_number = (day.day - 1) // 7 + 1
        if week_number % 2 == 0:
            if image_number == 1:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/FHZzKlD")
            elif image_number == 3:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/8vhoFQf")
            elif image_number == 5:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/QQI8LJW")
            elif image_number == 6:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/hWE7tpU")
        else:
            if image_number == 1:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/XChTN89")
            elif image_number == 3:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/uInBObA")
            elif image_number == 5:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/roc0PBQ")
            elif image_number == 6:
                await bot.send_photo(chat_id=message.chat.id, photo="https://imgur.com/a/WVMAa2Q")



# Функция для получения курса валют с сайта Центрального банка РФ
def get_currency_rate(currency):
    url = f'https://www.cbr-xml-daily.ru/daily_json.js'
    response = requests.get(url)
    data = response.json()
    if currency == 'USD':
        return data['Valute']['USD']['Value']
    elif currency == 'EUR':
        return data['Valute']['EUR']['Value']
    elif currency == 'GBP':
        return data['Valute']['GBP']['Value']
    else:
        return 'Invalid currency. Please use USD, EUR, or GBP.'




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()
