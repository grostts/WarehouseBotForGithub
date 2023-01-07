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
        try:
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
        except Exception:
            bot.send_message(message.chat.id, 'Комманда введена неверно. Воспользуйтесь /help, чтобы узнать, как правильно писать команды.')

    @bot.message_handler(commands=['list', 'List', 'Cписок', 'список'])
    def unit_list(message):
        equipment_list = [el[0] for el in botBD.get_all_unit_list()]
        bot.send_message(message.chat.id, str(equipment_list))
        bot.send_message(message.chat.id, 'Запрос на добавление новой установки направляете администратору.')



    @bot.message_handler(commands=['get', 'g', 'Get', 'GET'])
    def history(message):
        try:
            start_date = message.text.strip().split()[1]
            end_date = message.text.strip().split()[2]

            columns, data = botBD.get_records(start_date, end_date)

            df = pd.DataFrame(list(data), columns=columns)

            writer = pd.ExcelWriter( 'C:\\Users\\hp\\GitHubProjects\\WarehouseBotForGithub\\reports\\' + f'{start_date}-{end_date}.xlsx')
            df.to_excel(writer)
            writer.close()
            excel_result = open(f'C:\\Users\\hp\\GitHubProjects\\WarehouseBotForGithub\\reports\\{start_date}-{end_date}.xlsx', 'rb')
            bot.send_document(message.chat.id, excel_result)
        except Exception:
            bot.send_message(message.chat.id, 'Комманда введена неверно. Воспользуйтесь /help, чтобы узнать, как правильно писать команды.')


    @bot.message_handler(commands=['help', 'Help', 'HELP', 'помощь', 'Помощь', 'ПОМОЩЬ'])
    def help(message):
        bot.send_message(message.chat.id, """
        Добрый день, друг! Данный бот создан для создания списка использованныйх запасных частей.
        Бот знает следующие команды:
        /start - бот поприветсвует тебя.
        /test - бот проверит свою работоспособность.
        /id - бот вернет твой ID
        /add - бот добавит запись в базу данных. 
        Команда должна быть введена в следующем формате '/add (1) (2) (3)', где (1) номер установки, (2) артикул запасной части, (3) количество.
        /get -  бот вернет  Excel файл с записями  по запасным частям из диапазона дат. 
        Команда должна быть введена в следующем формате '/get (1) (2)', где (1) дата начала периода в формате YYYY-MM-DD , (2) дата конца периода в формате YYYY-MM-DD
        /help - бот вернет справку с описанием команд.
        /list - бот вернет список установок
        
        Также, если написать боту 'hello', 'hi', 'привет' данные команды, он отправит смешное видео.
        """)

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        hello_variants = ['hello', 'hi', 'привет']
        if message.text.lower() in hello_variants:
            video = open('C:\\Users\\hp\\GitHubProjects\\WarehouseBotForGithub\\Video\\IMG_2553.MP4', 'rb')
            bot.send_video(message.chat.id, video)

        else:
            bot.send_message(
                message.chat.id,
                'Что??? Я не знаю такую команду. Введите пожалуйста новую команду или воспользуйтесь коммандой /help.')

    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)

