import datetime, time
import tkinter as tk
import json
import webbrowser
import os
import requests
from googletrans import Translator
import imaplib
from email.header import decode_header
import smtplib
import ssl
import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def animate_text(text, delay_ms=100):
    for i in range(len(text) + 1):
        label.config(text=text[:i])
        root.update()
        time.sleep(delay_ms / 1000)
    entry.focus() 
    
    
#TODO sprawdzić działanie dodać sieć neuralną
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
      
     
def speech():
    r = sr.Recognizer()
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2, duration=0.2) 
        audio2 = r.listen(source2)
        MyText = r.recognize_google(audio2,language="pl")
        MyText = MyText.lower()
        # text_box.insert(END,MyText)
    return MyText       

def action():     
    
    
    fraze=speech
    
    
    # fraze = entry.get()
    
    if "przeglądarka" in fraze or "przeglądarke" in fraze or "strona" in fraze:
        webOpen()
    elif "wyszukaj" in fraze or "poszukaj" in fraze or "sprawdź" in fraze or "check" in fraze:
        webOpenwithQuestion()
    elif "poczta" in fraze or "mail" in fraze:
        poczOpen()
    elif "kalendarz" in fraze or "calendary" in fraze:
        CalOpen()
    elif "spotyfi" in fraze or "muzyka" in fraze or "music" in fraze:
        spoOpen()
    elif "storytell" in fraze or "audiobook" in fraze:
        storyOpen()
    elif "tłumacz" in fraze or "translate" in fraze:
        transOpen()
    elif "dodaj" in fraze or "add to" in fraze:
        addto()
    elif "pogoda" in fraze or "weather" in fraze:
        weather()
    elif "uruchom" in fraze or "start" in fraze or "włącz" in fraze:
        print("1")
    else:
        print("roport")

def webOpen():
    
    label.config(animate_text(text="Otwieram przegladarkę"))
    webbrowser.open("https://google.com/search")
def webOpenwithQuestion():
    print("co mam sprwdzić")
    
    
    test1=speech
    
    
    
    # query = entry.get()
    label.config(animate_text(text="Oczywiście, `wyszukuję..."))
    url = "https://www.google.com/search?q=" + test1
    webbrowser.open(url)
    
#TODO DO SPRAWDZENIA
def poczOpen():
    pytanie = speech()

    if pytanie == "unknown":
        print("Nie można zrozumieć mowy")
    elif pytanie == "error":
        print("Błąd podczas rozpoznawania mowy")
    elif pytanie == "tak":
        label.config(animate_text="poczta")
        email = "kpgebicz11@gmail.com"
        haslo = "KGP#12Q4rp_1"
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        try:
            mail.login(email, haslo)
            mail.select("inbox")

            # Get the current date and time
            today = datetime.date.today()
            
            # Calculate 24 hours ago
            twenty_four_hours_ago = today - datetime.timedelta(days=1)

            # Prepare the date format for the search
            date_format = "%d-%b-%Y"  # Format like: "01-Jan-2023"
            since_date = twenty_four_hours_ago.strftime(date_format)

            # Construct the search query
            search_query = f'(SINCE "{since_date}")'

            # Search for emails within the last 24 hours
            result, data = mail.uid("search", None, search_query)
            if result == "OK":
                numery_maili = data[0].split()
                for i in numery_maili:
                    result, message_data = mail.uid("fetch", i, "(RFC822)")
                    if result == "OK":
                        raw_email = message_data[0][1]
                        print(raw_email.decode("utf-8"))

        except Exception as e:
            print("Wystąpił błąd:", e)
        finally:
            mail.logout()
    elif pytanie =="nie":
        email = "kpgebicz11@gmail.com"
        haslo = "KGP#12Q4rp_1"



        print ("do kogo wysłać")
        
        
        odbiorca=speech
        
        
        
        # odbiorca = "kgebicz11@gmail.com"
        print("jaki mam wpisac temat")
        
        
        
        temat = speech
        
        
        
        # temat = "test"
        print("podaj treść wiadomości")
        # tresc = "test1"
        
        
        
        
        tresc=speech
        
        
        
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email, haslo)

            wiadomosc = f"Subject: {temat}\n\n{tresc}"

            server.sendmail(email, odbiorca, wiadomosc)

        print("Wiadomość została wysłana!")
     
#TODO dodać
def CalOpen():
    #TODO zmienić aby wcześniej było wybierane czy to dodanie czy przeczytanie
    print("co chcesz zrobić")
    
    
    sp=speech
    
    
    if "co mam w kalendarzu" or "sprawdź kalendarz" in sp:
        print("już mówię")
    elif "dodaj do kalendrza" or "dodaj do grafiku" in sp:
        print("oczywiście")
        
        
        #TODO sprawdxanie czy wolne
        sp2=speech
        
        
        if "1" in sp2:
            print("dodano")
        elif "2" in sp2:
            print("termin zajęty")
            if "dodaj to w wolnym terminie":
                print("oczywiście")
            else:
                print("Niestety nie ma wolnego czasu w tym termienie")
                print("co mam zrobić")
                
                
                sp3=speech
                
                
                if "sam to zrobię" in sp3:
                    print("oczywiście")
                elif "kiedy mam pierwszy wolny termin":
                    print("już mówię")
                    
                    
                    sp4=speech
                    
                    
                    if "dodaj to w inntm terminie" in sp4:
                        print("oczywiście")
                else:
                    print("przepraszam nie mogę tego zrobić")
        else:
            print("nie rozumiem")

def play_spotify(track_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

    results = sp.search(q=track_name, limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Odtwarzam {track_name} na Spotify.")
    else:
        print(f"Nie znaleziono utworu o nazwie {track_name}.")

def play_last_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-recently-played"))

    last_tracks = sp.current_user_recently_played(limit=1)

    if last_tracks and 'items' in last_tracks and last_tracks['items']:
        last_track = last_tracks['items'][0]
        playlist_id = last_track['context']['uri']

        sp.start_playback(context_uri=playlist_id)
        print("Odtwarzam ostatnią playlistę na Spotify.")
    else:
        print("Nie znaleziono ostatnio odtwarzanej playlisty.")

def spoOpen():
    label.config(animate_text="wyszukać konkretnej")
    print("Czy chcesz posłuchać czegoś konkretnego?")

    sp = speech()

    if "tak" in sp:
        print("Oczywiście, ostatnio słuchałeś. Chcesz kontynuować czy coś nowego?")

        sp1 = speech()

        if "kontynuuj" in sp1:
            play_last_playlist()
            print("Nie ma problemu, kontynuujemy.")
        else:
            print("Czy mam coś wybrać?")

            sp3 = speech()

            if "tak" in sp3:
                print("Oki, jakiś konkretny gatunek?")
                gat = speech()
                if "nie" in gat:
                    print("Już puszczałem.")
                    # play_random_top_100()
                else:
                    #TODO pobiera z speechrecognition gatuenk w jakim ma polecieć piosenka
                    print("Z jakiego gatunku mam wybrać?")
            else:
                print("Co mam puścić?")
    else:
        print("Puszcze coś z listy top 100.")

    # Example usage of play_spotify function
    track_to_play = "nazwa_utworu"  # Replace with the track name recognized from speech
    play_spotify(track_to_play)

        
#TODO dodać
def storyOpen():
    print("chesz posłuchać czegoś konkretnego?")
    
    sp=speech
    
    
    
    if "yes" in sp:
        print("oczywiście ostatnio słuchałeć\n chcesz kontunułować czy coś nowego")
        
        
        sp1 =speech
        
        
        
        if "kontynułuj" in sp1:
            print("nie ma problemu")
        else: 
            print("mam coś wybrać?")
            
            sp3=speech
            
            
            
            if "tak" in sp3:
                print("oki, jakiś konkretny gatunek?")
                if "nie":
                    print("już puszczam")
                else:
                    print ("z jakiego gatunku wybrać?")
            else:
                print("co mam puścić?")
    else:
        print ("puszczę coś z polecanych dla ciebieć")
    label.config(animate_text(text="storytell"))
    
    
def transOpen():
    print("co mam przetłumaczyć")
    
    
    transQ=speech
    
    
    
    # transQ = pytanie.get()
    if "nie" in transQ:
        url = 'https://translate.google.com/'
        webbrowser.open(url)
    elif "tak" in transQ:
        translator = Translator()
        tekst_do_tłumaczenia = input("Podaj tekst do przetłumaczenia: ")
        try:
            translation = translator.translate(tekst_do_tłumaczenia, src='pl', dest='en')
            print("Oryginalny tekst (Polish):", tekst_do_tłumaczenia)
            print("Tłumaczenie (English):", translation.text)
        except Exception as e:
            print("Błąd podczas tłumaczenia:", str(e))
def addto():
    
    print("jaki wysłać komentarz")
    
    
    
    kom=speech
    
    
    
    label.config(animate_text(text="dodanie"))
def weather():
    print("gdzie mam sprawdzić pogode")
    
    
    location=speech
    
    
    # location = pytanie.get()
    url = f'https://wttr.in/{location}?format=%C+%t+%w'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        print(f'Pogoda w {location}:')
        print(data)
    else:
        print('Nie udało się pobrać danych pogodowych.')
        


#TODO zmienićc na możliwośc zmiany hot worda // usprawienie o sieć neuralną
# HOTWORD = "hey siri"

# # Set up the audio stream
# pa = pyaudio.PyAudio()
# stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)

# # Initialize the speech recognizer
# r = sr.Recognizer()

# # Loop to listen for the hotword
# while True:
#     # Listen for audio input
#     data = stream.read(2048)
#     # Convert the audio to text using speech recognition
#     text = r.recognize_google(data, language='pl')
#     # Check if the hotword was detected
#     if HOTWORD in text.lower():
#         print("Hotword detected!")
#         # Perform further processing (e.g. speech recognition) to handle the user's command
#         break

# # Clean up the audio stream
# stream.stop_stream()
# stream.close()
# pa.terminate()

#TODO zamiienić na okno w stylu kalwisza windows // klasy pwiadomienia 
root = tk.Tk()
root.title("Okno z Przyciskiem")
root.geometry("400x300")

label = tk.Label(root, text="", font=("Arial", 16))
label.pack(pady=20)

entry = tk.Entry(root)
entry.pack(pady=10)
button = tk.Button(root, text="Wykonaj akcję", command=action)
button.pack(pady=10)

text_to_animate = "Witaj w moim pierwszym oknie!"

root.after(1000, lambda: animate_text(text_to_animate))
root.mainloop()