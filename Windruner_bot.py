#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Bot con varias funciones integradas para hacer algunas cosas en el servidor desde telegram
"""

import logging
import pyautogui
import vlc
import pafy
import youtube_dl
import time
import requests as req
import datetime
from forex_python.converter import CurrencyRates

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
token='Poner token generado en botfather

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi :3!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command"""
    update.message.reply_text('/start ')
    update.message.reply_text('/windcaptura ')
    update.message.reply_text('/video ')
    update.message.reply_text('/sumar ')
    update.message.reply_text('/dolarareal')
    update.message.reply_text('/read_webpage')


def windcaptura(update, context):
    """Scaptura de pantalla al server y envia."""
    myScreenshot= pyautogui.screenshot()
    myScreenshot.save(r'/home/windruner/Documents/Windruner_bot/foto.png')
    pic='/home/windruner/Documents/Windruner_bot/foto.png'
    context.bot.send_photo(chat_id=update.effective_chat.id,photo=open(pic,'rb'))
    update.message.reply_text('Done :3')

def video(update, context):
    """reproduce un video en el servidor"""
    url=context.args[0]
    video=pafy.new(url)
    best=video.getbest()
    playurl=best.url
    Instance=vlc.Instance()
    player=Instance.media_player_new()
    media=Instance.media_new(playurl)
    media.get_mrl()
    player.set_media(media)
    player.play()
    time.sleep(10)
    update.message.reply_text('Done :3')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def dolarareal(update, context):
    c=CurrencyRates()
    update.message.reply_text(c.get_rate('USD','BRL')*int(context.args[0]))
    update.message.reply_text('ese es el ratio humano :3')

def sumar(update,context):
    try:
        numero1 = int(context.args[0])
        numero2 = int(context.args[1])

        suma = numero1 + numero2

        update.message.reply_text("La suma es "+str(suma))

    except (ValueError):
        update.message.reply_text("por favor utilice dos numeros")

def read_webpage(update, context):
    try:
        pagina=str(context.args[0])
        resp=req.get (pagina)
        update.message.reply_text('pagina copiada en el servidor :3')
        archivo=open('pagina.txt','w+')
        archivo.write(resp.text)
        enviar='/home/windruner/Documents/Windruner_bot/pagina.txt'
        context.bot.send_document(chat_id=update.effective_chat.id,document=open(enviar,'rb'))
    except (ValueError):
        update.message.reply_text("ponga una direccion correcta")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("sumar", sumar))
    dispatcher.add_handler(CommandHandler("windcaptura", windcaptura))
    dispatcher.add_handler(CommandHandler("video", video))
    dispatcher.add_handler(CommandHandler("echo", echo))
    dispatcher.add_handler(CommandHandler("dolarareal", dolarareal))
    dispatcher.add_handler(CommandHandler("read_webpage", read_webpage))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

