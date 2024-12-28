import requests
import wikipedia
#import pywhatkit
from email.message import EmailMessage
import smtplib
import json
# from decouple import config

EMAIL = ""
PASSWORD = ""


def find_my_ip():
     ip_address = requests.get('https://api.ipify.org?format=json').json()
     return ip_address["ip"]
    # try:
    #     ip_address = requests.get("https://api64.ipify.org?format=json").json()['ip']
    #     return ip_address
    # except Exception as e:
    #     return f"Unable to get IP address: {e}"

def search_on_wikipedia(query):
    results = wikipedia.summary(query,sentences = 2)
    return results
    # try:
    #     results = wikipedia.summary("Python programming", sentences=2)
    #     print(results)
    # except Exception as e:
    #     print(f"Wikipedia error: {e}")

def send_emai(receiver_address,suject,message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email['Subject'] = suject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def get_news():
    news_headline = []
    result = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=general&apiKey"f"=6cf94a3776ed4890a27166f59d10fdb6").json()
    articles = result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:3] 

def weather_forecast(city):
    res = requests.get(
        f"https://api.weatherapi.com/v1/current.json?q={city}&key=6b3122823c974b759b6144830242612"
    ).json()
    weather = res["current"]["temp_c"]
    humidity = res["current"]["humidity"]
    feelsLike = res["current"]["feelslike_c"]
    return weather, humidity, feelsLike