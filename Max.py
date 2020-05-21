#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import time
import pygame
#from smbus import SMBus
#import paho.mqtt.client as mqtt
 
exe = '''pocketsphinx_continuous -adcdev plughw:0,0 -hmm /root/zero_ru_cont_8k_v3/zero_ru.cd_semi_4000/ -jsgf /root/pi_dic.gram -dict /root/pi_dic  -inmic yes -logfn /dev/null'''
p = subprocess.Popen(["%s" % exe], shell=True, stdout=subprocess.PIPE)
flag = {'mainLight' : False, 'extraLight' : False, 'music' : False, 'voice' : False, 'pause' : False, 'mute' : False}
song = 0
volume = 0.5
playlist = ["Bartholomew.wav", "Devil_Like_You.wav", "Everybody_Walkin__This_Land.wav", "Glitter_Gold.wav", "Hungry_Heart.wav",
            "In_My_Mind.wav", "La_dalle.wav", "New_Friends.wav", "Old_Town_Road.wav", "Seven_Nation_Army.wav",
            "Sloppy_Seconds.wav", "This_Is_The_Life.wav", "Unstoppable.wav", "We_Should_Plant_Tree.wav", "West_Coast.wav"]

#PyGame
# pylint: disable=no-member
pygame.mixer.init()
pygame.display.init()

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
            #client.publish("song", str(song) + " - " + playlist[song], retain = True)
            #client.publish("music", "ON", retain = True)
        elif flag['pause'] == True:
            talk("38.wav")
        else:
            talk("12.wav")
    else:
        if flag['music'] == True:
            flag['music'] = False
            talk("21.wav")
            pygame.mixer.music.stop()
            #client.publish("music", "OFF", retain = True)
        else:
            talk("22.wav")

def mute(bit):
    if flag['music'] == True:
        if bit == 1:
            if volume != 0:
                talk("36.wav")
                pygame.mixer.music.set_volume(0)
                flag['mute'] = True
                #client.publish("mute", "ON", retain = True)
            else:
                talk("35.wav")
        if bit == 0:
            if flag['mute'] == True:
                talk("37.wav")
                pygame.mixer.music.set_volume(volume)
                flag['mute'] = False
                #client.publish("mute", "OFF", retain = True)
            else:
                talk("42.wav")
    else:
        talk("27.wav")

def light(mode, bit):
    if mode == "main":
        if bit == 1:
            if flag['mainLight'] == False:
                flag['mainLight'] = True
                talk("5.wav")
                #bus.write_byte(bus_addr, 0x0)
                #client.publish("mainLight", "ON", retain = True)
            else: 
                talk("8.wav")
        if bit == 0:
            if flag['mainLight'] == True:
                flag['mainLight'] = False
                talk("15.wav")
                #bus.write_byte(bus_addr, 0x1)
                #client.publish("mainLight", "OFF", retain = True)
            else: 
                talk("16.wav")
    elif mode == "extra":
        if bit == 1:
            if flag['extraLight'] == False:
                flag['extraLight'] = True
                talk("6.wav")
                #client.publish("extraLight", "ON", retain = True)
            else: 
                talk("9.wav")
        if bit == 0:
            if flag['extraLight'] == True:
                flag['extraLight'] = False
                talk("17.wav")
                #client.publish("extraLight", "OFF", retain = True)
            else: 
                talk("18.wav")

while True:
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
    else:
        print(line)
        time.sleep(0.15)
    if(retcode is not None):
        break