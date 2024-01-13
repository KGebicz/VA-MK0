import requests
from bs4 import BeautifulSoup
import pyttsx3
import speech_recognition as sr
import threading

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_response(response):
    speak(response)

def speech(r):
    with sr.Microphone() as source2:
        try:
            print("Rozpoczynam nasłuchiwanie...")
            audio2 = r.listen(source2, timeout=0.0)
            MyText = r.recognize_google(audio2, language="pl")
            MyText = MyText.lower()
            
            print("Rozpoznano tekst: {}".format(MyText))
            return MyText
            
        except sr.UnknownValueError:
            print("Nie rozpoznano żadnej wypowiedzi.")
            return None
            
        except sr.RequestError as e:
            print(f"Błąd związany z usługą rozpoznawania mowy: {e}")
            return None

def get_search_definition(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        definition_block = soup.find('div', {'class': 'BNeawe s3v9rd AP7Wnd'})
        
        if definition_block:
            return definition_block.get_text()

    return None

def Speech_Start_Stop():
    r = sr.Recognizer()
    
    while True:
        try:
            with sr.Microphone() as source2:
                print("Czekam na wypowiedź...")
                audio2 = r.listen(source2, timeout=0.0)
                MyText = r.recognize_google(audio2, language="pl")
                MyText = MyText.lower()

                print("Rozpoznano tekst: {}".format(MyText))

                # Sprawdzamy, czy wypowiedziano "cześć" i reagujemy odpowiednio
                if "cześć" in MyText:
                    print("Wykryto wypowiedź 'cześć'. Uruchamiam odpowiednią akcję.")
                    action()

                PanicWords = ["stop zero jeden", "stop 01"]
                # Sprawdzamy, czy wypowiedziano którekolwiek z słów kluczowych z PanicWords
                if any(word in MyText for word in PanicWords):
                    print("Wykryto wypowiedź z listy słów kluczowych. Zatrzymuję program.")
                    break

        except sr.UnknownValueError:
            print("Nie rozpoznano żadnej wypowiedzi.")
        
        except sr.RequestError as e:
            print(f"Błąd związany z usługą rozpoznawania mowy: {e}")

def action():
    process_response('co chcesz zrobić?')
    fraze = speech(sr.Recognizer())

    if fraze:
        process_response('co sprawdzić?')
        fraze1 = speech(sr.Recognizer())
        if any(word in fraze for word in ["wyszukaj", "poszukaj", "sprawdź", "check"]):
            definition = get_search_definition(fraze1)
            print(definition)

thread = threading.Thread(target=Speech_Start_Stop)
thread.start()
