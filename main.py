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


#for recognizing the speech
class Person:
    name= ''
    def setName(self,name):
        self.name = name


#function for services
def services(*args):
    for s in args:
        speak(f'{len(s)}.{s}') 



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
            speak('Sorry, i did not get that.Please ensure you are in a quiet environment, Do you want to continue?')
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
    if 'yes' in voice_data:
        user = record_audio('Please what is your name')
        print(user)
        person_obj.setName(user.split('is')[-1])
        speak(f'welcome {user},below are my services')
        services('date request','make searches','play music','ask for anything you want')

    # when alexa is being asked of her name
    if 'what is your name' in voice_data:
        speak('My name is Alexa')

    # when alexa is being called
    if 'Alexa' in voice_data:
        if person_obj.name:
            speak('Hi aminat!')
        else:
            speak('Hi')

    #request for date
    if 'date' in voice_data:
        speak(ctime()|strftime('%d-%m-%Y'))

    # search for something
    if 'search' in voice_data:
        search = record_audio('what do you want to search for?')
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak('this is the result for '+ search + ',',+{person_obj.name})
    
    # search on youtube
    if "youtube" in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    # exit the alexa or off alexa
    if 'exit' in voice_data:
        speak('going offline')
        exit()

person_obj= Person()# user instance
time.sleep(1)
speak('Hi,welcome ,my name is alexa and i am your speech assistant.Please ensure you are in a quiet Environment.Do you want to continue?') # alxa introduction
while (1):
    voice_data = record_audio()
    respond(voice_data)
