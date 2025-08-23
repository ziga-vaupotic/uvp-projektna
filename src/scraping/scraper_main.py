import re
import requests
import datetime
import classes
import loader
import export

URL = "https://www.procyclingstats.com/"
TDF_FIRST_YEAR = 1903


def general_race_information(years = [], race = ""):
    # funkcija vrne vse obstoječe podatke od dirkah

    tdf_end = datetime.datetime.now().year #leto konca

    tdfs = []

    for i in (range(TDF_FIRST_YEAR, tdf_end) if years == [] else years):

        print(f"Nalagam glavno datoteko | {race} {i}")

        request = loader.request(f"{URL}race/{race}/{i}")

        if(request.status_code != 200):
            assert(f"Podatkov o dirki iz leta {i} ni bilo mogoče pridobiti."
                   f" Statusna koda: {request.status_code}")
            continue

        current_tdf = classes.Race(i, request.url, race)

        #for x in find_stages_by_list(request):
        #    current_tdf.add_stage(x)
        current_tdf.climbs = find_climbs(current_tdf)
        tdfs.append(current_tdf)

    return tdfs


def find_stages_by_list(request):
    pattern = r'<tr class=""><td>\d{0,2}/\d{0,2}</td>.*?href="(.*?)".*?</tr>'
    # samo url za zdaj, več podatkov dobimo na urlju.
    for match in re.findall(pattern, request.text):                
        # match je lahko empty, to pomeni, da je rest day!
        yield match


def find_climbs(race) -> list:

    request = loader.request(f"{race.url}/route/climbs")

    if(request.status_code != 200):
        assert(f"Podatkov o vzponih dirke iz leta {race.year} ni bilo mogoče pridobiti."
                f" Statusna koda: {request.status_code}")
        return None

    pattern_table = r'<h4>Longest</h4><table[^>]*>(.*?)</table>'

    table_match = re.search(pattern_table, request.text, re.DOTALL)

    if not table_match:
        assert(f"Tabele ni bilo možno najti!")
        return None

    table_buffer = table_match.group(1)

    pattern_table_row = re.compile(
        r'<tr[^>]+><td>(\d+)</td><td><a  href="([^<]*)">([^<]*)</a></td>'
        r'<td>(\d+(?:\.\d+)?)</td><td>(\d+(?:\.\d+)?)</td><td>(\d+)</td><td>(-?\d+)</td>.*?</tr>'
    , re.DOTALL)

    rows = pattern_table_row.findall(table_buffer)

    return_list = []

    for row in rows:
        return_list.append(classes.Climb(row[1], row[2], row[3], row[4], row[5], row[6]))

    return return_list





giro = general_race_information(range(2000, 2026), "giro-d-italia")
vuelta = general_race_information(range(2000, 2026), "vuelta-a-espana")
tdf  = general_race_information(range(2000, 2026), "tour-de-france")
#for x in tour:
#    print(x)
#    stages_tdf(x)

export.export_climbs(tdf + vuelta + giro, "tdf")
