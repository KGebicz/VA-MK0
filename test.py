{
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from datetime import datetime, timedelta
# import pyttsx3
# import speech_recognition as sr
# import threading
# from email.mime.text import MIMEText
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# import base64



# def speak(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

# def process_response(response):
#     speak(response)
# def process_response_cal(start, summary):
#     speak(f"{start} - {summary}")
# def speech(r):
#     with sr.Microphone() as source2:
#         try:
#             print("Rozpoczynam nasłuchiwanie...")
#             audio2 = r.listen(source2, timeout=0.0)
#             MyText = r.recognize_google(audio2, language="pl")
#             MyText = MyText.lower()
        
#             print("Rozpoznano tekst: {}".format(MyText))
#             return MyText
        
#         except sr.UnknownValueError:
#             print("Nie rozpoznano żadnej wypowiedzi.")
#             return None
        
#         except sr.RequestError as e:
#             print(f"Błąd związany z usługą rozpoznawania mowy: {e}")
#             return None

# def send_report_email(service, recipient_email, subject, body):
#     message = create_message(sender='TWOJ_ADRES_EMAIL@gmail.com', to=recipient_email, subject=subject, body=body)
#     send_message(service, 'me', message)

# def create_message(sender, to, subject, body):
#     message = MIMEText(body)
#     message['to'] = to
#     message['from'] = sender
#     message['subject'] = subject
#     return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# def send_message(service, user_id, message):
#     try:
#         message = service.users().messages().send(userId=user_id, body=message).execute()
#         print('Message Id: %s' % message['id'])
#         return message
#     except HttpError as error:
#         print(f'An error occurred: {error}')

# def setup_gmail_api():
#     SCOPES = ['https://www.googleapis.com/auth/gmail.send']
#     creds = None
#     # The file token3.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token3.json'):
#         creds = Credentials.from_authorized_user_file('token3.json')
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token3.json', 'w') as token:
#             token.write(creds.to_json())
#     return build('gmail', 'v1', credentials=creds)

# def Speech_Start_Stop():
#     r = sr.Recognizer()
#     service = setup_gmail_api()

#     while True:
#         try:
#             with sr.Microphone() as source2:
#                 print("Czekam na wypowiedź...")
#                 audio2 = r.listen(source2, timeout=0.0)
#                 MyText = r.recognize_google(audio2, language="pl")
#                 MyText = MyText.lower()

#                 print("Rozpoznano tekst: {}".format(MyText))

#                 # Sprawdzamy, czy wypowiedziano "cześć" i reagujemy odpowiednio
#                 if "cześć" in MyText:
#                     print("Wykryto wypowiedź 'cześć'. Uruchamiam odpowiednią akcję.")
#                     action(service)

#                 PanicWords = ["stop zero jeden", "stop 01", "top 01", "stop 0,1"]
#                 # Sprawdzamy, czy wypowiedziano którekolwiek z słów kluczowych z PanicWords
#                 if any(word in MyText for word in PanicWords):
#                     print("Wykryto wypowiedź z listy słów kluczowych. Zatrzymuję program.")
#                     break

#         except sr.UnknownValueError:
#             print("Nie rozpoznano żadnej wypowiedzi.")
    
#         except sr.RequestError as e:
#             print(f"Błąd związany z usługą rozpoznawania mowy: {e}")

# def action(service):
#     process_response('co chcesz zrobić?')
#     fraze = speech(sr.Recognizer())

#     if fraze:
#         if "raport" in fraze:
#             process_response('Proszę podać treść maila.')
#             treść_maila = speech(sr.Recognizer())

#             if treść_maila:
#                 send_report_email(service, 'kgebicz11@gmail.com', 'RAPORT', treść_maila)
# # Rozpocznij wątek nasłuchiwania
# thread = threading.Thread(target=Speech_Start_Stop)
# thread.start()

# import tkinter as tk
# from tkinter import ttk
# import json

# def create_form():
#     def submit_form():
#         name = entry_name.get()
#         email1 = entry_email1.get()
#         password1 = entry_password1.get()

#         data = {
#             "Name": name,
#             "Forms": [
#                 {"Name": "Email & Password", "Entries": [
#                     {"Email": email1, "Password": password1}
#                 ]},
#                 {"Name": "Spotyfi", "Entries": [
#                     {"Email": email2, "Password": password2}
#                 ]},
#                 {"Name": "Storytell", "Entries": [
#                     {"Email": email3, "Password": password3}
#                 ]}
#             ],
#             "Greetings": greeting_var.get(),
#             "TimePeriod": time_period_var.get()
#         }

#         with open("Dane.json", "w") as file:
#             json.dump(data, file, indent=4)
#             print("Dane zapisane do dane.json")
#         root.destroy()
#         process_file('Dane.json', 'Password', mode='encrypt')

#     root = tk.Tk()
#     root.title("Multiple Forms")

#     # Tworzenie etykiet i pól do wprowadzania imienia
#     label_name = tk.Label(root, text="Imię:")
#     label_name.grid(row=0, column=0, padx=10, pady=5)
#     entry_name = tk.Entry(root)
#     entry_name.grid(row=0, column=1, padx=10, pady=5)

#     # Ramka dla Email & Password
#     frame_email_password = tk.LabelFrame(root, text="Email & Password")
#     frame_email_password.grid(row=1, columnspan=2, padx=10, pady=5)

#     label_email1 = tk.Label(frame_email_password, text="Email:")
#     label_email1.grid(row=0, column=0, padx=10, pady=5)
#     entry_email1 = tk.Entry(frame_email_password)
#     entry_email1.grid(row=0, column=1, padx=10, pady=5)

#     label_password1 = tk.Label(frame_email_password, text="Hasło:")
#     label_password1.grid(row=1, column=0, padx=10, pady=5)
#     entry_password1 = tk.Entry(frame_email_password, show="*")
#     entry_password1.grid(row=1, column=1, padx=10, pady=5)

#     # Przyciski wyboru i pole dla okresu czasu
#     label_greetings = tk.Label(root, text="Pozdrowienia:")
#     label_greetings.grid(row=2, column=0, padx=10, pady=5)
#     greeting_var = tk.StringVar()
#     select_button_hello = ttk.Checkbutton(root, text="Cześć", variable=greeting_var, onvalue="Cześć")
#     select_button_hello.grid(row=2, column=1, padx=10, pady=5)
#     select_button_hi = ttk.Checkbutton(root, text="Hej", variable=greeting_var, onvalue="Hej")
#     select_button_hi.grid(row=2, column=2, padx=10, pady=5)
#     select_button_bye = ttk.Checkbutton(root, text="Pa", variable=greeting_var, onvalue="Pa")
#     select_button_bye.grid(row=2, column=3, padx=10, pady=5)

#     label_time_period = tk.Label(root, text="Okres sprawdzania maili (w godzinach):")
#     label_time_period.grid(row=3, column=0, padx=10, pady=5)
#     time_period_var = tk.StringVar()
#     time_period_entry = tk.Entry(root, textvariable=time_period_var)
#     time_period_entry.grid(row=3, column=1, padx=10, pady=5)

#     # Przycisk do przesyłania
#     submit_button = tk.Button(root, text="Prześlij", command=submit_form)
#     submit_button.grid(row=4, column=0, columnspan=2, pady=10)

#     root.mainloop()
# create_form()
}



import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import json

def on_entry_click(event):
    if time_entry_var.get() == 'Czas odczytu maili (w godzinach)':
        time_entry_var.set('')
        time_entry.config(fg='black')

def browse_file():
    file_path = filedialog.askopenfilename()
    file_var.set(file_path)

def submit_form():
    selected_file = file_var.get()
    time_interval = time_entry_var.get()
    activation_word = activation_var.get()

    if not selected_file:
        result = messagebox.askquestion("Brak pliku", "Nie dodano pliku! Kontynuować bez pliku?")
        if result == 'yes':
            # Kontynuuj bez pliku
            selected_file = "Brak pliku"

            # Zapisz dane do pliku JSON
            save_data(selected_file, time_interval, activation_word)

            # Zamknij okno
            app.destroy()
            return
        else:
            # Uzupełnij dane
            return

    if not time_interval or time_interval == 'Czas odczytu maili (w godzinach)':
        messagebox.showerror("Błąd", "Nie uzupełniono czasu!")
        return

    # Zapisz dane do pliku JSON
    save_data(selected_file, time_interval, activation_word)

    # Tutaj możesz użyć pobranych wartości do dalszej obróbki
    print(f"Selected File: {selected_file}")
    print(f"Time Interval: {time_interval} hours")
    print(f"Activation Word: {activation_word}")

    # Dodano messagebox z informacją o zapisie
    messagebox.showinfo("Sukces", "Dane zostały zapisane!")

def save_data(selected_file, time_interval, activation_word):
    data_to_save = {
        "selected_file": selected_file,
        "time_interval": time_interval,
        "activation_word": activation_word
    }

    with open("dane.json", 'w') as json_file:
        json.dump(data_to_save, json_file)

# Utwórz główne okno aplikacji
app = tk.Tk()
app.title("Formularz Projektu")

# Ustaw rozmiar okna
app.geometry("400x300")

# Utwórz ramkę główną
main_frame = tk.Frame(app)
main_frame.pack(padx=10, pady=10)

# Dodaj elementy do formularza w ramce
file_label = tk.Label(main_frame, text="Dodaj plik do projektu:")
file_label.grid(row=0, column=0, sticky="w")

file_var = tk.StringVar()
file_entry = ttk.Entry(main_frame, textvariable=file_var, state="readonly")
file_entry.grid(row=0, column=1, padx=(0, 5), sticky="w")

browse_button = tk.Button(main_frame, text="Przeglądaj", command=browse_file)
browse_button.grid(row=0, column=2, padx=(0, 5), sticky="w")

# Dodaj entry dla ilości godzin
time_entry_var = tk.StringVar()
time_entry = ttk.Entry(main_frame, textvariable=time_entry_var)
time_entry.grid(row=1, column=1, pady=5, sticky="w")

time_label = tk.Label(main_frame, text="Czas odczytu maili (w godzinach):")
time_label.grid(row=1, column=0, pady=5, sticky="w")

# Dodaj obsługę zdarzenia dla kliknięcia w pole tekstowe
time_entry.bind('<FocusIn>', on_entry_click)

activation_label = tk.Label(main_frame, text="Słowo aktywacyjne:")
activation_label.grid(row=2, column=0, pady=5, sticky="w")

activation_options = ["cześć", "hej", "witam"]
activation_var = tk.StringVar(main_frame)
activation_var.set(activation_options[0])  # Domyślna wartość

activation_menu = tk.OptionMenu(main_frame, activation_var, *activation_options)
activation_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Dodaj pusty element jako spacer
spacer_label3 = tk.Label(main_frame, text="", pady=10)
spacer_label3.grid(row=3, column=0, columnspan=3)

submit_button = tk.Button(app, text="zapisz dane", command=submit_form)
submit_button.pack()

# Uruchom pętlę główną
app.mainloop()
