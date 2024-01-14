import datetime, time
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
import json




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

                PanicWords = ["stop zero jeden", "stop 01","top 01"]
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
def process_response_cal(start, summary):
    speak(f"{start} - {summary}")
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
                process_response("chcesz sprawdzić czy wysłać")
                wyb=speech(sr.Recognizer())
                if any(word in wyb for word in ["sprawdź", "sprawdze", "check"]):
                    MailOpen()
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
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Warsaw',  # Change to your time zone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Warsaw',  # Change to your time zone
            },
        }

        created_event = calendar_service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {created_event.get("htmlLink")}')
    except HttpError as error:
        print(f"An error occurred: {error}")
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

#FUNCTIONs

def webOpen():
    process_response('już otwieram')
    webbrowser.open("https://google.com/search")
def webOpenwithQuestion():
    process_response('Co chcesz wyszukać?')
    query = speech(sr.Recognizer())

    if query:
        search_url = f"https://google.com/search?q={query}"
        process_response(f'Wyszukuję definicje dla: {query}')
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

        # Odczytujemy dane pogodowe odpowiedzią głosową
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
def MailOpen():
    query = "in:important"

    try:
        service = authenticate_and_build_service()
        if service:
            emails = authenticate_and_fetch_emails(service, query)

            if emails:
                speak("Oto tytuły ostatnich 3 maili w folderze 'Important':")
                for i, email in enumerate(emails[:3], start=1):
                    email_id = email['id']
                    email_data = service.users().messages().get(userId="me", id=email_id).execute()
                    subject = next(header['value'] for header in email_data['payload']['headers'] if header['name'] == 'Subject')
                    speak(f"Tytuł maila {i}: {subject}")
            else:
                speak("Brak maili w folderze 'Important'.")
        else:
            speak("Wystąpił błąd podczas uwierzytelniania usługi Gmail.")
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania maili: {e}")
        speak("Wystąpił błąd podczas pobierania maili.")

def send_email_command():
    process_response("podaj maila")
    mail = speech(sr.Recognizer())
    to_address = "kgebicz11@gmail.com"
    process_response("podaj temat")
    tem = speech(sr.Recognizer())
    subject = "testowy"
    
    speak("Prosze powiedz treść e-maila.")
    body = speech(sr.Recognizer())

    if body:
        try:
            service = authenticate_and_build_service2()
            if service:
                send_email(service, to_address, subject, body)
            else:
                speak("Wystąpił błąd podczas uwierzytelniania usługi Gmail.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
            speak("Wystąpił błąd podczas wysyłania e-maila.")
def add_cal():
    calendar_service = authenticate_and_build_calendar_service()

    if calendar_service:
        # Poproś użytkownika o podanie informacji
        process_response("Podaj nazwę spotkania")
        summary = speech(sr.Recognizer())

        process_response("Podaj miesiąc w którym będzie spotkanie")
        start_month_date = speech(sr.Recognizer())
        start_month_number = get_month_number(start_month_date)

        if start_month_number:
            process_response("Podaj dzień w którym będzie spotkanie")
            start_day_date = speech(sr.Recognizer())

            process_response("Podaj czas rozpoczęcia spotkania godzina, minuta")
            start_time = speech(sr.Recognizer())

            process_response("Podaj czas spotkania w minutach")
            duration_str = speech(sr.Recognizer())

            start_date = f"{start_month_number}-{start_day_date}"

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
def toReport(service):
    process_response('Proszę podać treść maila.')
    treść_maila = speech(sr.Recognizer())

    if treść_maila:
        send_report_email(service, 'kgebicz11@gmail.com', 'RAPORT', treść_maila)



#autoryzacja
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/calendar.readonly"]
CLIENT_SECRET_FILE = "credentials.json"  # Plik JSON pobrany z Konsoli Programisty Google
TOKEN_FILE = "token.json"
def authenticate_with_password(username, password):
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

    credentials = Credentials.from_authorized_user_info(
        client_id=flow.client_config["client_id"],
        client_secret=flow.client_config["client_secret"],
        scopes=SCOPES,
    )

    # Uzyskanie tokenu dostępu za pomocą loginu i hasła
    credentials.fetch_token(
        "https://oauth2.googleapis.com/token",
        authorization_response=None,
        username=username,
        password=password,
    )

    # Zapisz uzyskane poświadczenia do pliku
    credentials.to_json_file(TOKEN_FILE)

    # Zbuduj i zwróć obiekt usługi Gmail z uwierzytelnionymi danymi
    service = build("gmail", "v1", credentials=credentials)
    return service


#Formularz
def run_on_first_start():
    if not os.path.isfile("Dane.json"):
        with open("Dane.json", "w") as file:
            create_form()
def create_form():
    def submit_form():
        name = entry_name.get()
        email1 = entry_email1.get()
        password1 = entry_password1.get()

        data = {
            "Name": name,
            "Forms": [
                {"Name": "Email & Password", "Entries": [
                    {"Email": email1, "Password": password1}
                ]}
            ],
            "Greetings": greeting_var.get(),
            "TimePeriod": time_period_var.get()
        }

        with open("Dane.json", "w") as file:
            json.dump(data, file, indent=4)
            print("Dane zapisane do dane.json")
        root.destroy()
        process_file('Dane.json', 'Password', mode='encrypt')

    root = tk.Tk()
    root.title("Multiple Forms")

    # Tworzenie etykiet i pól do wprowadzania imienia
    label_name = tk.Label(root, text="Imię:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(root)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    # Ramka dla Email & Password
    frame_email_password = tk.LabelFrame(root, text="Email & Password")
    frame_email_password.grid(row=1, columnspan=2, padx=10, pady=5)

    label_email1 = tk.Label(frame_email_password, text="Email:")
    label_email1.grid(row=0, column=0, padx=10, pady=5)
    entry_email1 = tk.Entry(frame_email_password)
    entry_email1.grid(row=0, column=1, padx=10, pady=5)

    label_password1 = tk.Label(frame_email_password, text="Hasło:")
    label_password1.grid(row=1, column=0, padx=10, pady=5)
    entry_password1 = tk.Entry(frame_email_password, show="*")
    entry_password1.grid(row=1, column=1, padx=10, pady=5)

    # Przyciski wyboru i pole dla okresu czasu
    label_greetings = tk.Label(root, text="Pozdrowienia:")
    label_greetings.grid(row=2, column=0, padx=10, pady=5)
    greeting_var = tk.StringVar()
    select_button_hello = ttk.Checkbutton(root, text="Cześć", variable=greeting_var, onvalue="Cześć")
    select_button_hello.grid(row=2, column=1, padx=10, pady=5)
    select_button_hi = ttk.Checkbutton(root, text="Hej", variable=greeting_var, onvalue="Hej")
    select_button_hi.grid(row=2, column=2, padx=10, pady=5)
    select_button_bye = ttk.Checkbutton(root, text="Pa", variable=greeting_var, onvalue="Pa")
    select_button_bye.grid(row=2, column=3, padx=10, pady=5)

    label_time_period = tk.Label(root, text="Okres sprawdzania maili (w godzinach):")
    label_time_period.grid(row=3, column=0, padx=10, pady=5)
    time_period_var = tk.StringVar()
    time_period_entry = tk.Entry(root, textvariable=time_period_var)
    time_period_entry.grid(row=3, column=1, padx=10, pady=5)

    # Przycisk do przesyłania
    submit_button = tk.Button(root, text="Prześlij", command=submit_form)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()
    authenticate_with_password("123","123")
run_on_first_start()



thread = threading.Thread(target=Speech_Start_Stop)
thread.start()