import telebot
from BotToken import token
from datetime import datetime
import pandas as pd
from warehouseSQLite import BotDB


botBD = BotDB('warehouse.db')


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'начать', 'Start', 'Начать', 'START', 'НАЧАТЬ'])
    def start(message):
        mess = f'Привет, {message.from_user.first_name} !'
        bot.send_message(message.chat.id, mess, parse_mode='html')


    @bot.message_handler(commands=['test', 'тест', 'Test', 'Тест', 'TEST', 'ТЕСТ'])
    def ping(message):
        bot.send_message(message.chat.id, 'Бот работает!')


    @bot.message_handler(commands=['id', 'ID', 'Id'])
    def id(message):
        bot.send_message(message.chat.id, 'Твой ID: ' + str(message.chat.id))

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        hello_variants = ['hello', 'hi', 'привет']
        if message.text.lower() in hello_variants:
            video = open('C:\\Users\\hp\\GitHubProjects\\WarehouseBotForGithub\\Video\\IMG_2553.MP4', 'rb')
            bot.send_video(message.chat.id, video)

        else:
            bot.send_message(
                message.chat.id,
                'Что??? Я не знаю такую команду. Введите пожалуйста новую команду.')

    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

