#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
<<<<<<< HEAD
Bot con varias funciones integradas para hacer algunas cosas en el servidor desde telegram
=======
"""

import logging
import pyautogui
import vlc
import pafy
import youtube_dl
import time
import requests as req
import datetime
from multiprocessing import Process, Lock
from forex_python.converter import CurrencyRates
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
with open('token.txt','r') as file:
	token=file.read().replace('\n','')
# 
# 

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi :3!')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command"""
    update.message.reply_text('/start ')
    update.message.reply_text('/windcaptura ') #Envia una captura de pantalla del servidor
    update.message.reply_text('/video ') #Reproduce un video de youtube en VLC player en el servidor
    update.message.reply_text('/sumar ') #Recibe 2 numero y devuelve la suma.
    update.message.reply_text('/dolarareal') #Convierte la cantidad de dolares a reales brasileños.
    update.message.reply_text('/read_webpage') #Lee el codigo fuente de una pagina y guarda en el servidor un archivo de texto con el codigo fuente.
    update.message.reply_text('/graficar') #grafica una funcion matematica definida dentro de mat
    update.message.reply_text('/google') #crea un html con los atributos de google.com
    update.message.reply_text('/binorg') #hace un request a httpbin con un diccionario establecido.

def google(update, context):
	url='http://google.com'
	response=req.get(url)
	if response.status_code ==200:
		content= response.content
		file=open('google.html','wb')
		file.write(content)
		file.close()
	update.message.reply_text('done') 

def binorg(update, context):
	url='http://httpbin.org/get'
	args={ 'nombre': 'Eduardo', 'curso':'python', 'nivel':'intermedio'}
	response=req.get(url, params=args)
	if response.status_code ==200:
		content= response.content
		file=open('httpbin.html','wb')
		file.write(content)
		file.close()
		response_json=response.json()
		origin= response_json['origin']
	update.message.reply_text('done') 
	update.message.reply_text(str(origin)) 

def mat(route):
   
   # Fixing random state for reproducibility
   np.random.seed(19680801)

   # create random data
   xdata = np.random.random([2, 10])

   # split the data into two parts
   xdata1 = xdata[0, :]
   xdata2 = xdata[1, :]

   # sort the data so it makes clean curves
   xdata1.sort()
   xdata2.sort()

   # create some y data points
   ydata1 = xdata1 ** 2
   ydata2 = 1 - xdata2 ** 3

   # plot the data
   fig = plt.figure()
   ax = fig.add_subplot(1, 1, 1)
   ax.plot(xdata1, ydata1, color='tab:blue')
   ax.plot(xdata2, ydata2, color='tab:orange')

   # create the events marking the x data points
   xevents1 = EventCollection(xdata1, color='tab:blue', linelength=0.05)
   xevents2 = EventCollection(xdata2, color='tab:orange', linelength=0.05)

   # create the events marking the y data points
   yevents1 = EventCollection(ydata1, color='tab:blue', linelength=0.05,
                           orientation='vertical')
   yevents2 = EventCollection(ydata2, color='tab:orange', linelength=0.05,
                           orientation='vertical')

   # add the events to the axis
   ax.add_collection(xevents1)
   ax.add_collection(xevents2)
   ax.add_collection(yevents1)
   ax.add_collection(yevents2)

   # set the limits
   ax.set_xlim([0, 1])
   ax.set_ylim([0, 1])

   ax.set_title('line plot with data points')

   # display the plot
   plt.savefig(route)

def graficar(update, context):
    """Sacaptura de pantalla al server y envia."""
    pic='/home/windruner/Documents/Windruner_bot/foto.png'
    p=Process(target=mat,args=('foto.png',))
    p.start()
    while not p.is_alive():
    	time.sleep(2)
    time.sleep(3)
    context.bot.send_photo(chat_id=update.effective_chat.id,photo=open(pic,'rb'))
    update.message.reply_text('Done :3')

def windcaptura(update, context):
    """Sacaptura de pantalla al server y envia."""
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
    dispatcher.add_handler(CommandHandler("graficar", graficar))
    dispatcher.add_handler(CommandHandler("google", google))
    dispatcher.add_handler(CommandHandler("binorg", binorg))

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

