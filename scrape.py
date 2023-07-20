!pip install beautifulsoup4
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import os

# Huidige maand en jaar ophalen voor het bestandslabel
tijdstip = datetime.datetime.now().strftime('%Y%m')

# Logische namen van de kolommen
header = ['Postcode', 'Datum', 'Soort']

# Lees de postcodes in vanuit het CSV-bestand
postcodes = []
with open('pc4_2022.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    # Overslaan van de eerste regel (kop)
    next(reader)
    for row in reader:
        if len(row) > 0:
            postcodes.append(int(row[0]))

# Bestandspad
file_path = 'MiK-Nederland-PC4.csv'

# Controleren of het bestand al bestaat en de meest recente datum vinden
file_exists = os.path.isfile(file_path)
if file_exists:
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Overslaan van de headerrij
        next(reader)
        # Vind de meest recente datum in het bestand
        most_recent_date = max(datetime.datetime.strptime(row[1], '%d-%m-%Y') for row in reader)
else:
    # Als het bestand niet bestaat, wordt most_recent_date op None gezet
    most_recent_date = None

# Bestand openen in 'append' modus
with open(file_path, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    
    # Voeg header alleen toe als het bestand nog niet bestaat
    if not file_exists:
        writer.writerow(header)

    print(len(postcodes))
    for postcode in postcodes:
        time.sleep(2)
        print("Zoeken voor {}...".format(postcode))
        url = "https://www.politie.nl/mijn-buurt/misdaad-in-kaart/lijst?geoquery=" + str(postcode) + "&distance=5.0&categorie=1&categorie=2"
        content = requests.get(url)
        soup = BeautifulSoup(content.text, 'html.parser')
        stap1 = soup.find(id='crimemaps-list')
        if stap1 is not None:
            stap2 = stap1.find('tbody')
            if stap2 is not None:
                stap3 = stap2.find_all('tr')
                if len(stap3) > 0:
                    for melding in stap3:
                        datum = melding.find_all('td')[1::2][0].string
                        soort = melding.find_all('td')[2::3][0].string
                        
                        # Controleer of de datum recenter is dan de meest recente datum in het bestand
                        current_date = datetime.datetime.strptime(datum, '%d-%m-%Y')
                        if most_recent_date is None or current_date > most_recent_date:
                            writer.writerow([postcode, datum, soort])
