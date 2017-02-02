import telebot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

TG_TOKEN = config['Token']['Telegram']
bot = telebot.TeleBot(TG_TOKEN)
WIT_TOKEN = config['Token']['Wit']
