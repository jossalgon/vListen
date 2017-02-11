# -*- encoding: utf-8 -*-

import time

from variables import bot
from utils import Utils

utils = Utils()
uses = []

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
        def listen_handler_voice(message):
            utils.listen(message)


        @bot.message_handler(regexp='[Ll]isten')
        def listen_handler_command(message):
            if message.reply_to_message is not None and message.reply_to_message.voice is not None:
                utils.listen(message)


        bot.polling(none_stop=True)
    except Exception as e:
        print(str(e))
        time.sleep(10)
