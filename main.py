from ast import arg
from time import ctime, strftime
import webbrowser
import speech_recognition as sr
import playsound
import os
import time
import random 
from gtts import gTTS
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
    for s in args:
        speak(f'{count}.{s}') 
        count+=1



r = sr.Recognizer()


def record_audio(ask=False):
    ''' this is the voice recognition function'''
    
    with sr.Microphone() as source:
        audio = r.listen(source) # listens to what the user says 
        if ask:
            speak(ask)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio) # recognizes what the user said
        except sr.UnknownValueError:
            speak('Sorry, i did not get that.Kindly ensure you are in a quiet environment and speak well.')
        except sr.RequestError:
            speak('Sorry , my speech service is down.Please try again later')
            exit()
        return voice_data


def speak(audio_string):
    ''' speaks whatever alexa wants to say'''
    tts = gTTS(text=audio_string,lang='en')  
    r = random.randint(1,10000000)
    audio_file = 'audio'+str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    ''' function that relies what is in the  '''

    # requesting for user name
    if 'my name is' in voice_data:
        name = voice_data.split('is')[-1]
        person_obj.setName(name)
        speak(f'welcome{person_obj.name}')
        speak('services include '+ services('date','time','make searches','play music','youtube',' ask for anything you want'))

    # when alexa is being asked of her name
    if 'what is your name' in voice_data:
        speak('My name is Alexa')


    if 'services' in voice_data:
        speak('My services are as follow:\n'+ services('date','time','make searches','play music','youtube',' ask for anything you want'))

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

    if 'time' in voice_data:
        x = datetime.now()
        speak(f"The time is {x.strftime('%H:%M %p')}")

    # search for something
    if 'search' in voice_data:
        search =voice_data.split('for')[-1]
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak('this is the result for '+ search + ','+ {person_obj.name})
    
    # search on youtube
    if "youtube" in voice_data:
        search_term = voice_data.split("watch")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    # search on youtube
    if "play me " in voice_data:
        music_term = voice_data.split("play me")[-1]
        url = f"https://music.youtube.com/search?q={''.join([music_term])}"
        webbrowser.get().open(url)
        speak(f'here are the result for {music_term} on youtube music {person_obj.name}, please kindly choose the one to play')

    # exit the alexa or off alexa
    if 'exit' in voice_data:
        speak('going offline')
        exit()

person_obj= Person()# user instance
time.sleep(1)
speak('Hi,welcome,my name is alexa and i am your speech assistant.') # alxa introduction
speak('Please what is your name?')
while (1):
    voice_data = record_audio()
    respond(voice_data)
