import gtts
import playsound
import openai
import pyautogui
from sys import platform
import speech_recognition as sr
import datetime
import pygame
import wikipedia
import datetime
import webbrowser
import threading
import numpy
import os
import smtplib
from mutagen.mp3 import MP3
from pydub import AudioSegment
from AppOpener import open,close
import ctypes
import time
# -*- coding: utf-8 -*-
import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'

def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences

openai.api_key = "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"

email = "awesomeandy9829@gmail.com"
pwd = "Bitragunta@123"
off = False
audio = None
musicThread = None
stopMusic = False
pauseMusic = False
continueMusic = False
restartSong = False
restartPlaylist = False
skipSong = False
def speak(audio):

    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "./mp3/voice"+date_string+".mp3"
    sound = gtts.gTTS(text=audio, lang="en", tld="com", slow=False)
    sound.save(filename)
    audio = AudioSegment.from_mp3(filename)
    final = audio.speedup(playback_speed=1.3)  # speed up by 2x
    # export to mp3
    final.export("./mp3/voice500" + date_string + ".mp3", format="mp3")
    length = MP3("./mp3/voice500" + date_string + ".mp3")
    playsound.playsound("./mp3/voice500" + date_string + ".mp3")
    time.sleep(length.info.length - 0.8)

def closeApplication(appName):
    app_name = appName.replace("close ", "").strip()
    close(app_name, match_closest=True,output=False)  # App will be close be it matches little bit too (Without printing context (like CLOSING <app_name>))
def openApplication(appName):
    app_name = appName.replace("open ", "")
    open(app_name, match_closest=True)  # App will be open be it matches little bit too
def askChatGPT(text):
    response = openai.ChatCompletion.create(  # Change the function Completion to ChatCompletion
        model='gpt-3.5-turbo',
        messages=[  # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': text}
        ],
        temperature=1
    )
    speak(response.choices[0].message.content)
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    assistname = ("")
    speak("Tell me your name please" + assistname)


def username():
    uname = takeCommand(prompt=True)

    speak("Welcome " + uname)
    # columns = shutil.get_terminal_size().columns

    # print("#####################".center(columns))
    # print("Welcome Mr.", uname.center(columns))
    # print("#####################".center(columns))

    speak("How can i Help you?")


def takeCommand(prompt):
    r = sr.Recognizer()

    with sr.Microphone() as source:

        if off == False:
            print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)

    try:
        if off == False:
            print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        if off == False:
            print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        if off == False:
            print("Unable to Recognize your voice.")
        if prompt:
            speak("sorry, i didn't catch that. Could you say that again?")
            return takeCommand(True)
        return ""

    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()

def playMusic():
    music_dir = "C:\\Users\\aweso\\my music"
    songs = os.listdir(music_dir)
    numpy.random.shuffle(songs)
    print(songs)
    playlist(songs, music_dir)
def playlist(songs, music_dir):
    pygame.init()
    pygame.mixer.init()
    for song in songs:
        pygame.mixer.music.load(os.path.join(music_dir, song))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            if stopMusic:
                pygame.mixer.music.stop()
                return
            if pauseMusic:
                pygame.mixer.music.pause()
            if continueMusic:
                pygame.mixer.music.unpause()
            if restartSong:
                pygame.mixer.music.stop()
                pygame.mixer.music.play()
            if restartPlaylist:
                pygame.mixer.music.stop()
                playlist(songs, music_dir)
            if skipSong:
                pygame.mixer.music.stop()
                break


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    username()
    while True:

        query = takeCommand(prompt=False).lower()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["search", "https://www.bing.com"],
                 ["github", "https://www.github.com"], ["google meet", "https://www.meet.google.com"]]
        appAlias = ["Notepad", "Netbeans", "PyCharm", "File Explorer", "PowerPoint", "Visual Studio Code"]
        # All the commands said by user will be
        # stored here in 'query' and will be
        # converted to lower case for easily
        # recognition of command
        if off == False:
            for site in sites:
                if (query.lower().__contains__("open") & query.lower().__contains__(site[0].lower())):
                    speak("Opening")
                    webbrowser.open(site[1], new=2)

            for alias in appAlias:
                if query.lower().__contains__(alias.lower()):
                    if query.lower().__contains__("open"):
                        speak("Opening")
                        openApplication("open " + alias)
                    elif query.lower().__contains__("close"):
                        speak("Closing")
                        closeApplication("close " + alias)
            if query.startswith("who is"):
                speak('Searching Wikipedia...')
                query = query.replace("who is", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif query.startswith("what is"):
                speak('Searching Wikipedia...')
                query = query.replace("what is", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif query.startswith("where is"):
                speak('Searching Wikipedia...')
                query = query.replace("where is", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif query.startswith("when was"):
                speak('Searching Wikipedia...')
                query = query.replace("what is", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            elif ('play' in query and "music" in query) or ("play" in query and "song" in query):
                musicThread = threading.Thread(target=playMusic, args=())
                musicThread.start()
                # music_dir = "G:\\Song"
                # RECODE
            elif ('stop' in query and 'music' in query):
                if musicThread != None:
                    stopMusic = True
            elif ('pause' in query and 'music' in query):
                if musicThread != None:
                    pauseMusic = True
            elif ('continue' in query and 'music' in query):
                if musicThread != None:
                    continueMusic = True
            elif query == "what time is it" or "what's the time":
                now = datetime.datetime.now()
                if now.hour > 11:
                    speak("It is currently " + str((now.hour - 12)) + " " + str(now.minute) + " PM")
                else:
                    speak("It is currently " + str(now.hour) + " " + str(now.minute) + " AM")
            elif query == "what is the date" or query == "what's the date":
                speak("the date is " + datetime.datetime.now().strftime("%A, %B %d"))
            elif query == "lock the computer" or query == "lock my computer":
                speak("OK, locking")
                if platform == "linux" or platform == "linux2":
                    pyautogui.hotkey('ctrl', 'alt', 'l')
                    print('linux')
                elif platform == "darwin":
                    os.system('/System/Library/CoreServices/"Menu Extras"/User.menu/Contents/Resources/CGSession -suspend')
                    # pyautogui.hotkey('command', 'ctrl', 'q')
                    print('mac')
                elif platform == "win32":
                    print('win')
                    ctypes.windll.user32.LockWorkStation()
                pyautogui.hotkey('ctrl', 'c')
            elif ('repeat' in query and 'song' in query) or ('replay' in query and 'song' in query):
                restartSong = True
            elif query == "replay the playlist" or query == "start the playlist from the beginning":
                restartPlaylist = True
            elif query == "skip a song" or query == "skip the song":
                skipSong = True
            elif query == "send an email":
                speak("Who should I send it to? Type in the console")
                to = input()
                speak("Type your text that you want to send in emailcontent.txt and say done when you finish")
                with open('readme.txt') as f:
                    lines = f.readlines()
                sendEmail(to, lines)
            elif query == "":
                time.sleep(1)
            elif query == "turn off":
                off = True
                speak("Deactivating. You can say turn on at any time if you want to talk to me")
            else:
                speak("Asking ChatGPT:")
                askChatGPT(query)
        elif query == "turn on":
            off = False