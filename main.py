from ast import arg
from time import ctime, strftime
import webbrowser
import speech_recognition as sr
import playsound
import os
import time
import random 
from gtts import gTTS


#for recognizing the speech
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
            speak('sorry, i did not get that')
        except sr.RequestError:
            speak('Sorry , my speech service is down.Please try again later')
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
    if 'what is your name' in voice_data:
        speak('My name is Alexa')
    if 'Alexa' in voice_data:
        speak('Hi aminat!')
    if 'what date is it ' in voice_data:
        speak(ctime()|strftime('%d-%m-%Y'))
    if 'search' in voice_data:
        search = record_audio('what do you want to search for?')
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak('this is the result for '+ search)
    if 'exit' in voice_data:
        speak('going offline')
        exit()

    
time.sleep(1)
speak('hi, how may i help you?')
while (1):
    voice_data = record_audio()
    respond(voice_data)
