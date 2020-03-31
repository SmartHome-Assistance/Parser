import speech_recognition as sr
import os
import sys
import webbrowser
from gtts import gTTS

flag = {'mainLight' : False, 'extraLight' : False, 'music' : False}
light = {}
hello = "Привет, чем я могу помочь вам?"
r = sr.Recognizer()
r.energy_threshold = 150  # пороговое значение шума
r.dynamic_energy_threshold  = True # автоматическое определение порога шума

def talk(words):
    print(words)
    language = 'ru'
    myobj = gTTS(text=words, lang=language, slow=False)
    myobj.save("talk.mp3")
    os.system("talk.mp3")

def takeWord(par):
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        zadanie = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали: " + zadanie)
    except sr.UnknownValueError:
        if par == 0:
            print("Я вас не понял, повторите")
        elif par == 1:
            print("Я жду вашей команды")
    return zadanie

def command():
    talk ("Жду команды Nomad")
    zadanie = ""
    while zadanie != "nomad":
        zadanie = takeWord(1)
    talk(hello)
    audio = r.listen(source)
    zadanie = takeWord()
    while makeSomething(zadanie, flag, 0) or zadane != "стоп":
        audio = r.listen(source)
        zadanie = takeWord(0)

def makeSomething(zadanie, flag, count):
    if zadanie.find('включи') != -1 or zadanie.find('включить') != -1:
        if zadanie.find('свет') != -1:
            if zadanie.find('основной') != -1:
                if flag['mainLight'] == False:
                    talk("Включаю основной свет")
                    flag['mainLight'] = True
                else:
                    talk("Основной свет уже включен")
            elif zadanie.find('дополнительный') != -1:
                if flag['extraLight'] == False:
                    talk("Включаю дополнительный свет")
                    flag['extraLight'] = True
                else:
                    talk("Дополнительный свет уже включен")
            else:
                if flag['mainLight'] == False and flag['extraLight'] == False:
                    talk("Включаю весь свет")
                    flag['mainLight'] = True
                    flag['extraLight'] = True
                elif flag['mainLight'] == False:
                    talk("Включаю основной свет")
                    flag['mainLight'] = True
                elif flag['extraLight'] == False:
                    talk("Включаю дополнительный свет")
                    flag['extraLight'] = True
                else:
                    talk("Весь свет уже включен")
        elif zadanie.find('аудио') != -1 or zadanie.find('аудиосистему') != -1 or zadanie.find('аудосистема') != -1 or zadanie.find('музыку') != -1 or zadanie.find('музыка') != -1 or zadanie.find('медиацентр') != -1:
            if flag['music'] == False:
                talk("Включаю музыку")
                flag['music'] = True
            else:
                talk("Музыка уже включена")
        else:
            if count == 0: talk("Что для вас включить?")
            elif count >= 1: talk("Извините, не расслышал, не моглибы повторить?")
            thing = takeWord(0)
            zadanie = zadanie + thing
            makeSomething(zadanie, flag, count + 1)
    elif zadanie.find('выключи') != -1 or zadanie.find('выключить') != -1:
        if zadanie.find('свет') != -1:
            if zadanie.find('основной') != -1:
                if flag['mainLight'] == True:
                    talk("Выключаю основной свет")
                    flag['mainLight'] = False
                else:
                    talk("Основной свет уже выключен")
            elif zadanie.find('дополнительный') != -1:
                if flag['extraLight'] == True:
                    talk("Выключаю дополнительный свет")
                    flag['extraLight'] = False
                else:
                    talk("Дополнительный свет уже выключен")
            else: 
                if flag['mainLight'] == True and flag['extraLight'] == True:
                    talk("Выключаю весь свет")
                    flag['mainLight'] = False
                    flag['extraLight'] = False
                elif flag['mainLight'] == True:
                    talk("Выключаю основной свет")
                    flag['mainLight'] = False
                elif flag['extraLight'] == True:
                    talk("Выключаю дополнительный свет свет")
                    flag['extraLight'] = False
                else: 
                    talk("Весь свет уже выключен")
        elif zadanie.find('аудио') != -1 or zadanie.find('аудиосистему') != -1 or zadanie.find('аудосистема') != -1 or zadanie.find('музыку') != -1 or zadanie.find('музыка') != -1 or zadanie.find('медиацентр') != -1:
            if flag['music'] == True:
                talk("Выключаю музыку")
                flag['music'] = False
            else:
                talk("Mузыка уже выключена")
        else:
            if count == 0: talk("Что для вас выключить?")
            elif count >= 1: talk("Извините, не расслышал, не моглибы повторить?")
            thing = takeWord(0)
            zadanie = zadanie + thing
            makeSomething(zadanie, flag, count + 1)
    elif zadanie.find('поставь на паузу') != -1 or zadanie.find('поставить на паузу') != -1:
        if flag['music'] == True:
            talk("Пауза")
        else:
            talk("Музыка выключена")
    elif zadanie.find('следующий трек') != -1 or zadanie.find('следующая песня') != -1 or zadanie.find('вперед') != -1:
        if flag['music'] == True:
            talk("Следующий трек")
        else:
            talk("Музыка выключена")
    elif zadanie.find('предыдущий трек') != -1 or zadanie.find('предыдущая песня') != -1 or zadanie.find('назад') != -1:
        if flag['music'] == True:
            talk("Предыдущий трек")
        else:
            talk("Музыка выключена")
    elif zadanie.find('распечатай') != -1 or zadanie.find('распечатать') != -1 or zadanie.find('напечатать') != -1 or zadanie.find('напечатай') != -1 or zadanie.find('печать') != -1:
        talk("Печатаю")
    elif zadanie.find('отсканируй') != -1 or zadanie.find('отсканировать') != -1:
        load = False
        if zadanie.find('загрузи') != -1 or zadanie.find('загрузить') != -1:
            talk("Сканирую и загружаю")
            load = True
        if load == False:
            talk("Сканирую")
    #elif zadanie.find('стоп') != -1:
        #talk("Да, конечно, без проблем")
        #sys.exit() 
    #if 'открыть сайт' in zadanie:
        #talk("Уже открываю")
         #url = 'https://itproger.com'
         #webbrowser.open(url)
    #elif 'имя' in zadanie:
        #talk("Меня зовут Nomad")

while True:
    command()