import re
import requests
import datetime

def general_information_tdf(years = []):
    # funkcija vrne vse obstoječe podatke od dirkah

    tdf_start = 1903 # leto začetka
    tdf_end = datetime.datetime.now().year #leto konca

    urls = []

    for i in (range(tdf_start, tdf_end) if years == [] else years):

        request = requests.get(f"https://www.procyclingstats.com/race/tour-de-france/{i}")

        if(request.status_code != 200):
            assert(f"Podatkov o dirki iz leta {i} ni bilo mogoče pridobiti."
                   f" Statusna koda: {request.status_code}")
        else:
            rows = re.findall(r'<tr>(.*?)</tr>', request.text)
            print(rows)
            for row in rows:
                print(row)

    return urls

print(general_information_tdf([2015,  2024])) 