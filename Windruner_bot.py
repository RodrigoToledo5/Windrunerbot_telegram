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
import pycurl
import difflib
from io import BytesIO
import datetime
from multiprocessing import Process, Lock
from forex_python.converter import CurrencyRates
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.path as mpath
import requests as req
import numpy as np
import json
from pprint import pprint 

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
    update.message.reply_text('/google') #crea un html con los atributos de poeninja
    update.message.reply_text('/binorg') #hace un request a httpbin con un diccionario establecido.
    update.message.reply_text('/buscarpokemon') #buscar un pokemon en la api https://pokeapi.co/api/v2/
    update.message.reply_text('/cripto') 
    update.message.reply_text('/traslate') 

def google(update, context):
	url='https://google.com'
	response=req.get(url)
	if response.status_code ==200:
		content=response.content
		file=open('google.html','wb')
		file.write(content)
		file.close()
	update.message.reply_text('done') 

def transform_text(lines):
	modified_lines=lines
	return modified_lines

def poeninja(update, context):
	url='https://poe.ninja/api/data/currencyoverview?league=Ultimatum&type=Currency'
	response=req.get(url)
	if response.status_code ==200:
		content=response.content
		response_json=response.json()
		lines=response_json['lines']
		update.message.reply_text('Precio en poe ninja de la currency rate')
		for currency in lines:		
			update.message.reply_text(currency['currencyTypeName']+' '+str(currency['chaosEquivalent'])+' Chaos')			
	update.message.reply_text('Done :3')

def poeninja_ex(update, context):
	url='https://poe.ninja/api/data/currencyoverview?league=Ultimatum&type=Currency'
	response=req.get(url)
	if response.status_code ==200:
		content=response.content
		response_json=response.json()
		lines=response_json['lines']
		update.message.reply_text('Precio')
		for currency in lines:		
			if currency['currencyTypeName']=='Exalted Orb':
				update.message.reply_text(currency['currencyTypeName']+' '+str(currency['chaosEquivalent'])+' Chaos')
	update.message.reply_text('Done :3')

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

def binpost(update, context):
	url='http://httpbin.org/post'
	payload={ 'nombre': 'Eduardo', 'curso':'python', 'nivel':'intermedio'}
	headers={'Content-Type': 'application/json','access-token':'12345'}
	response=req.post(url,data=json.dumps(payload),headers=headers)
	if response.status_code ==200:
		headers_response= response.headers
		server = headers_response['Server']
	update.message.reply_text('done') 
	update.message.reply_text(str(server))

def obtenerimg(update, context):
	url=str(context.args[0])
	response = req.get(url,stream=True)# realiza la peticion sin descargar el contentino
	with open('imagen.jpg','wb') as file:
		for chunk in response.iter_content(): # descarga el contenido poco a poco
			file.write(chunk)		
	response.close()
	update.message.reply_text('done') 
# def get_pokemons(url='http://pokeapi.co/api/v2/pokemon-form/', offset=0,update,context):
# 	args={'offset':offset} if offset else {}
	

def pokemon(update, context):
	offset=0
	args={'offset': offset} if offset else {} 
	url='http://pokeapi.co/api/v2/pokemon-form/'
	response = req.get(url, params=args)	# realiza la peticion sin descargar el contentino
	if response.status_code==200:

		payload=response.json()
		results=payload.get('results',[]) 
		if results:
			for pokemon in results:
				name=pokemon['name']
				pokeurl=pokemon['url']
				update.message.reply_text(name) 
				update.message.reply_text(pokeurl) 

	update.message.reply_text('done :3') 

def buscar(nombre,url='http://pokeapi.co/api/v2/pokemon-form/', offset=0):# busca un pokemon que le pasas
	args={'offset': offset} if offset else {} 	
	response = req.get(url, params=args)	
	if response.status_code==200:

		payload=response.json()
		results=payload.get('results',[]) 
		if results:
			for pokemon in results:
				name=pokemon['name']
				pokeurl=pokemon['url']
				if name==nombre:
					break
				else:
					offset=offset+1
		if offset%20==0:
			pokeurl=buscar(nombre,offset=offset)

		if offset>898:
			pokeurl='No se encontro su pokemon'

		return (pokeurl)
	else:
		pokeurl='error'
		return (pokeurl)

def buscarimg(url):# busca un pokemon que le pasas	
	response = req.get(url)	
	if response.status_code==200:

		payload=response.json()
		results=payload.get('sprites') 
		return results['front_default']
	else:
		return 'error'

def buscarpokemon(update, context):
	try:	
		nombre=str(context.args[0])
		url='http://pokeapi.co/api/v2/pokemon-form/'
		pokeurl=buscar(nombre)
		urlimg=buscarimg(pokeurl)		
		update.message.reply_text(urlimg) 
		update.message.reply_text(pokeurl) 	
		update.message.reply_text('done :3') 

	except (ValueError):
        	update.message.reply_text("ponga un nombre correcto")

def cripto(update, context):
	headers={'cache-control': 'no-cache','content-length': 0,'content-type': 'application/json'}
	url="https://btg.2miners.com/api/accounts/0x56c5fb2d2162a1a888a888d31236df08371256ec"
	response=req.get(url)
	if response.status_code==200:
		payload=response.json()
		results=playload.get('currentHashrate')
		update.message.reply_text(str(results))
		update.message.reply_text('done :3')  
	else :
		update.message.reply_text(str(response))

def converit(context):
	convertido=''
	frase=context.args
	for x in frase:
		convertido=convertido+' '+str(frase[0])
	return convertido

def traslate(update, context):
	with open('key.txt','r') as file:
		key=file.read().replace('\n','')
	url = "https://google-translate1.p.rapidapi.com/language/translate/v2"	
	archivo=open('traduccion.txt','w+')
	archivo.write(converit(context))
	with open('traduccion.txt','r') as file:
		arch=file.read().replace(' ','%20')
	payload = "q=Hello%2C%20world!&target=es&source=en"
	headers = {'content-type': "application/x-www-form-urlencoded",'accept-encoding': "application/gzip",'x-rapidapi-key': key,'x-rapidapi-host': "google-translate1.p.rapidapi.com"}
	response = req.request("POST", url, data=payload, headers=headers)
	if response.status_code==200:
		payload=response.json()
		results=payload.get('data') 
		traduccion=results['translations']
		tras=traduccion[0]
		update.message.reply_text(tras['translatedText'])
	else:
		update.message.reply_text('error'+' '+str(response.status_code))

def mat(route):
	fig, ax = plt.subplots()

	Path = mpath.Path
	path_data = [
	    (Path.MOVETO, (1.58, -2.57)),
	    (Path.CURVE4, (0.35, -1.1)),
	    (Path.CURVE4, (-1.75, 2.0)),
	    (Path.CURVE4, (0.375, 2.0)),
	    (Path.LINETO, (0.85, 1.15)),
	    (Path.CURVE4, (2.2, 3.2)),
	    (Path.CURVE4, (3, 0.05)),
	    (Path.CURVE4, (2.0, -0.5)),
	    (Path.CLOSEPOLY, (1.58, -2.57)),
	    ]
	codes, verts = zip(*path_data)
	path = mpath.Path(verts, codes)
	patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
	ax.add_patch(patch)

	# plot control points and connecting lines
	x, y = zip(*path.vertices)
	line, = ax.plot(x, y, 'go-')

	ax.grid()
	ax.axis('equal')

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
	dispatcher.add_handler(CommandHandler("poeninja", poeninja))
	dispatcher.add_handler(CommandHandler("poeninja_ex", poeninja_ex))
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
	dispatcher.add_handler(CommandHandler("binpost", binpost))
	dispatcher.add_handler(CommandHandler("obtenerimg", obtenerimg))
	dispatcher.add_handler(CommandHandler("pokemon", pokemon))
	dispatcher.add_handler(CommandHandler("buscarpokemon", buscarpokemon))
	dispatcher.add_handler(CommandHandler("cripto", cripto))
	dispatcher.add_handler(CommandHandler("traslate", traslate))

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

