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
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
from googleapiclient.discovery import build
import os.path
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
API_KEY = 'YOUR_API_KEY'
CLIENT_SECRET_FILE = 'path/to/client_secret.json'
   
#CORE
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
def Take_data_to_login(choice):
    process_file('Dane.json', 'Password', mode='decrypt')
    with open('rep.json', 'r') as file:
        data = json.load(file)

    for element in data:
        for platforma, dane in element.items():
            if platforma == choice:
                login = dane.get('login')
                password = dane.get('password')
                print(f"Platforma: {platforma}, Login: {login}, Hasło: {password}")
def encrypt(plaintext, password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return salt + iv + ciphertext
def decrypt(ciphertext, password):
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    ciphertext = ciphertext[32:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext
def process_file(file_path, password, mode='encrypt'):
    with open(file_path, 'rb') as file:
        data = file.read()

    if mode == 'encrypt':
        ciphertext = encrypt(data, password)

        with open(file_path, 'wb') as file:
            file.write(ciphertext)

    elif mode == 'decrypt':
        plaintext = decrypt(data, password)

        with open(file_path, 'wb') as file:
            file.write(plaintext)

    else:
        print("Invalid mode. Please use 'encrypt' or 'decrypt'.")

#Started
def action():
    process_response('co chcesz zrobić?')
    fraze = speech(sr.Recognizer())

    if fraze:
        if any(word in fraze for word in ["przeglądarka", "otwórz stronę", "odpal stronę"]):
            webOpen()
        elif any(word in fraze for word in ["wyszukaj", "poszukaj", "sprawdź", "check"]):
            webOpenwithQuestion()
        elif any(word in fraze for word in ["poczta", "mail"]):
            poczOpen()
        elif any(word in fraze for word in ["kalendarz", "calendary"]):
            CalOpen()
        elif any(word in fraze for word in ["spotyfi", "muzyka", "music"]):
            spoOpen()
        elif any(word in fraze for word in ["tłumacz", "translate"]):
            transOpen()
        elif any(word in fraze for word in ["dodaj", "add to"]):
            addto()
        elif any(word in fraze for word in ["pogoda", "weather"]):
            weather()
        else:
            print("roport")




#TO FUNCTION
def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
def check_google_calendar(creds):
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        print('Upcoming events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f'{start} - {event["summary"]}')

def get_google_calendar_service():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service
def event_exists(service, calendar_id, event_summary):
    try:
        events_result = service.events().list(
            calendarId=calendar_id, timeMin=datetime.datetime.utcnow().isoformat() + 'Z',
            maxResults=10, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        for event in events:
            if 'summary' in event and event['summary'] == event_summary:
                return True

        return False

    except HttpError as e:
        print(f'An error occurred: {e}')
        return False
def add_event_to_calendar(service, calendar_id, event_summary, event_start, event_end):
    if not event_exists(service, calendar_id, event_summary):
        event = {
            'summary': event_summary,
            'start': {
                'dateTime': event_start,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': event_end,
                'timeZone': 'UTC',
            },
        }

        try:
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
            print('Zdarzenie utworzone: %s' % (event.get('htmlLink')))
        except HttpError as e:
            print(f'An error occurred: {e}')
    else:
        print('Zdarzenie już istnieje w kalendarzu.')
def get_event_info():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        print("Podaj identyfikator kalendarza:")
        calendar_id = input().strip()

        print("Podaj podsumowanie wydarzenia:")
        event_summary = input().strip()

        print("Podaj czas rozpoczęcia wydarzenia (np. 2024-01-15T10:00:00):")
        event_start = input().strip()

        print("Podaj czas zakończenia wydarzenia (np. 2024-01-15T12:00:00):")
        event_end = input().strip()

        service = get_google_calendar_service()
        add_event_to_calendar(service, calendar_id, event_summary, event_start, event_end)


    except sr.UnknownValueError:
        print("Nie udało się zrozumieć mowy.")
    except sr.RequestError as e:
        print(f"Błąd żądania rozpoznawania mowy: {e}")

        service = get_google_calendar_service()
        add_event_to_calendar(service, calendar_id, event_summary, event_start, event_end)

    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Speech Recognition request failed: {e}")
  

#FUNCTION

def webOpen():
    process_response('już otwieram')
    webbrowser.open("https://google.com/search")
import webbrowser

def webOpenwithQuestion():
    process_response('Co chcesz wyszukać?')
    query = speech(sr.Recognizer())

    if query:
        search_url = f"https://google.com/search?q={query}"
        process_response(f'Wyszukuję definicje dla: {query}')
        webbrowser.open(search_url)

        process_response(f'Czy mam przeczytać definicje dla: {query}?')
        response = speech(sr.Recognizer())

        if response and any(word in response.lower() for word in ["tak", "czytaj"]):
            process_response(f'Oto definicje dla: {query}')
            # Tutaj można również dodać kod do zapisania definicji do pliku tekstowego
            with open('definicje.txt', 'a') as file:
                file.write(f'Definicje dla {query}:\n')
                # Dodaj kod do pobrania definicji z internetu i zapisania do pliku
                # Przykładowy kod:
                # file.write(f'Definicja 1: ... \n')
                # file.write(f'Definicja 2: ... \n')
        else:
            process_response('OK, nie będę czytać definicji.')

  
  
  
 #TODO do sprawdzenia   
def poczOpen():
    pytanie = speech()

    if pytanie == "unknown":
        print("Nie można zrozumieć mowy")
    elif pytanie == "error":
        print("Błąd podczas rozpoznawania mowy")
    elif pytanie == "tak":
        process_response('')
        label.config(animate_text="poczta")
        Take_data_to_login("gmail")
        print(Take_data_to_login)
        #TODOD pobieranie danycb z json  i wpisuwanie 
        email = "kpgebicz11@gmail.com"
        haslo = "KGP#12Q4rp_1"
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        try:
            mail.login(email, haslo)
            mail.select("inbox")

            today = datetime.date.today()
            
            twenty_four_hours_ago = today - datetime.timedelta(days=1)

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
        
        print("jaki mam wpisac temat")
        
        temat = speech
        
        print("podaj treść wiadomości")
        
        tresc=speech
        
        
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email, haslo)

            wiadomosc = f"Subject: {temat}\n\n{tresc}"

            server.sendmail(email, odbiorca, wiadomosc)

        print("Wiadomość została wysłana!")
   
   
   
   
     
def CalOpen():
    print("co chcesz zrobić")
    
    sp=speech
    
    
    if "co mam w kalendarzu" or "sprawdź kalendarz" in sp:
        print("już mówię")
        creds = authenticate_google_calendar()
        check_google_calendar(creds)
        
    elif "dodaj do kalendrza" or "dodaj do grafiku" in sp:
        print("oczywiście")
        get_event_info()

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
                    gatunek=speech
            else:
                print("Co mam puścić?")
                track_to_play = speech
                play_spotify(track_to_play)
    else:
        print("Puszcze coś z listy top 100.")
       
def transOpen():
    print("co mam przetłumaczyć")
    
    transQ=speech
    
    if "nie" in transQ:
        url = 'https://translate.google.com/'
        webbrowser.open(url)
    elif "tak" in transQ:
        translator = Translator()
        process_response("Podaj tekst do przetłumaczenia")
        try:
            translation = translator.translate(tekst_do_tłumaczenia, src='pl', dest='en')
            print("Oryginalny tekst (Polish):", tekst_do_tłumaczenia)
            print("Tłumaczenie (English):", translation.text)
        except Exception as e:
            print("Błąd podczas tłumaczenia:", str(e))
def addto():
    
    print("jaki wysłać komentarz")
    
    
    
    kom=speech
    
    
    
    label.config(text="dodanie")
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
        
#Pierwsze uruchomienie/formularz
def run_on_first_start():
    if not os.path.isfile("Dane.json"):
        with open("Dane.json", "w") as file:
            create_form()
def create_form():
    def submit_form():
        name = entry_name.get()
        email1 = entry_email1.get()
        password1 = entry_password1.get()  
        email2 = entry_email2.get()
        password2 = entry_password2.get()
        email3 = entry_email3.get()
        password3 = entry_password3.get()

        data = {
            "Name": name,
            "Forms": [
                {"Name": "Email & Password", "Entries": [
                    {"Email": email1, "Password": password1}
                ]},
                {"Name": "Spotyfi", "Entries": [
                    {"Email": email2, "Password": password2}
                ]},
                {"Name": "Storytell", "Entries": [
                    {"Email": email3, "Password": password3}
                ]}
            ]
        }

        with open("Dane.json", "w") as file:
            json.dump(data, file, indent=4)
            print("Data saved to dane.json")    
        root.destroy()
        process_file('Dane.json', 'Password', mode='encrypt') 

    root = tk.Tk()
    root.title("Multiple Forms")

# Create labels and entries for name
    label_name = tk.Label(root, text="Name:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(root)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    # Email & Password frame
    frame_email_password = tk.LabelFrame(root, text="Email & Password")
    frame_email_password.grid(row=1, columnspan=2, padx=10, pady=5)

    label_email1 = tk.Label(frame_email_password, text="Email:")
    label_email1.grid(row=0, column=0, padx=10, pady=5)
    entry_email1 = tk.Entry(frame_email_password)
    entry_email1.grid(row=0, column=1, padx=10, pady=5)

    label_password1 = tk.Label(frame_email_password, text="Password:")
    label_password1.grid(row=1, column=0, padx=10, pady=5)
    entry_password1 = tk.Entry(frame_email_password, show="*")
    entry_password1.grid(row=1, column=1, padx=10, pady=5)

    # Spotyfi frame
    frame_spotyfi = tk.LabelFrame(root, text="Spotyfi")
    frame_spotyfi.grid(row=2, columnspan=2, padx=10, pady=5)

    label_email2 = tk.Label(frame_spotyfi, text="Email:")
    label_email2.grid(row=0, column=0, padx=10, pady=5)
    entry_email2 = tk.Entry(frame_spotyfi)
    entry_email2.grid(row=0, column=1, padx=10, pady=5)

    label_password2 = tk.Label(frame_spotyfi, text="Password:")
    label_password2.grid(row=1, column=0, padx=10, pady=5)
    entry_password2 = tk.Entry(frame_spotyfi, show="*")
    entry_password2.grid(row=1, column=1, padx=10, pady=5)

    # Storytell frame
    frame_storytell = tk.LabelFrame(root, text="Storytell")
    frame_storytell.grid(row=3, columnspan=2, padx=10, pady=5)

    label_email3 = tk.Label(frame_storytell, text="Email:")
    label_email3.grid(row=0, column=0, padx=10, pady=5)
    entry_email3 = tk.Entry(frame_storytell)
    entry_email3.grid(row=0, column=1, padx=10, pady=5)

    label_password3 = tk.Label(frame_storytell, text="Password:")
    label_password3.grid(row=1, column=0, padx=10, pady=5)
    entry_password3 = tk.Entry(frame_storytell, show="*")
    entry_password3.grid(row=1, column=1, padx=10, pady=5)

    submit_button = tk.Button(root, text="Submit", command=submit_form)
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10)

    root.mainloop()
run_on_first_start()
