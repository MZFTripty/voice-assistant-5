import time
import pyttsx3
import speech_recognition as sr
import eel
import subprocess as sp
import os
from random import choice
from engine.jokesCollection import jokes
import webbrowser
from datetime import datetime
import wolframalpha
import pyautogui
from engine.online import find_my_ip,search_on_wikipedia,weather_forecast,get_news

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        #speak(query)
        time.sleep(2)
        eel.DisplayMessage(query)
        
        

    except Exception as e:
        return ""
    
    return query.lower()

# text = takeCommand()

# speak(text)
@eel.expose
def greet_me():
    hour = datetime.now().hour
    if (hour>=6) and (hour < 12):
        speak(f"Good Morning Tripty")
    elif (hour >= 12) and (hour <16):
        speak(f"Good Afternoon Tripty")
    elif (hour >=16) and (hour < 19):
        speak(f"Good Evening Tripty")
    speak(f"Hello Sir, i am Tia, your voice assistant. How may i assist you?")

@eel.expose
def allCommands():
    query = takeCommand()
    print(query)


    if "open camera" in query:
        speak("opening camera sir")
        sp.run('start microsoft.windows.camera:', shell=True)

    elif "open calculator" in query:
        speak("Opening calculator")
        sp.Popen('calc.exe')
    
    elif "play music" in query:
        music_dir = 'C:\\Users\zarin\Music\Audio Song'  
        songs = os.listdir(music_dir)
        speak("Playing music")
        os.startfile(os.path.join(music_dir, songs[0]))  
    
    elif "tell me a joke" in query:
        joke = choice(jokes)
        speak(joke)
        print(joke)
    
    elif "search google for" in query:
        search_query = query.replace("search google for", "")
        speak(f"Searching Google for {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        
    elif "ip address" in query:
        ip_address = find_my_ip()
        speak(f"your ip address is {ip_address}")
        print(f"your ip address is {ip_address}")
        
    elif "wikipedia" in query:
        speak("what do you want to search on wikipedia sir?")
        search = takeCommand().lower()
        results = search_on_wikipedia(search)
        speak(f"according to wikipedia, {results}")
        #speak("i am printing it on terminal ")
        #print(results)
        
    elif "weather" in query:
        try:
            ip_address = find_my_ip()
            speak("tell me the name of your city ")
            city = takeCommand().lower()
            speak(f"Getting weather report for your city {city}")
            weather,humidity, feelsLike = weather_forecast(city)
            speak(f"The current temperature is {weather} degree celcius, and humidity is {humidity} but it feels like {feelsLike}")
            #speak(f"Also the weather report talks about {weather}")
            #speak("For your convenience, I am writing it on the screen sir.")
            #print(f"Description: {weather}")
            
        except Exception as e:
            print('can not find your city')
        
    
    elif "calculate" in query:
        app_id = "XVK393-6T6KER6YEL"  # Replace with your WolframAlpha app ID
        client = wolframalpha.Client(app_id)

        try:
            # Get the part of the query after "calculate"
            ind = query.lower().split().index("calculate")
            text = query.split()[ind + 1:]
            result = client.query(" ".join(text))

            # Extract the result from WolframAlpha
            ans = next(result.results).text
            print(f"Raw Answer from WolframAlpha: {ans}")

            # Remove any non-numeric text, such as "(irreducible)"
            ans_clean = ans.split(' ')[0]  # Take only the first part before any spaces
            print(f"Cleaned Answer: {ans_clean}")

            try:
                # Try to evaluate the cleaned answer (if it's an expression like '1/2')
                ans_float = float(eval(ans_clean))  # Handle expressions like '1/2'
                
                # Round the result to two decimal places
                rounded_ans = round(ans_float, 2)

                speak(f"The answer is {rounded_ans:.2f}")
                print(f"The answer is {rounded_ans:.2f}")
            except (ValueError, SyntaxError):
                # If it can't be converted, just speak the raw answer
                speak(f"The answer is {ans}")
                print(f"The answer is {ans}")

        except StopIteration:
            speak("I couldn't find that. Please try again.")
    
    
    elif "what is" in query or "who is" in query or "which is" in query:
        app_id = "XVK393-6T6KER6YEL"
        client = wolframalpha.Client(app_id)
        try:
            ind = query.lower().index('what is') if 'what is' in query.lower() else \
                    query.lower().index('who is') if 'who is' in query.lower() else \
                    query.lower().index('which is') if 'which is' in query.lower() else None

            if ind is not None:
                text = query.split()[ind + 2:]
                result = client.query(" ".join(text))
                ans = next(result.results).text
                speak("The answer is " + ans)
                print("The answer is " + ans)
            else:
                speak("I could not find that")
        except StopIteration:
            speak("I could not find that. Please try again.")
    
    
    elif "open calendar" in query:
        speak("Opening Google Calendar")
        webbrowser.open("https://calendar.google.com")
    
    elif "go to facebook" in query:
        speak("opening facebook")
        webbrowser.open("https://www.facebook.com/")
        
    elif "how are you" in query:
        speak("I am absoloutely fine sir. What about you?")
        query = takeCommand()
        if 'fine' in query:
            speak('Good to hear that.')
        elif 'not fine' in query:
            speak('sorry to hear that.')
        
    elif "take screenshot" in query:
        screenshot = pyautogui.screenshot()
        save_path = "C:\\Users\zarin\OneDrive\Pictures\Screenshots"  # Adjust path as needed
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot.save(f"{save_path}\\screenshot_{timestamp}.png")
        print("Screenshot taken and saved.")
        
    
    elif "give me news" in query:
        speak(f"I am reading out the latest headlines of today,sir")
        speak(get_news())
        # speak("I am printing it on screen sir")
        # print(*get_news(),sep='\n')
    
    

        
    elif 'open' in query:
        from engine.features import openCommand
        openCommand(query)

    elif 'on youtube':
        from engine.features import PlayYoutube
        PlayYoutube(query)
    
    
    

    else:
        print('Not run')


    eel.ShowHood()

    