telgram_bot_token = "7367595601:AAGjydMTnUZiybjkswSdnLKxWoOc1LUYo38"
open_weather_token = "6a22c05ed0565ed32a595d8754feac40"
import requests
import datetime
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram import executor


bot = Bot(token=telgram_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message):
    await message.reply("type the name of your city and i will give you the weather")

@dp.message_handler()
async def get_weather(message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #pprint(data)
        city = data["name"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure =  data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]) - datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        type_of_weather = data["weather"][0]["main"]
        await message.reply(
            f"City: {city} \n" +
            f"Temperature: {temp} \n" +
            f"Humidity: {humidity} \n" +
            f"Pressure: {pressure} \n" +
            f"Speed of wind: {wind_speed} \n" +
            f"Sunrise time: {sunrise} \n" +
            f"Sunset time: {sunset} \n" +
            f"Length of the day: {length_of_the_day} \n" +
            f"Type of the weather: {type_of_weather} \n"
        )
    except Exception as e:
        await message.reply(print("Проверьте название города"))



if name == "main":
    executor.start_polling(dp)