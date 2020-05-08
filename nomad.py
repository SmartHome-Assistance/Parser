import speech_recognition as sr
import os
import sys
import pygame
import time
import datetime
import paho.mqtt.client as mqtt
from pyspectator.processor import Cpu

song = 0
volume = 0.5
flag = {'mainLight' : False, 'extraLight' : False, 'music' : False, 'voice' : False, 'pause' : False, 'mute' : False}
playlist = ["Bartholomew.wav", "Devil_Like_You.wav", "Everybody_Walkin__This_Land.wav", "Glitter_Gold.wav", "Hungry_Heart.wav",
         "In_My_Mind.wav", "La_dalle.wav", "New_Friends.wav", "Old_Town_Road.wav", "Seven_Nation_Army.wav",
         "Sloppy_Seconds.wav", "This_Is_The_Life.wav", "Unstoppable.wav", "We_Should_Plant_Tree.wav", "West_Coast.wav"]

#PyGame
# pylint: disable=no-member
pygame.mixer.init()
pygame.display.init()

#MQTT
def on_message(client, userdata, message):
    global song, volume
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic =",message.topic)
    if message.topic == "volume":
        if flag['mute'] == False:
            volume = float(message.payload.decode("utf-8"))
            pygame.mixer.music.set_volume(volume)
    elif message.topic == "previous":
        if str(message.payload.decode("utf-8")) == "ON":
            if song != 0:
                song -= 1
            else:
                song = 14
            play(song)
            client.publish("previous", "OFF", retain = True)
    elif message.topic == "following":
        if str(message.payload.decode("utf-8")) == "ON":
            song = (song + 1) % 15
            play(song)
            client.publish("following", "OFF", retain = True)
    elif message.topic == "voice":
        flag['voice'] = False
        if str(message.payload.decode("utf-8")) == "Woman":
            flag['voice'] = True
    elif message.topic == "music":
        if flag['music'] == False and str(message.payload.decode("utf-8")) == "ON":
            play(song)
            flag['music'] = True
        elif flag['music'] == True and str(message.payload.decode("utf-8")) == "OFF":
            pygame.mixer.music.stop()
            flag['music'] = False
    elif message.topic == "mute":
        if flag['music'] == True:
            if flag['mute'] == False and str(message.payload.decode("utf-8")) == "ON":
                pygame.mixer.music.set_volume(0)
                flag['mute'] = True
            elif flag['mute'] == True and str(message.payload.decode("utf-8")) == "OFF":
                pygame.mixer.music.set_volume(volume)
                flag['mute'] = False
    elif message.topic == "pause":
        if flag['music'] == True:
            if flag['pause'] == False and str(message.payload.decode("utf-8")) == "ON":
                pygame.mixer.music.pause()
                flag['pause'] = True
            elif flag['pause'] == True and str(message.payload.decode("utf-8")) == "OFF":
                pygame.mixer.music.unpause()
                flag['pause'] = False
    else:
        flag[message.topic] = False
        if str(message.payload.decode("utf-8")) == "ON":
            flag[message.topic] = True

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
client.subscribe("song")
client.subscribe("voice")
time.sleep(2)

def play(song):
    pygame.mixer.music.load("music/" + playlist[song])
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    client.publish("song", str(song) + " - " + playlist[song], retain = True)

def talk(number):
    words = "voice/m" + number
    if flag['voice'] == True:
        words = "voice/w" + number
    pygame.mixer.music.pause()
    sound = pygame.mixer.Sound(words)
    sound.play()
    while pygame.mixer.get_busy() == True:
        pass
    if flag['pause'] == False:
        pygame.mixer.music.unpause()

def welcome(command):
    if 'макс' == command:
        talk("1.wav")
        operation = -1
        while operation == -1:
            operation = recognition()
        makeSomething(operation)
    elif command.find('макс') != -1:
        makeSomething(command)

def recognition():
    r = sr.Recognizer()
    r.energy_threshold = 150  
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Говорите")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали: " + command)
    except sr.UnknownValueError:
        print("Я вас не понял")
        command = -1
    return command

def makeSomething(command):
    global song, volume
    if command.find('включи') != -1 or command.find('включить') != -1:
        if command.find('свет') != -1:
            if command.find('основной') != -1:
                if flag['mainLight'] == False:
                    talk("5.wav")
                    flag['mainLight'] = True
                    client.publish("mainLight", "ON", retain = True)
                else:
                    talk("8.wav")
            elif command.find('дополнительный') != -1:
                if flag['extraLight'] == False:
                    talk("6.wav")
                    flag['extraLight'] = True
                    client.publish("extraLight", "ON", retain = True)
                else:
                    talk("9.wav")
            else:
                if flag['mainLight'] == False and flag['extraLight'] == False:
                    talk("7.wav")
                    flag['mainLight'] = True
                    client.publish("mainLight", "ON", retain = True)
                    flag['extraLight'] = True
                    client.publish("extraLight", "ON", retain = True)
                elif flag['mainLight'] == False:
                    talk("5.wav")
                    flag['mainLight'] = True
                    client.publish("mainLight", "ON", retain = True)
                elif flag['extraLight'] == False:
                    talk("6.wav")
                    flag['extraLight'] = True
                    client.publish("extraLight", "ON", retain = True)
                else:
                    talk("10.wav")
        elif command.find('аудио') != -1 or command.find('аудиосистему') != -1 or command.find('аудосистема') != -1 or command.find('музыку') != -1 or command.find('музыка') != -1 or command.find('медиацентр') != -1:
            if flag['music'] == False:
                talk("11.wav")
                flag['music'] = True
                client.publish("music", "ON", retain = True)
                play(song)
            elif flag['pause'] == True:
                talk("38.wav")
            else:
                talk("12.wav")
        elif command.find('звук') != -1:
            if flag['music'] == True:
                if flag['mute'] == True:
                    talk("37.wav")
                    pygame.mixer.music.set_volume(volume)
                    flag['mute'] = False
                    client.publish("mute", "OFF", retain = True)
                else:
                    talk("42.wav")
            else:
                talk("27.wav")
        else:
            talk("13.wav")
    elif command.find('выключи') != -1 or command.find('выключить') != -1:
        if command.find('свет') != -1:
            if command.find('основной') != -1:
                if flag['mainLight'] == True:
                    talk("15.wav")
                    flag['mainLight'] = False
                    client.publish("mainLight", "OFF", retain = True)
                else:
                    talk("16.wav")
            elif command.find('дополнительный') != -1:
                if flag['extraLight'] == True:
                    talk("17.wav")
                    flag['extraLight'] = False
                    client.publish("extraLight", "OFF", retain = True)
                else:
                    talk("18.wav")
            else: 
                if flag['mainLight'] == True and flag['extraLight'] == True:
                    talk("19.wav")
                    flag['mainLight'] = False
                    client.publish("mainLight", "OFF", retain = True)
                    flag['extraLight'] = False
                    client.publish("extraLight", "OFF", retain = True)
                elif flag['mainLight'] == True:
                    talk("15.wav")
                    flag['mainLight'] = False
                    client.publish("mainLight", "OFF", retain = True)
                elif flag['extraLight'] == True:
                    talk("17.wav")
                    flag['extraLight'] = False
                    client.publish("extraLight", "OFF", retain = True)
                else: 
                    talk("20.wav")
        elif command.find('аудио') != -1 or command.find('аудиосистему') != -1 or command.find('аудосистема') != -1 or command.find('музыку') != -1 or command.find('музыка') != -1 or command.find('медиацентр') != -1:
            if flag['music'] == True:
                talk("21.wav")
                flag['music'] = False
                client.publish("music", "OFF", retain = True)
                pygame.mixer.music.stop()
            else:
                talk("22.wav")
        elif command.find('звук') != -1:
            if flag['music'] == True:
                if volume != 0:
                    talk("36.wav")
                    pygame.mixer.music.set_volume(0)
                    flag['mute'] = True
                    client.publish("mute", "ON", retain = True)
                else:
                    talk("35.wav")
            else:
                talk("27.wav")
        else:
            talk("23.wav")
    elif command.find('поставь на паузу') != -1 or command.find('поставить на паузу') != -1:
        if flag['music'] == True:
            if flag['pause'] == False:
                talk("38.wav")
                flag['pause'] = True
                pygame.mixer.music.pause()
                client.publish("pause", "ON", retain = True)
            else:
                talk("40.wav")
        else:
            talk("27.wav")
    elif command.find('сними с паузы') != -1 or command.find('убери c паузы') != -1 or command.find('убери паузy') != -1:
        if flag['music'] == True:
            if flag['pause'] == True:
                talk("39.wav")
                flag['pause'] = False
                pygame.mixer.music.unpause()
                client.publish("pause", "OFF", retain = True)
            else:
                talk("41.wav")
        else:
            talk("27.wav")
    elif command.find('следующий трек') != -1 or command.find('следующая песня') != -1 or command.find('вперед') != -1:
        if flag['music'] == True:
            talk("25.wav")
            song = (song + 1) % 15
            play(song)
        else:
            talk("27.wav")
    elif command.find('предыдущий трек') != -1 or command.find('предыдущая песня') != -1 or command.find('назад') != -1:
        if flag['music'] == True:
            talk("26.wav")
            if song != 0:
                song -= 1
            else:
                song = 14
            play(song)
        else:
            talk("27.wav")
    elif command.find('убавь громкость') != -1 or command.find('сделай потише') != -1 or command.find('убавь звук') != -1:
        if flag['music'] == True:
            if (volume - 0.1 > 0):
                volume -= 0.1
                pygame.mixer.music.set_volume(volume)
                if flag['mute'] == True:
                    flag['mute'] == False
                    client.publish("mute", "OFF", retain = True)
                talk("33.wav")
                client.publish("volume", str(volume), retain = True)
            else:
                talk("36.wav")
                flag['mute'] == True
                client.publish("mute", "ON", retain = True)
        else:
            talk("27.wav")
    elif command.find('прибавь громкость') != -1 or command.find('сделай погромче') != -1 or command.find('прибавь звук') != -1:
        if flag['music'] == True:
            if (volume + 0.1 <= 1):
                volume += 0.1
                pygame.mixer.music.set_volume(volume)
                if flag['mute'] == True:
                    flag['mute'] == False
                    client.publish("mute", "OFF", retain = True)
                talk("32.wav")
                client.publish("volume", str(volume), retain = True)
            else:
                talk("34.wav")
        else:
            talk("27.wav")
    elif command.find('распечатай') != -1 or command.find('распечатать') != -1 or command.find('напечатать') != -1 or command.find('напечатай') != -1 or command.find('печать') != -1:
        talk("28.wav")
    elif command.find('отсканируй') != -1 or command.find('отсканировать') != -1:
        load = False
        if command.find('загрузи') != -1 or command.find('загрузить') != -1:
            talk("29.wav")
            load = True
        if load == False:
            talk("30.wav")
    elif command.find('измени голос') != -1 or command.find('смени голос') != -1:
        if flag['voice'] == False:
            flag['voice'] = True
            client.publish("voice", "Woman", retain = True)
        else:
            flag['voice'] = False
            client.publish("voice", "Man", retain = True)
        talk("31.wav")

while True:
    client.publish("cpu", Cpu(monitoring_latency=1).temperature, retain = True)
    client.publish("datetime", datetime.datetime.now().strftime("%H:%M:%S %d.%m.%Y"), retain = True)

    #Music
    if flag['music'] == True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                song = (song + 1) % 15
                play(song)

    command = -1
    while command == -1:
        command = recognition()
    welcome(command)