from subprocess import Popen
from subprocess import PIPE
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from API.weather import WeatherClient
from API.weather import WeatherQueryError, WeatherRequestError
from config import load_conf

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

condition = {
    "clear": "☀️",
    "partly-cloudy": "🌤",
    "cloudy": "🌥",
    "overcast": "☁️",
    "drizzle": "🌦",
    "light-rain": "🌧",
    "rain": "🌧",
    "moderate-rain": "🌧",
    "heavy-rain": "🌧",
    "continuous-heavy-rain": "🌧",
    "showers": "🌧",
    "wet-snow": "🌨",
    "light-snow": "❄️",
    "snow": "❄️❄️",
    "snow-showers": "❄️❄️❄️",
    "hail": "🥶",
    "thunderstorm": "🌩",
    "thunderstorm-with-rain": "🌩",
    "thunderstorm-with-hail": "🌩"
}

wind_dir = {
    "nw": "↖️",
    "n": "⬆️",
    "ne": "↗️",
    "e": "➡️",
    "se": "↘️",
    "s": "⬇️",
    "sw": "↙️",
    "w": "⬅️",
    "c": "0️⃣"
}

daytime = {
    "d": "☀️ ",
    "n": "🌙 "
}

moon_code = ['🌕', '🌖', '🌖', '🌖', '🌗', '🌘', '🌘', '🌘', '🌑', '🌒', '🌒', '🌒', '🌓', '🌔', '🌔', '🌔']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message.text
    text = f"Chat ID: {chat_id}, \n" \
           f"Message: {message}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Это бот команды АТ \n"
             f"Список досступных команд есть в меню \n"
             f"Так же я отвечу на любой вопрос"
    )


async def do_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    process = Popen("date", stdout=PIPE)
    text, error = process.communicate()
    if error:
        text = "Что-то пошло не так"
    else:
        text = text.decode("utf-8")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = WeatherClient()
    chat_id = update.effective_chat.id
    try:
        fact_weather = client.get_weather(lat=56.129057, lon=40.406635)
        if fact_weather['fact']['daytime'] == "d":
            text = daytime["d"]
        else:
            text = daytime["n"]
        if fact_weather['forecast']['parts'][0]['part_name'] == "night":
            text += "Доброй ночи \n"
        elif fact_weather['forecast']['parts'][0]['part_name'] == "morning":
            text += "Доброе утро \n"
        elif fact_weather['forecast']['parts'][0]['part_name'] == "evening":
            text += "Добрый вечер \n"
        else:
            text += "Добрый день \n"
        text += f"🌡️{fact_weather['fact']['temp']}"
    except:
        text = "WeatherRequestError"
        raise WeatherRequestError
    await context.bot.send_message(chat_id=chat_id, text=text)


if __name__ == '__main__':
    config = load_conf()
    application = ApplicationBuilder().token(config.TG_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    help_handler = CommandHandler('help', help)
    time_handler = CommandHandler('time', do_time)
    weather_handler = CommandHandler("weather", weather)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(help_handler)
    application.add_handler(time_handler)
    application.add_handler(weather_handler)

    application.run_polling()
