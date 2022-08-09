import mysql.connector
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

## Logging kan være praktisk - husk å importere logging etter de andre bibliotekene for å slippe støy med logging fra dem

import logging.config
logging.config.dictConfig({'version': 1,'disable_existing_loggers': True})

filelog = logging.FileHandler("standardlogg.log");  filelog.setLevel(level = logging.INFO)
conslog = logging.StreamHandler();                  conslog.setLevel(level = logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s: %(message)s', handlers=[filelog, conslog])

## Lager en kobling til serveren: 
kobling = mysql.connector.connect(  host ="localhost",
                                    user = "importuser",
                                    password = "importere",
                                    database = "tolltest1",
                                    port = "3306",)

logging.info(f"Sjekker om koblingen fungerer: {kobling.is_connected()=}")
## Henter ut liste over alle kolonnene

tabell_navn = "lite_tabell"

cursor = kobling.cursor()
cursor.execute(f"SHOW columns FROM {tabell_navn}")
liste_over_alle_kolonner = [column[0] for column in cursor.fetchall()]

print(f"{liste_over_alle_kolonner = }")

def genererer_tegning():

    
    def lag_sporring():

        sporring = f"SELECT {kolonne}, count({kolonne}) FROM `lite_tabell` GROUP BY {kolonne} ORDER BY {kolonne}"
        logging.debug(f"Generert spørring: {sporring}")
        
        return sporring

    def hent_dataene():

        cursor = kobling.cursor()
        cursor.execute(sporring)
        dataene = cursor.fetchall()

        logging.debug(f"Antall rekker i kolonnen \'{kolonne}\': {len(dataene)}")

        return dataene


    def lag_df():

        dataene_df = pd.DataFrame(dataene,columns = ["Kategori", "Antall"])
        logging.debug(f"Differanse mellom data og df for kolonnen \'{kolonne}\': {len(dataene)-len(dataene_df)=}")
        return dataene_df

    def tegne_diagram():

        plt.pie(dataene_df["Antall"], labels=dataene_df["Kategori"]);
        #plt.savefig(f'books_read_{kolonne}.png') # Hvis man vil lagre grafen
        plt.show()  # Viktig å be om show for at grafene skal vises separat i Jupyter


    sporring = lag_sporring()
    dataene = hent_dataene() 
    dataene_df = lag_df()

    tegne_diagram()

    



interessante_kolonner = ['kategori', 'behstat', 'innfgjel', 'hervang', 'landkode', 'transpm',]
#interessante_kolonner = ['landkode', 'transpm',]
#interessante_kolonner = liste_over_alle_kolonner

logging.debug(f'Utfører spørringer mot følgende kolonner: {interessante_kolonner=}')

for kolonne in interessante_kolonner:

    genererer_tegning()

