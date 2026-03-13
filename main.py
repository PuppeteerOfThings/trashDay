#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: PuppeteerOfThings
Date: 2025-10-08
Description: Small script scraps the collection dates for rubbish from Providers Page in Stuttgart
"""

#import requests
import time
import os
from datetime import datetime
#from bs4 import BeautifulSoup
import logging
from playwright.sync_api import sync_playwright
#from flask import Flask

#class RubbishKalender:
    #dates = Json
    #Function which Collection is in the next three days
    #Function delete Memory
    #Setter und Getter Funktion

# -------------------------------
# Klassen
# -------------------------------
 
    

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(
    level=logging.INFO,  # Log-Level: zeigt alles ab INFO an
    format="%(asctime)s - %(levelname)s - %(message)s"  # Format der Ausgabe
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# -------------------------------
# Funktionen
# -------------------------------

def parse_arguments():
    """
    Kommandozeilenargumente parsen
    """
    pass

def fetch_dates ():
    logging.info("trying to fetch dates for the next 30 days")
    """
    Liefert die Mülldaten in folgender Form:
    {' Restabfall': [datetime.date(2025, 10, 24), datetime.date(2025, 11, 7), datetime.date(2025, 11, 21)], ' Bioabfall': [datetime.date(2025, 10, 23), datetime.date(2025, 10, 30), datetime.date(2025, 11, 6), datetime.date(2025, 11, 13), datetime.date(2025, 11, 20)], ' Altpapier': [datetime.date(2025, 10, 30), datetime.date(2025, 11, 20)], ' Gelber Sack': [datetime.date(2025, 11, 7)]}
    """
    for i in range(3): #Mehrere Versuche Vielleicht anders strukturieren
        with sync_playwright() as p:
            #Seite aufrufen
            browser = p.chromium.launch(headless=False, slow_mo=250) #Debug parameter
            page = browser.new_page()
            try:
                page.goto("https://service.stuttgart.de/lhs-services/aws/abfuhrtermine")
                #Seite bedienen
                page.get_by_placeholder("Straße").fill(os.getenv("STREET")) #Kandidat für Schnittstelle
                page.get_by_placeholder("Hnr.").fill(os.getenv("HOUSENR")) #Kandidat für Schnittstelle
                page.locator("#calendar_submit").click()
            except:
                #Logging Seite konnte nicht geladen oder bedient werden
                pass


            #Daten auslesen
            try:
                page.wait_for_selector("#awstable", state="visible") #Warten bis Tabelle da ist
                #a = 5/0
                rows = page.locator ('#awstable tr')
            except:
                print("geplanter Fehler")
                rows = None
                data = None
                #Logging Es konnten keine Daten ermittelt werden
            
            #Daten umwandeln
            try:
                data = {}
                rowNumber = rows.count()
                for i in range(rowNumber):
                    row = rows.nth(i) 
                    if row.locator("th").count()>0: #tableheader Zeilen Müllart
                        muellart = row.locator("th").all_inner_texts()[0]
                        muellart = muellart.strip()
                        data.setdefault(muellart,[]) #Wenn noch nicht im Dictionary enthalten hinzufügen
                    else:
                        dates_str = row.locator("td").all_inner_texts()[1]
                        date_obj = datetime.strptime(dates_str, "%d.%m.%Y").date()
                        # for date in listdates:
                        if date_obj not in data[muellart]: #Wenn datum noch nicht in der liste ist hinzufügen
                            data [muellart].append(date_obj)
            except NameError:
                data = {"error": "Keine Daten verfügbar"}
                pass
                # logging nicht vorhandenes Objekt
            else:
                #Fehler bei Datenumwandlung aufgetreten
                logging.info("Data tranformation without errors")
                pass
            

            browser.close()
            if data != {}: #Exit aus Loop, wenn Daten ermittelt wurden
                logging.info("Received Information from provider")
                break
            else:
                logging.info("fetching failed will retry in 4 minutes")
                time.sleep(240)

    #maybe editing Validation
    return data    

def main():
        
        #Logging "RubbishRemovalDates Service startet"
        logging.info("Rubbish Collection Dates providing Service started")
        #app.run(host="0.0.0.0", port=5000, debug=False)
        data= fetch_dates()
        print(data)



#Bsp. Response
# {
#     "Altpapier": [
#         "Thu, 30 Oct 2025 00:00:00 GMT",
#         "Thu, 20 Nov 2025 00:00:00 GMT"
#     ],
#     "Bioabfall": [
#         "Thu, 30 Oct 2025 00:00:00 GMT",
#         "Thu, 06 Nov 2025 00:00:00 GMT",
#         "Thu, 13 Nov 2025 00:00:00 GMT",
#         "Thu, 20 Nov 2025 00:00:00 GMT"
#     ],
#     "Gelber Sack": [
#         "Fri, 07 Nov 2025 00:00:00 GMT"
#     ],
#     "Restabfall": [
#         "Fri, 24 Oct 2025 00:00:00 GMT",
#         "Fri, 07 Nov 2025 00:00:00 GMT",
#         "Fri, 21 Nov 2025 00:00:00 GMT"
#     ]
# }


""" {
     "Altpapier": [
         "Thu, 30 Oct 2025 00:00:00 GMT",
         "Thu, 20 Nov 2025 00:00:00 GMT"
     ],
     "Bioabfall": [
         "Thu, 30 Oct 2025 00:00:00 GMT",
         "Thu, 06 Nov 2025 00:00:00 GMT",
         "Thu, 13 Nov 2025 00:00:00 GMT",
         "Thu, 20 Nov 2025 00:00:00 GMT"
     ],
     "Gelber Sack": [
         "Fri, 07 Nov 2025 00:00:00 GMT"
     ],
     "Restabfall": [
         "Fri, 24 Oct 2025 00:00:00 GMT",
         "Fri, 07 Nov 2025 00:00:00 GMT",
         "Fri, 21 Nov 2025 00:00:00 GMT"
     ]
} """

"""
daten = {
    "Restmüll": [Datum1, Datum2, Datum3],
    "Gelber-Sack": [Datum1, Datum2]
}
Kann folgendermaßen umgewandelt werden
json_string = json.dumps(daten, indent=4)
{
    "Restmüll":
        [
            "Datum1",
            "Datum2",
            "Datum3"
        ],
    "Gelber-Sack":
        [
            "Datum1",
            "Datum2"
        ]
} 
"""

if __name__ == "__main__":
    #args = parse_arguments()
    main()
