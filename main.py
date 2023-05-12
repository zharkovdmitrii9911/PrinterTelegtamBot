import os
import time

import keyboard
import telebot;

from telebot import types

bot = telebot.TeleBot('');

filename="";


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'D:/Python/Save/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    #file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    #downloaded_file = bot.download_file(file_info.file_path)

    #src = 'D:/Python/' + file_info.file_path
    #with open(src, 'wb') as new_file:
    #    new_file.write(downloaded_file)

    bot.reply_to(message, "Сохраняю")
    start(message)

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'D:/Python/Save/' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Сохраняю")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Вот что я умею!')
    bot.send_message(message.from_user.id, "/print - печать\n")

@bot.message_handler(commands=['print'])
def selectFiles(message):
    keyboard = types.InlineKeyboardMarkup();
    indir = 'D:/Python/Save/'
    all_files = next(os.walk(indir))[2]

    for file in all_files:
        key_print = types.InlineKeyboardButton(text=file, callback_data='D:/Python/Save/'+file);
        keyboard.add(key_print);

    indir = 'D:/Python/Save/photos/'
    all_files = next(os.walk(indir))[2]

    for file in all_files:
        key_print = types.InlineKeyboardButton(text=file, callback_data='D:/Python/Save/photos/'+file);
        keyboard.add(key_print);

    bot.send_message(message.from_user.id, 'Выберете фаил!', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    mesg = bot.send_message(call.message.chat.id, 'Пин код')
    global filename
    filename = ""+call.data
    bot.register_next_step_handler(mesg, correctpin)

def correctpin(message):
    if message.text == '1111':
        bot.send_message(message.chat.id, 'Верно, Начинаю Печать!');
        os.startfile(filename, "print")

        if filename.find("/photos/",12,22)>0:
            time.sleep(15)
            keyboard.send("enter")
    else:
        bot.send_message(message.chat.id, 'Извините, ваш пин код не верный');
    start(message)







bot.polling(none_stop=True)