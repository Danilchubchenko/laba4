import asyncio
import aiohttp
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Ваш токен Telegram бота
TELEGRAM_BOT_TOKEN = "7367595601:AAGjydMTnUZiybjkswSdnLKxWoOc1LUYo38"

# Токен OpenWeatherMap API
OPEN_WEATHER_MAP_API_KEY = "e435ca744b6743415bb80d0df802ec40"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer("Привет! Напишите мне название города, чтобы узнать погоду.")


# Обработчик всех сообщений
@dp.message()
async def get_weather(message: types.Message):
    try:
        # Получение данных о погоде через API
        async with aiohttp.ClientSession() as session:
            url = f'https://api.openweathermap.org/data/2.5/weather?' \
                  f'q={message.text}&' \
                  f'appid={OPEN_WEATHER_MAP_API_KEY}&' \
                  f'units=metric'

            async with session.get(url) as resp:
                if resp.status != 200:
                    raise ValueError('Ошибка при запросе к API OpenWeatherMap')

                data = await resp.json()

        # Извлечение данных из ответа
        city = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')
        weather_type = data['weather'][0]['description'].capitalize()

        # Формирование сообщения
        answer_message = (
            f'<b>{city}</b>\n\n'
            f'Температура: {temperature}C°\n'
            f'Влажность: {humidity}%\n'
            f'Давление: {pressure} гПа\n'
            f'Скорость ветра: {wind_speed} м/с\n'
            f'Время восхода солнца: {sunrise_time}\n'
            f'Время заката солнца: {sunset_time}\n'
            f'Описание погоды: {weather_type}'
        )

        # Отправка сообщения пользователю
        await message.answer(answer_message, parse_mode='HTML')

    except KeyError:
        await message.answer("Не удалось найти город. Проверьте правильность написания и попробуйте снова.")
    except Exception as e:
        print(e)
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
