import requests

def pobierz_pogode(city):
    # Adres URL API MetaWeather
    url = f'https://www.metaweather.com/api/location/search/?query={city}'

    # Wyślij zapytanie HTTP
    response = requests.get(url)

    if response.status_code == 200:
        # Jeśli zapytanie było udane, pobierz pierwsze id lokalizacji
        woeid = response.json()[0]['woeid']

        # Utwórz nowe zapytanie, aby pobrać dane pogodowe na podstawie woeid
        url = f'https://www.metaweather.com/api/location/{woeid}/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return "Nie można pobrać danych pogodowych."
    else:
        return "Nie można znaleźć miasta."

miasto = "London"
wynik = pobierz_pogode(miasto)

if isinstance(wynik, str):
    print(wynik)  # Wyświetl komunikat o błędzie
else:
    print(f'Pogoda w {miasto}:')
    for day in wynik['consolidated_weather']:
        print(f'Data: {day["applicable_date"]}, '
              f'Min temperatura: {day["min_temp"]}, '
              f'Max temperatura: {day["max_temp"]}, '
              f'Opady: {day["weather_state_name"]}')
