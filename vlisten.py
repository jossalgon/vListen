# -*- encoding: utf-8 -*-

import telebot
import speech_recognition as sr
import os
import time
import configparser
from pydub import AudioSegment

config = configparser.ConfigParser()
config.read('config.ini')

TG_TOKEN = config['Token']['Telegram']
WIT_TOKEN = config['Token']['Wit']

bot = telebot.TeleBot(TG_TOKEN)

uses = []


def send_listen(file_info, user_id, chat_id, reply_id):
    global uses
    uses.append(user_id)
    name = '%dU%d' % (user_id, len(uses))
    text = ''

    msg = bot.send_message(chat_id, '🕓 Procesando...', reply_to_message_id=reply_id, disable_notification=True)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('%s.ogg' % name, 'wb') as new_file:
        new_file.write(downloaded_file)
    wav_audio = AudioSegment.from_file("%s.ogg" % name, format="ogg")
    wav_audio.export("%s.wav" % name, format="wav")

    audio_file = "%s.wav" % name
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        text = r.recognize_wit(audio, key=WIT_TOKEN)
    except Exception as e:
        print(e)

    if len(text) == 0:
        text = '🔇 Mensaje de voz en silencio'
    else:
        text = '💬 %s' % text.lower().capitalize()
    os.remove('%s.ogg' % name)
    os.remove('%s.wav' % name)
    bot.edit_message_text(text, chat_id=chat_id, message_id=msg.message_id)


while True:
    try:
        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            bot.reply_to(message,
                         '📢 Este bot transcribe mensajes de voz a texto tan solo enviando un audio por privado o \
                         respondiendo al mensaje con "listen" si estás en un grupo.\n\nCualquier sugerencia es \
                         bienvenida por mi creador @selui')


        @bot.message_handler(commands=['getusos'])
        def send_usos(message):
            bot.reply_to(message, 'Actualmente lo han usado %d veces.' % len(uses))


        @bot.message_handler(content_types=['voice'], func=lambda msg: msg.chat.type == 'private')
        def listen_handler(message):
            user_id = message.from_user.id
            chat_id = message.chat.id
            reply_id = message.message_id
            file_info = bot.get_file(message.voice.file_id)
            send_listen(file_info, user_id, chat_id, reply_id)


        @bot.message_handler(regexp='[Ll]isten')
        def listen_handler(message):
            if message.reply_to_message is not None and message.reply_to_message.voice is not None:
                user_id = message.from_user.id
                chat_id = message.chat.id
                reply_id = message.reply_to_message.message_id
                file_info = bot.get_file(message.reply_to_message.voice.file_id)
                send_listen(file_info, user_id, chat_id, reply_id)


        bot.polling(none_stop=True)
    except Exception as e:
        print(str(e))
        time.sleep(10)
