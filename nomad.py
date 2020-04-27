import speech_recognition as sr
import os
import sys
import pygame
import webbrowser
from gtts import gTTS

flag = {'mainLight' : False, 'extraLight' : False, 'music' : False, 'voice' : False}

def talk(number):
    if flag['voice'] == False:
        words = "voice/m" + number
    else:
        words = "voice/w" + number
    pygame.mixer.init()
    sound = pygame.mixer.Sound(words)
    sound.play()

def makeSomething1(zadanie):
    if 'макс' == zadanie:
        talk("1.wav")
        makeSomething(command(), flag)
    elif zadanie.find('макс') != -1:
        makeSomething(zadanie, flag)
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
    except sr.UnknownValueError:
        print("Я вас не понял")
        zadanie = command()
    return zadanie
def makeSomething(zadanie, flag):
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
            else:
                talk("12.wav")
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
            else:
                talk("22.wav")
        else:
            talk("23.wav")
    elif zadanie.find('поставь на паузу') != -1 or zadanie.find('поставить на паузу') != -1:
        if flag['music'] == True:
            talk("24.wav")
        else:
            talk("27.wav")
    elif zadanie.find('следующий трек') != -1 or zadanie.find('следующая песня') != -1 or zadanie.find('вперед') != -1:
        if flag['music'] == True:
            talk("25.wav")
        else:
            talk("27.wav")
    elif zadanie.find('предыдущий трек') != -1 or zadanie.find('предыдущая песня') != -1 or zadanie.find('назад') != -1:
        if flag['music'] == True:
            talk("26.wav")
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
        #sys.exit() 
    #if 'открыть сайт' in zadanie:
        #talk("Уже открываю")
         #url = 'https://itproger.com'
         #webbrowser.open(url)
    #elif 'имя' in zadanie:
        #talk("Меня зовут Nomad")
while True:
    makeSomething1(command())