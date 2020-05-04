import speech_recognition as sr
import os
import sys
import pygame
import time

# pylint: disable=no-member
pygame.mixer.init()
pygame.display.init()

song = 0
volume = 0.5
flag = {'mainLight' : False, 'extraLight' : False, 'music' : False, 'voice' : False, 'pause' : False, 'mute' : False}
music = ["Bartholomew.wav", "Devil_Like_You.wav", "Everybody_Walkin__This_Land.wav", "Glitter_Gold.wav", "Hungry_Heart.wav",
         "In_My_Mind.wav", "La_dalle.wav", "New_Friends.wav", "Old_Town_Road.wav", "Seven_Nation_Army.wav",
         "Sloppy_Seconds.wav", "This_Is_The_Life.wav", "Unstoppable.wav", "We_Should_Plant_Tree.wav", "West_Coast.wav"]

def talk(number):
    words = "voice/w" + number
    if flag['voice'] == False:
        words = "voice/m" + number
    pygame.mixer.music.pause()
    sound = pygame.mixer.Sound(words)
    sound.play()
    while pygame.mixer.get_busy() == True:
        pass
    if flag['pause'] == False:
        pygame.mixer.music.unpause()

def makeSomething1(zadanie):
    if 'макс' == zadanie:
        talk("1.wav")
        makeSomething(command())
    elif zadanie.find('макс') != -1:
        makeSomething(zadanie)
def command():
    r = sr.Recognizer()
    r.energy_threshold = 150  # пороговое значение шума
    r.dynamic_energy_threshold = True # автоматическое определение порога шума
    with sr.Microphone() as source:
        print("Говорите")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали: " + zadanie)
        makeSomething1(zadanie)
    except sr.UnknownValueError:
        print("Я вас не понял")

def makeSomething(zadanie):
    global song, volume
    if zadanie.find('включи') != -1 or zadanie.find('включить') != -1:
        if zadanie.find('свет') != -1:
            if zadanie.find('основной') != -1:
                if flag['mainLight'] == False:
                    talk("5.wav")
                    flag['mainLight'] = True
                else:
                    talk("8.wav")
            elif zadanie.find('дополнительный') != -1:
                if flag['extraLight'] == False:
                    talk("6.wav")
                    flag['extraLight'] = True
                else:
                    talk("9.wav")
            else:
                if flag['mainLight'] == False and flag['extraLight'] == False:
                    talk("7.wav")
                    flag['mainLight'] = True
                    flag['extraLight'] = True
                elif flag['mainLight'] == False:
                    talk("5.wav")
                    flag['mainLight'] = True
                elif flag['extraLight'] == False:
                    talk("6.wav")
                    flag['extraLight'] = True
                else:
                    talk("10.wav")
        elif zadanie.find('аудио') != -1 or zadanie.find('аудиосистему') != -1 or zadanie.find('аудосистема') != -1 or zadanie.find('музыку') != -1 or zadanie.find('музыка') != -1 or zadanie.find('медиацентр') != -1:
            if flag['music'] == False:
                talk("11.wav")
                flag['music'] = True
                pygame.mixer.music.load("music/" + music[song])
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.set_endevent(pygame.USEREVENT)  
                pygame.mixer.music.play()
            elif flag['pause'] == True:
                talk("38.wav")
            else:
                talk("12.wav")
        elif zadanie.find('звук') != -1:
            if flag['music'] == True:
                if flag['mute'] == True:
                    talk("37.wav")
                    pygame.mixer.music.set_volume(volume)
                    flag['mute'] = False
                else:
                    talk("42.wav")
            else:
                talk("27.wav")
        else:
            talk("13.wav")
    elif zadanie.find('выключи') != -1 or zadanie.find('выключить') != -1:
        if zadanie.find('свет') != -1:
            if zadanie.find('основной') != -1:
                if flag['mainLight'] == True:
                    talk("15.wav")
                    flag['mainLight'] = False
                else:
                    talk("16.wav")
            elif zadanie.find('дополнительный') != -1:
                if flag['extraLight'] == True:
                    talk("17.wav")
                    flag['extraLight'] = False
                else:
                    talk("18.wav")
            else: 
                if flag['mainLight'] == True and flag['extraLight'] == True:
                    talk("19.wav")
                    flag['mainLight'] = False
                    flag['extraLight'] = False
                elif flag['mainLight'] == True:
                    talk("15.wav")
                    flag['mainLight'] = False
                elif flag['extraLight'] == True:
                    talk("17.wav")
                    flag['extraLight'] = False
                else: 
                    talk("20.wav")
        elif zadanie.find('аудио') != -1 or zadanie.find('аудиосистему') != -1 or zadanie.find('аудосистема') != -1 or zadanie.find('музыку') != -1 or zadanie.find('музыка') != -1 or zadanie.find('медиацентр') != -1:
            if flag['music'] == True:
                talk("21.wav")
                flag['music'] = False
                pygame.mixer.music.stop()
            else:
                talk("22.wav")
        elif zadanie.find('звук') != -1:
            if flag['music'] == True:
                if volume != 0:
                    talk("36.wav")
                    pygame.mixer.music.set_volume(0)
                    flag['mute'] = True
                else:
                    talk("35.wav")
            else:
                talk("27.wav")
        else:
            talk("23.wav")
    elif zadanie.find('поставь на паузу') != -1 or zadanie.find('поставить на паузу') != -1:
        if flag['music'] == True:
            if flag['pause'] == False:
                talk("38.wav")
                flag['pause'] = True
                pygame.mixer.music.pause()
            else:
                talk("40.wav")
        else:
            talk("27.wav")
    elif zadanie.find('сними с паузы') != -1 or zadanie.find('убери c паузы') != -1 or zadanie.find('убери паузy') != -1:
        if flag['music'] == True:
            if flag['pause'] == True:
                talk("39.wav")
                flag['pause'] = False
                pygame.mixer.music.unpause()
            else:
                talk("41.wav")
        else:
            talk("27.wav")
    elif zadanie.find('следующий трек') != -1 or zadanie.find('следующая песня') != -1 or zadanie.find('вперед') != -1:
        if flag['music'] == True:
            talk("25.wav")
            song = (song + 1) % 15
            pygame.mixer.music.load("music/" + music[song])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  
            pygame.mixer.music.play()
        else:
            talk("27.wav")
    elif zadanie.find('предыдущий трек') != -1 or zadanie.find('предыдущая песня') != -1 or zadanie.find('назад') != -1:
        if flag['music'] == True:
            talk("26.wav")
            if song != 0:
                song -= 1
            else:
                song = 14
            pygame.mixer.music.load("music/" + music[song])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  
            pygame.mixer.music.play()
        else:
            talk("27.wav")
    elif zadanie.find('убавь громкость') != -1 or zadanie.find('сделай потише') != -1 or zadanie.find('убавь звук') != -1:
        if flag['music'] == True:
            if (volume - 0.1 > 0):
                volume -= 0.1
                pygame.mixer.music.set_volume(volume)
                talk("33.wav")
            else:
                talk("36.wav")
        else:
            talk("27.wav")
    elif zadanie.find('прибавь громкость') != -1 or zadanie.find('сделай погромче') != -1 or zadanie.find('прибавь звук') != -1:
        if flag['music'] == True:
            if (volume + 0.1 <= 1):
                volume += 0.1
                pygame.mixer.music.set_volume(volume)
                talk("32.wav")
            else:
                talk("34.wav")
        else:
            talk("27.wav")
    elif zadanie.find('распечатай') != -1 or zadanie.find('распечатать') != -1 or zadanie.find('напечатать') != -1 or zadanie.find('напечатай') != -1 or zadanie.find('печать') != -1:
        talk("28.wav")
    elif zadanie.find('отсканируй') != -1 or zadanie.find('отсканировать') != -1:
        load = False
        if zadanie.find('загрузи') != -1 or zadanie.find('загрузить') != -1:
            talk("29.wav")
            load = True
        if load == False:
            talk("30.wav")
    elif zadanie.find('измени голос') != -1 or zadanie.find('смени голос') != -1:
        if flag['voice'] == False:
            flag['voice'] = True
        else:
            flag['voice'] = False
        talk("31.wav")

while True:
    if flag['music'] == True:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                song = (song + 1) % 15
                pygame.mixer.music.load("music/" + music[song])
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play()
    command()
