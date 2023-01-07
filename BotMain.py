import telebot
from BotToken import token
from datetime import datetime
import pandas as pd
from warehouseSQLite import BotDB
from replace_fu import replace_ru_to_eng, get_data_with_re


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


    @bot.message_handler(commands=['add', 'a', 'Add', 'A', 'ADD'])
    def record(message):

        text = replace_ru_to_eng(message.text.upper().strip())

        unit_name, spare_parts_name, count = get_data_with_re(text)

        date = datetime.fromtimestamp(int(message.date)).date()

        if not botBD.unit_exists(unit_name):
            bot.send_message(message.chat.id, 'Данной установки нет в базе. Выберете установку из списка ниже:')
            equipment_list = [el[0] for el in botBD.get_all_unit_list()]

            bot.send_message(message.chat.id, str(equipment_list))
        else:
            botBD.add_record(unit_name, spare_parts_name, count, date)
            bot.send_message(message.chat.id, 'Запись добавлена!!!')

    @bot.message_handler(commands=['get', 'g', 'Get', 'GET'])
    def history(message):
        start_date = message.text.strip().split()[1]
        end_date = message.text.strip().split()[2]


        columns, data = botBD.get_records(start_date, end_date)

        df = pd.DataFrame(list(data), columns=columns)

        writer = pd.ExcelWriter( 'C:\\Users\\hp\\GitHubProjects\\WarehouseBot\\reports\\' + f'{start_date}-{end_date}.xlsx')
        df.to_excel(writer)
        writer.close()
        excel_result = open(f'C:\\Users\\hp\\GitHubProjects\\WarehouseBot\\reports\\{start_date}-{end_date}.xlsx', 'rb')
        bot.send_document(message.chat.id, excel_result)

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

