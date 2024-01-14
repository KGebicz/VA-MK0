import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pyttsx3
import speech_recognition as sr
import threading
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64



def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_response(response):
    speak(response)
def process_response_cal(start, summary):
    speak(f"{start} - {summary}")
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

def send_report_email(service, recipient_email, subject, body):
    message = create_message(sender='TWOJ_ADRES_EMAIL@gmail.com', to=recipient_email, subject=subject, body=body)
    send_message(service, 'me', message)

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

def Speech_Start_Stop():
    r = sr.Recognizer()
    service = setup_gmail_api()

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
                    action(service)

                PanicWords = ["stop zero jeden", "stop 01", "top 01", "stop 0,1"]
                # Sprawdzamy, czy wypowiedziano którekolwiek z słów kluczowych z PanicWords
                if any(word in MyText for word in PanicWords):
                    print("Wykryto wypowiedź z listy słów kluczowych. Zatrzymuję program.")
                    break

        except sr.UnknownValueError:
            print("Nie rozpoznano żadnej wypowiedzi.")
        
        except sr.RequestError as e:
            print(f"Błąd związany z usługą rozpoznawania mowy: {e}")

def action(service):
    process_response('co chcesz zrobić?')
    fraze = speech(sr.Recognizer())

    if fraze:
        if "raport" in fraze:
            process_response('Proszę podać treść maila.')
            treść_maila = speech(sr.Recognizer())

            if treść_maila:
                send_report_email(service, 'kgebicz11@gmail.com', 'RAPORT', treść_maila)
# Rozpocznij wątek nasłuchiwania
thread = threading.Thread(target=Speech_Start_Stop)
thread.start()