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
    
   
def Take_data_to_login(choice):
    with open('rep.json', 'r') as file:
        data = json.load(file)

    for element in data:
        for platforma, dane in element.items():
            if platforma == choice:
                login = dane.get('login')
                password = dane.get('password')
                print(f"Platforma: {platforma}, Login: {login}, Hasło: {password}")

 
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
        Take_data_to_login("gmail")
        print(Take_data_to_login)
        #TODOD pobieranie danycb z json  i wpisuwanie 
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
                    gatunek=speech
            else:
                print("Co mam puścić?")
                track_to_play = speech
                play_spotify(track_to_play)
    else:
        print("Puszcze coś z listy top 100.")

        
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
        

def run_on_first_start():
    if not os.path.isfile("form_data.json"):
        with open("form_data.json", "w") as file:
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

        with open("form_data.json", "w") as file:
            json.dump(data, file, indent=4)
            print("Data saved to form_data.json")
        root.destroy()

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