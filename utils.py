from pydub import AudioSegment
import speech_recognition as sr
import os

from variables import bot, WIT_TOKEN

uses = []

class Utils:
    def listen(self, message):
        if message.reply_to_message is not None and message.reply_to_message.voice is not None:
            user_id = message.from_user.id
            chat_id = message.chat.id
            reply_id = message.message_id
            file_info = bot.get_file(message.reply_to_message.voice.file_id)
            self.send_listen(file_info, user_id, chat_id, reply_id)

    def send_listen(self, file_info, user_id, chat_id, reply_id):
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
            text = '🗣 Lo siento, no te he entendido'
        else:
            text = '💬 %s' % text.lower().capitalize()
        os.remove('%s.ogg' % name)
        os.remove('%s.wav' % name)
        bot.edit_message_text(text, chat_id=chat_id, message_id=msg.message_id)
