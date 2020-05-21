#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import datetime
import pygame
from smbus import SMBus
import paho.mqtt.client as mqtt
import threading
from pyowm import OWM
 
bus_addr = 0x04 #bus address
bus = SMBus(1) # indicates /dev/ic2-1
exe = '''pocketsphinx_continuous -adcdev plughw:0,0 -hmm /root/zero_ru_cont_8k_v3/zero_ru.cd_semi_4000/ -jsgf /root/pi_dic.gram -dict /root/pi_dic  -inmic yes -logfn /dev/null'''
p = subprocess.Popen(["%s" % exe], shell=True, stdout=subprocess.PIPE)
flag = {'mainLight' : False, 'extraLight' : False, 'music' : False, 'voice' : False, 'pause' : False, 'mute' : False}
song = 0
value = 0.5
playlist = ["Bartholomew.wav", "Devil_Like_You.wav", "Everybody_Walkin__This_Land.wav", "Glitter_Gold.wav", "Hungry_Heart.wav",
            "In_My_Mind.wav", "La_dalle.wav", "New_Friends.wav", "Old_Town_Road.wav", "Seven_Nation_Army.wav",
            "Sloppy_Seconds.wav", "This_Is_The_Life.wav", "Unstoppable.wav", "We_Should_Plant_Tree.wav", "West_Coast.wav"]

#PyGame
# pylint: disable=no-member
pygame.mixer.init()
pygame.display.init()

#MQTT
def on_message(client, userdata, message):
    global song, value
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    if message.topic == "volume":
        value = float(message.payload.decode("utf-8"))
        volume(value)
    elif message.topic == "previous":
        change(0)
    elif message.topic == "following":
        change(1)
    elif message.topic == "voice":
        voice
    elif message.topic == "music":
        if str(message.payload.decode("utf-8")) == "ON":
            play(song, 1)
        elif str(message.payload.decode("utf-8")) == "OFF":
            play(song, 0)
    elif message.topic == "mute":
        if  str(message.payload.decode("utf-8")) == "ON":
            mute(1)
        elif str(message.payload.decode("utf-8")) == "OFF":
            mute(0)
    elif message.topic == "pause":
        if str(message.payload.decode("utf-8")) == "ON":
            pause(1)
        elif str(message.payload.decode("utf-8")) == "OFF":
            pause(0)
    elif message.topic == "mainLight":
        if str(message.payload.decode("utf-8")) == "ON":
            light('main', 1)
        elif str(message.payload.decode("utf-8")) == "OFF":
            light('main', 0)
    else:
        if str(message.payload.decode("utf-8")) == "ON":
            light('extra', 1)
        else:
            light('extra', 0)

bus.write_byte(bus_addr, 0x1)
client = mqtt.Client("server") #creating new instance
client.on_message = on_message #attach function to callback
client.connect("localhost") #connect to broker

client.publish("mainLight", "OFF", retain = True) #publishing starter messages in topics
client.publish("extraLight", "OFF", retain = True)
client.publish("music", "OFF", retain = True)
client.publish("mute", "OFF", retain = True)
client.publish("previous", "OFF", retain = True)
client.publish("following", "OFF", retain = True)
client.publish("pause", "OFF", retain = True)
client.publish("volume", "0.5", retain = True)
client.publish("song", "0 - Bartholomew.wav", retain = True)
client.publish("voice", "Man", retain = True)

client.loop_start() #start the loop
client.subscribe("mainLight") #subscribing to topics
client.subscribe("extraLight")
client.subscribe("music")
client.subscribe("mute")
client.subscribe("previous")
client.subscribe("following")
client.subscribe("pause")
client.subscribe("volume")
client.subscribe("voice")
time.sleep(2)

#Weather
def weather():
    API_key = "eba58a5494ba58eeadd60a2a0107ae3c"
    owm = OWM(API_key, language = 'ru')
    obs = owm.weather_at_coords(56.196132, 44.003592)
    w = obs.get_weather()
    temp = str(w.get_temperature(unit = 'celsius'))[9:13] + "°С"
    client.publish("weather", temp, retain = True)
    threading.Timer(3600, weather).start() 

def talk(number):
    words = "voice/M" + number
    if flag['voice'] == True:
        words = "voice/W" + number
    pygame.mixer.music.pause()
    sound = pygame.mixer.Sound(words)
    sound.play()
    while pygame.mixer.get_busy() == True:
        pass
    if flag['pause'] == False:
        pygame.mixer.music.unpause()

def play(song, bit):
    if bit == 1:
        if flag['music'] == False:
            talk("11.wav")
            flag['music'] = True
            pygame.mixer.music.load("music/" + playlist[song])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.mixer.music.play()
            client.publish("song", str(song) + " - " + playlist[song], retain = True)
            client.publish("music", "ON", retain = True)
        elif flag['pause'] == True:
            talk("38.wav")
        else:
            talk("12.wav")
    else:
        if flag['music'] == True:
            flag['music'] = False
            talk("21.wav")
            pygame.mixer.music.stop()
            client.publish("music", "OFF", retain = True)
        else:
            talk("22.wav")

def mute(bit):
    if flag['music'] == True:
        if bit == 1:
            if volume != 0:
                talk("36.wav")
                pygame.mixer.music.set_volume(0)
                flag['mute'] = True
                client.publish("mute", "ON", retain = True)
            else:
                talk("35.wav")
        if bit == 0:
            if flag['mute'] == True:
                talk("37.wav")
                pygame.mixer.music.set_volume(volume)
                flag['mute'] = False
                client.publish("mute", "OFF", retain = True)
            else:
                talk("42.wav")
    else:
        talk("27.wav")

def pause(bit):
    if flag['music'] == True:
        if bit == 1:
            if flag['pause'] == False:
                talk("38.wav")
                flag['pause'] = True
                pygame.mixer.music.pause()
                client.publish("pause", "ON", retain = True)
            else:
                talk("40.wav")
        else:
            if flag['pause'] == True:
                talk("39.wav")
                flag['pause'] = False
                pygame.mixer.music.unpause()
                client.publish("pause", "OFF", retain = True)
            else:
                talk("41.wav")
    else:
        talk("27.wav")

def change(bit):
    if flag['music'] == True:
        if bit == 1:
            talk("25.wav")
            song = (song + 1) % 15
        elif bit == 0:
            talk("26.wav")
            if song != 0:
                song -= 1
            else:
                song = 14
        play(song, 1)
    else:
        talk("27.wav")
    client.publish("previous", "OFF", retain = True)
    client.publish("following", "OFF", retain = True)

def volume(value):
    if flag ['music'] == True:
        if flag['mute'] == True:
            flag['mute'] == False
            client.publish("mute", "OFF", retain = True)
        pygame.mixer.music.set_volume(value)
        client.publish("volume", str(value), retain = True)
    else:
        talk("27.wav")

def voice():
    if flag['voice'] == False:
        flag['voice'] = True
        client.publish("voice", "Woman", retain = True)
    else:
        flag['voice'] = False
        client.publish("voice", "Man", retain = True)
    talk("31.wav")


def light(mode, bit):
    if mode == "main":
        if bit == 1:
            if flag['mainLight'] == False:
                flag['mainLight'] = True
                talk("5.wav")
                bus.write_byte(bus_addr, 0x0)
                client.publish("mainLight", "ON", retain = True)
            else: 
                talk("8.wav")
        if bit == 0:
            if flag['mainLight'] == True:
                flag['mainLight'] = False
                talk("15.wav")
                bus.write_byte(bus_addr, 0x1)
                client.publish("mainLight", "OFF", retain = True)
            else: 
                talk("16.wav")
    elif mode == "extra":
        if bit == 1:
            if flag['extraLight'] == False:
                flag['extraLight'] = True
                talk("6.wav")
                client.publish("extraLight", "ON", retain = True)
            else: 
                talk("9.wav")
        if bit == 0:
            if flag['extraLight'] == True:
                flag['extraLight'] = False
                talk("17.wav")
                client.publish("extraLight", "OFF", retain = True)
            else: 
                talk("18.wav")

weather()
while True:
    cpu = str(CPUTemperature())[44:49]
    client.publish("temp",cpu, retain = True)
    client.publish("time", datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"), retain = True)
    #Music
    if flag['music'] == True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                song = (song + 1) % 15
                play(song)
    #Recognition
    retcode = p.returncode 
    line = p.stdout.readline()
    line = str(line, "utf-8")
    if line == "макс включи свет\n":
        light('main', 1)
        light('extra', 1)
    elif line == "макс включи основной свет\n":
        light('main', 1)
    elif line == "макс включи дополнительный свет\n":
        light('extra', 1)
    elif line == "макс выключи свет\n":
        light('main', 0)
        light('extra', 0)
    elif line == "макс выключи основной свет\n":
        light('main', 0)
    elif line == "макс выключи дополнительный свет\n":
        light('extra', 0)
    elif line == "макс включи музыку\n":
        play(song, 1)
    elif line == "макс выключи музыку\n":
        play(song, 0)
    elif line == "макс включи звук\n":
        mute(0)
    elif line == "макс выключи звук\n":
        mute(1)
    elif line == "макс поставь на паузу\n":
        pause(1)
    elif line == "макс убери на паузу\n":
        pause(0)
    elif line == "макс следующий трек\n":
        change(1)
    elif line == "макс предыдущий трек\n":
        change(0)
    elif line == "макс прибавь громкость\n":
        if (value + 0.1 <= 1):
            value += 0.1
            volume(value)
            talk("32.wav")
        else:
            talk("34.wav")
    elif line == "макс убавь громкость\n":
        if (value - 0.1 > 0):
            value -= 0.1
            volume(value)
            talk("33.wav")
        else:
            mute(1)
    elif line == "макс смени голос\n":
        voice()
    else:
        print(line)
        time.sleep(0.15)
    if(retcode is not None):
        break