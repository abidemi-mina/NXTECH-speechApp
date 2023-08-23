from time import *
from  tkinter import messagebox,Message
import webbrowser
import speech_recognition as sr
import playsound
import os
import pyttsx3
import time
import random 
from gtts import gTTS,gTTSError
import os
from datetime import datetime


#for recognizing the speech
class Person:
    name= ''
    def setName(self,name):
        self.name = name


#function for services
def services(*args):
    count=1
    speak('My services include the following:')
    for s in args:
        speak(f'{count}.{s}') 
        count+=1
    speak('How may i help you')

def mult_request(terms):
    for t in terms:
        if t in voice_data:
            return True

r = sr.Recognizer()


def record_audio(ask=False):
    ''' this is the voice recognition function'''
    
    with sr.Microphone() as source:
        audio = r.record(source,duration=5) # listens to what the user says 
        if ask:
            speak(ask)
        print("Done Listening")
        voice_data =''
        try:
            voice_data = r.recognize_google(audio) # recognizes what the user said
        except sr.UnknownValueError:
            speak('Sorry, i did not get that.Kindly ensure you are in a quiet environment and speak well.')
        except sr.RequestError as rs:
            engine_speak('Request error,Sorry , could not get your request')
            exit()
        except sr.WaitTimeoutError:
            engine_speak('Timeout Error')
        
        return voice_data.lower()


def engine_speak(text):
    '''speak function for offline mode'''
    text = str(text)
    engine.say(text)
    engine.runAndWait()


def speak(audio_string):
    ''' speaks whatever alexa wants to say'''
    try:
        tts = gTTS(text=audio_string,lang='en')  
        r = random.randint(1,10000000)
        audio_file = 'audio'+str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(audio_string)
        os.remove(audio_file)
    except gTTSError:
        engine_speak('Sorry there\'s a network issue')
        os.remove(audio_file)
    except AssertionError as e:
        print(e)



def respond(voice_data):
    ''' function that relies what is in the  '''

    # requesting for user name
    if 'my name is' in voice_data:
        name = voice_data.split('is')[-1]
        person_obj.setName(name)
        speak(f'welcome{person_obj.name}')
        speak(services('date','time','make searches','play music','youtube'))

    # when alexa is being asked of her name
    if 'what is your name' in voice_data:
        speak('My name is Alexa')


    if 'Thank you' in voice_data:
        speak('You are welcome' +person_obj.name)


    if 'services' in voice_data:
        speak(services('date','time','make searches','play music','youtube'))

    # when alexa is being called
    if 'Alexa' in voice_data:
        if person_obj.name:
            speak(f'Hi {person_obj.name}!')
        else:
            speak('Hi,what is your name')

    #request for date
    if 'date' in voice_data:
        x = datetime.now()
        speak(f"Today's date is {x.strftime('%d-%B-%Y')}")

    if mult_request(['what time is it','what says the time','what is the time']):
        x = datetime.now()
        speak(f"The time is {x.strftime('%H:%M %p')}")

    # search for something
    if mult_request(['search','what is']) and not 'what is the time' in voice_data:
        search =voice_data.split('for')[-1]
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak('this is the result for '+ search + ','+ person_obj.name)
    
    # search on youtube
    if "youtube" in voice_data:
        search_term = voice_data.split("watch")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')


    # Current location as per Google maps
    if "what is my exact location" in voice_data:
        url = "https://www.google.com/maps/search/Where+am+I+?/"
        webbrowser.get().open(url)
        speak("You must be somewhere near here, as per Google maps")

    if "weather" in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?q=weather"+search_term
        webbrowser.get().open(url)
        speak("Here is what I found for on google")

    # search on youtube
    if "play me " in voice_data:
        music_term = voice_data.split("play me")[-1]
        url = f"https://music.youtube.com/search?q={''.join([music_term])}"
        webbrowser.get().open(url)
        speak(f'here are the result for {music_term} on youtube music {person_obj.name}, please kindly choose the one to play')

    # exit the alexa or off alexa
    if 'exit' in voice_data:
        engine_speak('going offline,have a nice day' )
        exit()





person_obj= Person()# user instance
engine = pyttsx3.init()


time.sleep(1)
engine_speak('Hi,welcome,my name is alexa and i am your speech assistant.') # alxa introduction
speak('Please what is your name?')
while (1):
    voice_data = record_audio()
    respond(voice_data)
