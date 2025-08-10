import re
import requests
import datetime
import classes

TDF_URL = "https://www.procyclingstats.com/race/tour-de-france/"
TDF_FIRST_YEAR = 1903
DATA_FOLDER = "../data/"


def general_information_tdf(years = []):
    # funkcija vrne vse obstoječe podatke od dirkah

    tdf_end = datetime.datetime.now().year #leto konca

    tdfs = []

    for i in (range(TDF_FIRST_YEAR, tdf_end) if years == [] else years):

        request = requests.get(f"{TDF_URL}{i}")

        if(request.status_code != 200):
            assert(f"Podatkov o dirki iz leta {i} ni bilo mogoče pridobiti."
                   f" Statusna koda: {request.status_code}")
        else:
            current_tdf = classes.TourDeFrance(i, request.url)

            pattern = r'<tr class=""><td>\d{0,2}/\d{0,2}</td>.*?href="(.*?)".*?</tr>'
            # samo url za zdaj, več podatkov dobimo na urlju.
            for match in re.findall(pattern, request.text):                
                # match je lahko empty, to pomeni, da je rest day!
                current_tdf.add_stage(classes.Stage(match))
            
            tdfs.append(current_tdf)

    return tdfs

print(general_information_tdf([2015,  2024])) 