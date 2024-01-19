import webbrowser
import os
import requests
from googletrans import Translator
from email.header import decode_header
import speech_recognition as sr
import pyttsx3
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
from email.mime.text import MIMEText
import base64
from datetime import datetime, timedelta
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import json
import shutil




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
    def get_config_from_json():
        try:
            with open('dane.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                if isinstance(data, dict):
                    return data
                else:
                    print(f'Błąd: Plik {"dane.json"} nie zawiera poprawnych danych konfiguracyjnych.')
                    return {}
        except FileNotFoundError:
            print(f'Plik {"dane.json"} nie został znaleziony.')
            return {}
        except json.JSONDecodeError as json_error:
            print(f'Wystąpił błąd podczas dekodowania pliku JSON: {"dane.json"}')
            print(f'Szczegóły błędu: {json_error}')
            return {}
        except Exception as e:
            print(f'Inny błąd: {e}')
            return {}

    def recognize_speech():
        with sr.Microphone() as source:
            print("Czekam na wypowiedź...")
            audio = r.listen(source, timeout=0.0)
            return r.recognize_google(audio, language="pl").lower()

    r = sr.Recognizer()
    config_data = get_config_from_json()
    
    # Print the entire content of the config_data for debugging
    print("Config data:", config_data)
    
    # Use the provided activation_word or get it from the config_data
    activation_word = config_data.get('activation_word', "").strip().lower()
    
    # Print the activation_word for debugging
    print("Activation word:", activation_word)

    while True:
        try:
            MyText = recognize_speech()
            print("Rozpoznano tekst:", MyText)

            if activation_word in MyText:
                print(f"Wykryto wypowiedź '{activation_word}'. Uruchamiam odpowiednią akcję.")
                action()

            panic_words = ["stop zero jeden", "stop 01", "top 01"]
            if any(word in MyText for word in panic_words):
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
def process_response_cal(start, summary):
    speak(f"{start} - {summary}")
#Started
def action():
    process_response('co chcesz zrobić?')
    fraze = speech(sr.Recognizer())
    try:
        with open("dane.json", 'r') as file:  # Use 'r' for reading text
            data = json.load(file)
            time_get = int(data.get('time_interval', ""))
    except FileNotFoundError:
        print(f'Plik {"dane.json"} nie został znaleziony.')
        time_get = 24
    except json.JSONDecodeError as json_error:
        print(f'Wystąpił błąd podczas dekodowania pliku JSON: {"dane.json"}')
        print(f'Szczegóły błędu: {json_error}')
        time_get = 24
    except Exception as e:
        print(f'Inny błąd: {e}')
        time_get = 24
    if fraze:
            if any(word in fraze for word in ["przeglądarka", "otwórz stronę", "odpal stronę","strona"]):
                webOpen()
            elif any(word in fraze for word in ["wyszukaj", "poszukaj", "sprawdź", "check"]):
                webOpenwithQuestion()
            elif any(word in fraze for word in ["poczta", "mail"]):
                process_response("chcesz sprawdzić czy wysłać")
                wyb=speech(sr.Recognizer())
                if any(word in wyb for word in ["sprawdź", "sprawdze", "check"]):
                    MailOpen(time_get)
                elif any(word in wyb for word in ["wyśle", "wysli", "wysłać"]):
                    send_email_command()  
                else:
                    process_response("nie rozumiem")
            elif any(word in fraze for word in ["kalendarz", "calendary", "włącz kalendarz"]):
                process_response("chcesz sprawdzić czy dodać")
                wyb1=speech(sr.Recognizer())
                if any(word in wyb1 for word in ["sprawdź", "sprawdze", "check"]):
                    CalOpen()
                elif any(word in wyb1 for word in ["dodaj", "zaplanuj spotkanie", "zaplanuj"]):
                    add_cal()
                else:
                    process_response("nie rozumiem")
            elif any(word in fraze for word in ["tłumacz", "translate"]):
                transOpen()
            elif any(word in fraze for word in ["dodaj", "add to","wyślij raport","raport"]):
                toReport()
            elif any(word in fraze for word in ["pogoda", "weather"]):
                weather()
            else:
                toReport()
            
#TO FUNCTION
SCOPES1 = ["https://www.googleapis.com/auth/gmail.readonly"]
def authenticate_and_build_service():
    creds = None
    if os.path.exists("token1.json"):
        creds = Credentials.from_authorized_user_file("token1.json", SCOPES1)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES1
            )
            creds = flow.run_local_server(port=0)
        with open("token1.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
def authenticate_and_fetch_emails(service, query=""):
    try:
        results = service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])
        return messages
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def authenticate_and_build_service2():
    creds = None
    if os.path.exists("token2.json"):
        creds = Credentials.from_authorized_user_file("token2.json", SCOPES1)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES1
            )
            creds = flow.run_local_server(port=0)
        with open("token2.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
def send_email(service, to, subject, body):
    try:
        message = create_message("me", to, subject, body)
        send_message(service, "me", message)
        print("Wysłano e-mail pomyślnie.")
    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłania e-maila: {e}")
def create_message(sender, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {'raw': raw}
def send_message(service, user_id, message):
    try:
        service.users().messages().send(userId=user_id, body=message).execute()
    except HttpError as error:
        print(f"An error occurred while sending the message: {error}")
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
def authenticate_and_build_calendar_service():
    creds = None
    if os.path.exists("token_calendar.json"):
        creds = Credentials.from_authorized_user_file("token_calendar.json", CALENDAR_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", CALENDAR_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token_calendar.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except Exception as error:
        print(f"An error occurred: {error}")
        return None
def add_event_to_calendar(calendar_service, summary, start_time, end_time):
    try:
        with open("Dane.json", 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = decrypt(encrypted_data, 'password')
        data = json.loads(decrypted_data.decode('utf-8'))

        if data:
            time_zone = data.get('time_zone', 'Europe/Warsaw')
        else:
            time_zone = "Europe/Warsaw"

        try:
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_time,
                    'timeZone': time_zone,
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': time_zone,
                },
            }

            created_event = calendar_service.events().insert(calendarId='primary', body=event).execute()
            print(f'Utworzono wydarzenie: {created_event.get("htmlLink")}')
        except HttpError as error:
            print(f"Wystąpił błąd: {error}")
    except FileNotFoundError:
        print(f'Plik {"Dane.json"} nie został znaleziony.')
        return None
    except json.JSONDecodeError:
        print(f'Wystąpił błąd podczas dekodowania pliku JSON: {"Dane.json"}')
        return None     
def get_month_number(month_name):
    months_mapping = {
        "styczeń": "01",
        "luty": "02",
        "marzec": "03",
        "kwiecień": "04",
        "maj": "05",
        "czerwiec": "06",
        "lipiec": "07",
        "sierpień": "08",
        "wrzesień": "09",
        "październik": "10",
        "listopad": "11",
        "grudzień": "12",
    }

    # Check if the input is already a number
    if month_name.isdigit() and 1 <= int(month_name) <= 12:
        return f"{int(month_name):02}"

    # Convert spoken representation to number
    result = months_mapping.get(month_name.lower(), None)

    if result:
        return result
    else:
        print("Błąd: Nieprawidłowy miesiąc. Spróbuj ponownie.")
        return None
def is_event_conflict(calendar_service, start_time, end_time):
    try:
        events_result = calendar_service.events().list(
            calendarId='primary',
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        return len(events) > 0

    except Exception as error:
        print(f"An error occurred while checking for conflicts: {error}")
        return True
def create_message(sender, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
def setup_gmail_api():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    # The file token3.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token3.json'):
        creds = Credentials.from_authorized_user_file('token3.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token3.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)
def send_report_email(service, recipient_email, subject, body):
    message = create_message(sender='email', to=recipient_email, subject=subject, body=body)
    send_message(service, 'me', message)
def word_to_number(word):
    word_dict = {
        'pierwszy': 1,
        'drugi': 2,
        'trzeci': 3,
        'czwarty': 4,
        'piąty': 5,
        'szósty': 6,
        'siódmy': 7,
        'ósmy': 8,
        'dziewiąty': 9,
        'dziesiąty': 10,
        'jedenasty': 11,
        'dwunasty': 12,
        'trzynasty': 13,
        'czternasty': 14,
        'piętnasty': 15,
        'szesnasty': 16,
        'siedemnasty': 17,
        'osiemnasty': 18,
        'dziewiętnasty': 19,
        'dwudziesty': 20,
        'dwudziesty pierwszy': 21,
        'dwudziesty drugi': 22,
        'dwudziesty trzeci': 23,
        'dwudziesty czwarty': 24,
        'dwudziesty piąty': 25,
        'dwudziesty szósty': 26,
        'dwudziesty siódmy': 27,
        'dwudziesty ósmy': 28,
        'dwudziesty dziewiąty': 29,
        'trzydziesty': 30,
        'trzydziesty pierwszy': 31,
    }

    lowercase_word = word.lower()
    return word_dict.get(lowercase_word, None)
#FUNCTIONs

def webOpen():
    process_response('już otwieram')
    webbrowser.open("https://google.com/search")
def webOpenwithQuestion():
    process_response('Co chcesz wyszukać?')
    query = speech(sr.Recognizer())

    if query:
        search_url = f"https://google.com/search?q={query}"
        process_response(f'Wyszukuję informacji dla: {query}')
        webbrowser.open(search_url)
def transOpen():
    process_response("Czy chcesz coś przetłumaczyć za pomocą głosu?")

    transQ = speech(sr.Recognizer())
    if transQ == "tak":
        process_response("Podaj tekst do przetłumaczenia")

        tekst_do_tłumaczenia = speech(sr.Recognizer())

        if tekst_do_tłumaczenia:
            translator = Translator()
            try:
                translation = translator.translate(tekst_do_tłumaczenia, src='pl', dest='en')
                print("Oryginalny tekst (Polish):", tekst_do_tłumaczenia)
                print("Tłumaczenie (English):", translation.text)
                process_response(translation.text)
            except Exception as e:
                print("Błąd podczas tłumaczenia:", str(e))
    elif transQ == "nie":
        url = 'https://translate.google.com/'
        webbrowser.open(url)
    else:
        process_response("nie zrozumiałem czekam na kolejne polecenia")
def weather():
    process_response('Podaj lokalizację do sprawdzenia pogody')
    lokalizacja = speech(sr.Recognizer())
    print(f"Sprawdzam pogodę w {lokalizacja}...")

    url = f'https://wttr.in/{lokalizacja}?format=%C+%t+%w'
    odpowiedz = requests.get(url)

    if odpowiedz.status_code == 200:
        dane = odpowiedz.text
        print(f'Pogoda w {lokalizacja}:')
        print(dane)

        process_response(f'Pogoda w {lokalizacja}: {dane}')
    else:
        print('Nie udało się pobrać danych pogodowych.')
        process_response('Nie udało się pobrać danych pogodowych.')

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
def CalOpen():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        process_response("sprawdzić kalendarz czy dodać zdarzenie?")
        fraze = speech(sr.Recognizer())
        if fraze:
            if any(word in fraze for word in ["sprawdź", "podaj"]):

                service = build("calendar", "v3", credentials=creds)
                now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
                events_result = (
                    service.events()
                    .list(
                        calendarId="primary",
                        timeMin=now,
                        maxResults=10,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])

                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    # Parsuj datę i czas, a następnie wybierz tylko datę
                    start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                    process_response_cal(start_date.strftime("%Y-%m-%d"), event["summary"])
    except HttpError as error:
        print(f"An error occurred: {error}")            
def load_configuration():
    try:
        with open('dane.json', 'r') as file:
            config_data = json.load(file)
        return config_data
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None
def MailOpen(time_to_check):
    try:
        config_data = load_configuration()

        service = authenticate_and_build_service()
        if service:
            start_date = datetime.utcnow() - timedelta(hours=time_to_check)
            query = f"in:important after:{int(start_date.timestamp())}"

            emails = authenticate_and_fetch_emails(service, query)

            if emails:
                speak(f"Oto tytuły maili z ostatnich {time_to_check} godzin w folderze 'Important':")
                for i, email in enumerate(emails, start=1):
                    email_id = email['id']
                    try:
                        email_data = service.users().messages().get(userId="me", id=email_id).execute()
                        subject = next((header['value'] for header in email_data['payload']['headers'] if header['name'] == 'Subject'), 'Brak tematu')
                        speak(f"Tytuł maila {i}: {subject}")
                    except Exception as e:
                        print(f"Error fetching email details: {e}")
                        speak(f"Błąd podczas pobierania szczegółów maila {i}.")

            else:
                speak(f"Brak maili z ostatnich {time_to_check} godzin w folderze 'Important'.")
        else:
            speak("Wystąpił błąd podczas uwierzytelniania usługi Gmail.")
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania maili: {e}")
        speak("Wystąpił błąd podczas pobierania maili.")
def send_email_command():
    process_response("Podaj adres e-mail, podaj tylko część przed @gmail.com")
    email_name = speech(sr.Recognizer())
    to_address = email_name.lower() + "@gmail.com"
    process_response("Podaj temat e-maila")
    subject = speech(sr.Recognizer())

    speak("Proszę powiedz treść e-maila.")
    body = speech(sr.Recognizer())

    if body:
        try:
            service = authenticate_and_build_service2()
            
            if service:
                process_response("Czy na pewno chcesz wysłać e-mail?")
                send_confirmation=speech(sr.Recognizer)
                
                
                
                if send_confirmation == "tak":
                    send_email(service, to_address, subject, body)
                    process_response("E-mail został wysłany.")
                else:
                    process_response("Anulowano wysyłanie e-maila.")
            else:
                speak("Wystąpił błąd podczas uwierzytelniania usługi Gmail.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            speak("Wystąpił błąd podczas wysyłania e-maila.")
def add_cal():
    calendar_service = authenticate_and_build_calendar_service()

    if calendar_service:
        process_response("Podaj nazwę spotkania")
        summary = speech(sr.Recognizer())

        process_response("Podaj miesiąc w którym będzie spotkanie")
        start_month_date = speech(sr.Recognizer())
        start_month_number = get_month_number(start_month_date)

        if start_month_number:
            process_response("Podaj dzień w którym będzie spotkanie")
            start_day_date = speech(sr.Recognizer())
            start_day_number = word_to_number(start_day_date)
            
            process_response("Podaj czas rozpoczęcia spotkania godzina, minuta")
            start_time = speech(sr.Recognizer())

            process_response("Podaj czas spotkania w minutach, podaj tylko liczbę")
            duration_str = speech(sr.Recognizer())

            start_date = f"{start_month_number}-{start_day_number}"
            
            try:
                start_datetime_str = f"{datetime.now().year}-{start_date} {start_time}:00"
                start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")
                end_time = start_datetime + timedelta(minutes=int(duration_str))

                start_time_iso = start_datetime.isoformat()
                end_time_iso = end_time.isoformat()

                # Sprawdź konflikty przed dodaniem spotkania
                if not is_event_conflict(calendar_service, start_time_iso, end_time_iso):
                    add_event_to_calendar(calendar_service, summary, start_time_iso, end_time_iso)
                else:
                    process_response("Konflikt: Spotkanie w tym czasie już istnieje.")
            except ValueError:
                print("Błąd: Nieprawidłowy format daty i czasu. Upewnij się, że używasz poprawnego formatu.")
        else:
            print("Błędny miesiąc. Spróbuj ponownie.")
def toReport(service, rep_mail):
    process_response('Proszę podać treść maila.')
    treść_maila = speech(sr.Recognizer())

    if treść_maila:
        recipient_email = get_rep_mail_from_json()
        if recipient_email:
            send_report_email(service, recipient_email, 'RAPORT', treść_maila)

def get_rep_mail_from_json():
    try:
        with open("dane.json", 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data.get("Rep_Mail")
    except FileNotFoundError:
        print("File 'dane.json' not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return None


def create_form():
    def on_entry_click(event):
        if time_entry_var.get() == 'Czas odczytu maili (w godzinach)':
            time_entry_var.set('')
            time_entry.config(fg='black')

    def browse_file():
        file_path = filedialog.askopenfilename()

        if file_path:
            directory, original_filename = os.path.split(file_path)
            new_file_path = os.path.join(directory, "credentials.json")

            os.rename(file_path, new_file_path)

            file_var.set(new_file_path)

    def save_data(selected_file, time_interval, activation_word):
        data_to_save = {
            "selected_file": selected_file,
            "time_interval": time_interval,
            "activation_word": activation_word,
            "category": "kgebicz11@gmail.com",  
        }

        with open("dane.json", 'w', encoding='utf-8') as json_file:
            json.dump(data_to_save, json_file, ensure_ascii=False)

    def submit_form():
        selected_file = file_var.get()
        time_interval = time_entry_var.get()
        activation_word = activation_var.get()

        if not selected_file:
            result = messagebox.askquestion("Brak pliku", "Nie dodano pliku! Kontynuować bez pliku?")
            if result == 'yes':
                selected_file = "Brak pliku"
                save_data(selected_file, time_interval, activation_word)
                app.destroy()
                return
            else:
                return

        if not time_interval or time_interval == 'Czas odczytu maili (w godzinach)':
            messagebox.showerror("Błąd", "Nie uzupełniono czasu!")
            return

        project_folder = os.getcwd()
        destination_path = os.path.join(project_folder, os.path.basename(selected_file))

        try:
            os.rename(selected_file, destination_path)
        except FileNotFoundError as e:
            messagebox.showerror("Błąd", f"Plik nie został znaleziony: {e}")
            return
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas przenoszenia pliku: {e}")
            return

        save_data(destination_path, time_interval, activation_word)
        messagebox.showinfo("Sukces", "Dane zostały zapisane!")
    
    
    app = tk.Tk()
    app.title("Formularz Projektu")
    app.geometry("400x300")
    main_frame = tk.Frame(app)
    main_frame.pack(padx=10, pady=10)
    file_label = tk.Label(main_frame, text="Dodaj plik do projektu:")
    file_label.grid(row=0, column=0, sticky="w")

    file_var = tk.StringVar()
    file_entry = ttk.Entry(main_frame, textvariable=file_var, state="readonly")
    file_entry.grid(row=0, column=1, padx=(0, 5), sticky="w")

    browse_button = tk.Button(main_frame, text="Przeglądaj", command=browse_file)
    browse_button.grid(row=0, column=2, padx=(0, 5), sticky="w")

    time_entry_var = tk.StringVar()
    time_entry = ttk.Entry(main_frame, textvariable=time_entry_var)
    time_entry.grid(row=1, column=1, pady=5, sticky="w")

    time_label = tk.Label(main_frame, text="Czas odczytu maili (w godzinach):")
    time_label.grid(row=1, column=0, pady=5, sticky="w")

    time_entry.bind('<FocusIn>', on_entry_click)

    activation_label = tk.Label(main_frame, text="Słowo aktywacyjne:")
    activation_label.grid(row=2, column=0, pady=5, sticky="w")

    activation_options = ["cześć", "hej", "witam"]
    activation_var = tk.StringVar(main_frame)
    activation_var.set(activation_options[0])

    activation_menu = tk.OptionMenu(main_frame, activation_var, *activation_options)
    activation_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    spacer_label3 = tk.Label(main_frame, text="", pady=10)
    spacer_label3.grid(row=3, column=0, columnspan=3)

    submit_button = tk.Button(app, text="zapisz dane", command=submit_form)
    submit_button.pack()

    # Uruchom pętlę główną
    app.mainloop()




#Formularz
def run_on_first_start():
    if not os.path.isfile("Dane.json"):
        with open("Dane.json", "w") as file:
            create_form()
    else:
        thread = threading.Thread(target=Speech_Start_Stop)
        thread.start()

run_on_first_start()