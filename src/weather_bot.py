import telebot

from src.utils import get_token
from src.intents import GreetingIntent, EndingIntent, WeatherReportIntent
from src.follow_ups import random_followup, random_greeting_followup
from src.dialog_context import DialogContextStorage, WeatherReportContext
from src.entity_extractor import (
    SequentialEntityExtractor,
    NatashaDateExtractor,
    NatashaLocationExtractor,
    HandcraftedDateExtractor,
    HandcraftedLocationExtractor
)
from src.response_formaters import JsonToTextFormatter

weather_bot = telebot.TeleBot(get_token("tg_token.txt"))

context_storage = DialogContextStorage(WeatherReportContext)

greeting_intent = GreetingIntent(None)
ending_intent = EndingIntent(None)
weather_report_intent = WeatherReportIntent(
    SequentialEntityExtractor([
        NatashaDateExtractor(),
        NatashaLocationExtractor(),
        HandcraftedDateExtractor(),
        HandcraftedLocationExtractor()
    ])
)

json_to_text_formatter = JsonToTextFormatter()


@weather_bot.message_handler(commands=['help'])
def command_help(message):
    weather_bot.send_message(message.chat.id, "Напишите привет!")


@weather_bot.message_handler(commands=['start'])
@weather_bot.message_handler(func=greeting_intent.accept, content_types=['text'])
def greeting_handler(message):
    weather_bot.send_message(
        message.from_user.id,
        "Добрый день, пользователь!\n" +
        "Я могу предоставить прогноз погоды до двух дней вперед для Москвы и Санк-Петербурга"
    )
    weather_bot.send_message(message.from_user.id, random_greeting_followup())


@weather_bot.message_handler(func=ending_intent.accept, content_types=['text'])
def ending_handler(message):
    weather_bot.send_message(message.from_user.id, "До свидания!")


@weather_bot.message_handler(func=weather_report_intent.accept, content_types=['text'])
def weather_report_handler(message):
    user_id = message.chat.id
    new_context = weather_report_intent.to_context(message.text, WeatherReportContext())
    current_context = context_storage.get_context(user_id, new_context)

    if current_context.is_empty():
        return unknown_intent_handler(message)

    should_clear_context, response = current_context.get_response()
    response = json_to_text_formatter.from_json(response) or response
    weather_bot.send_message(user_id, response)

    if should_clear_context:
        context_storage.clear_context(user_id)
        weather_bot.send_message(user_id, random_followup())


def unknown_intent_handler(message):
    weather_bot.send_message(message.from_user.id, "Не понимаю вашего сообщения :(")
