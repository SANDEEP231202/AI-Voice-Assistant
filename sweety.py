import pyttsx3
import speech_recognition as sr
from googletrans import Translator
import datetime
import os
import webbrowser
import openai
from config import apikey
import cv2
import random
from requests import get
import wikipedia
import pywhatkit as kit
import smtplib
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)   0 for male & 1 for female
newVoiceRate = 145
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', newVoiceRate)

def ai(prompt):
    openai.api_key = apikey

    #openai.api_key = os.getenv("OPENAI_API_KEY")
    text = f"OpenAI response for prompt: {prompt} \n *********************\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("openai"):
        os.mkdir("openai")
        
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    
#to start or stop
def start_stop_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)
        
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        
    except Exception as e:
        print("")
        return "none"
    query = str(query).lower()
    return query

#voice to text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
    try:
        print("Recognising....")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        
    except Exception as e:
        speak("Say that again please.....")
        return "none"
    query = str(query).lower()
    return query

#translate
def TranslationHinToEng(Text):
    line = str(Text)
    translate = Translator()
    result = translate.translate(line)
    data = result.text
    print(f"user said: {data}.")
    return data

#connect
def MicExecution():
    query = takecommand().lower()
    data = TranslationHinToEng(query)
    return data

#to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    
    if hour>=0 and hour<=12:
        speak("good morning")
    elif hour>12 and hour<18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("hi I am sweety. I am at your service, please tell me how can I help you")

#to send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'your password')
    server.sendmail('your email id', to, content)
    server.close()

if __name__=="__main__":
    
    
    one_time_wish = 1
    
    flag = True
    while flag:
    

        query = start_stop_command().lower()
        if "stop" in query:
            speak("Thank you. Call me anytime if you want anything")
            flag = False
        if "hey sweety" in query or "hii sweety" in query or "sweetie" in query or "sweety" in query:
        
            if (one_time_wish == 1):
                wish()
                one_time_wish = 2
                
            else:
                speak("yes sir, what can i help you")
            
            query = takecommand().lower()
            
            #logical building for tasks
            
            #for websites
            sites = [["youtube", "https://www.youtube.com"],
                    ["chat GTP", "https://chat.openai.com/"],
                    ["google" or "chrome", "https://www.google.com"],
                    ["wikipedia", "https://www.wikipedia.com"],]
            for site in sites:
                if f"open {site[0]}".lower() in query.lower():
                    speak(f"opening {site[0]}...")
                    webbrowser.open(site[1])
                    
            apps = [["osu","C:\\Users\\Sandeep\\AppData\\Local\\osu!\\osu!.exe"],
                    ["notepad","C:\\Windows\\System32\\notepad.exe"]]
            for app in apps:
                if f"open {app[0]}".lower() in query.lower():
                    speak(f"opening {app[0]}...")
                    os.system(app[1])
                    
            for site in sites:
                if f"search on {site[0]}".lower() in query.lower() or f"search in {site[0]}".lower() in query.lower():
                    speak(f"what should i search on {site[0]}")
                    if site[0] == "youtube":
                        cd = takecommand().lower()
                        url =f"https://www.youtube.com/results?search_query={cd}"
                        webbrowser.open(url)
                        
                    if site[0] == "google":
                        cd = takecommand().lower()
                        url =f"https://www.google.com/search?q={cd}"
                        webbrowser.open(url)
                        
            if"using artificial intelligence".lower() in query.lower():
                ai(prompt=query)
                    
                
            elif "open command prompt" in query:
                os.system("start cmd")
                speak("opening command prompt...")
                
            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    command = start_stop_command()
                    if "stop" in command:
                        break;
                cap.release()
                cv2.destroyAllWindows()
                    
            elif "open music" in query:
                music_dir = "D:\\music\\beat"
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))
                
            # # if the directory folder have other than mp3. 
            # for song in songs:
            #     if song.endswith(".mp3"):
            #         os.startfile(os.path.join(music_dir, song))
            
            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP adress is {ip}")
            
            #contacts = [[sweety 👩‍🦰,]]
            #not tested
            elif "send message" in query:
                kit.sendwhatmsg("+918252995450", "msg testing", 12,4)
                
            #not tested
            elif "play on youtube" in query:
                speak(f"what should i play on youtube")
                cd = takecommand().lower
                kit.playonyt(cd)
            
            #not tested
            #to send email  
            elif "send an email" in query:
                try:
                    speak("what should i say?")
                    content = takecommand()
                    to = "senders gmail"
                    sendEmail(to, content)
                    speak("Email has been sent to sender")
                    
                except Exception as e:
                    print(e)
                    speak("sorry sir, i was not able to send this email")
            
                