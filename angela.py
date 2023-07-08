
import pyttsx3 
import speech_recognition as sr 
import datetime
import webbrowser   
import openai     
import os
from config import apikey

chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Anurag: {query}\n Angela: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
   
    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]



def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Angela Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query    

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

    # Logic for executing tasks based on query.
        sites = [["youtube", "www.youtube.com"], ["wikipedia", "www.wikipedia.com"], ["google", "www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        
        
        if "open spotify".lower() in query.lower():
            speak("Opening Spotify")
            os.system(f"spotify")

        elif "open ai".lower() in query.lower():
            ai(prompt=query)
          
        elif "Angela Quit".lower() in query.lower():
            speak("Bye Anurag")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
        
        else:
            print("Chatting...")
            chat(query)

            

        

    