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
        current_temp = client.get_fact_temp(lat=56.129057, lon=40.406635)
        message = f"🌡️{current_temp}"
    except:
        logger.exception("WeatherRequestError")
        message = "WeatherRequestError"
        raise WeatherRequestError
    text = f"Chat ID: {chat_id}, \n" \
           f"Message: {message}"
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
