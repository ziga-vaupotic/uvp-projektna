import re
import requests
import datetime
import classes
import loader
import export
import scraper_stages

TDF_FIRST_YEAR = 1903


def general_race_information(years: list, race_name: str) -> list:
    # funkcija vrne vse obstoječe podatke od dirkah

    races = []

    for i in years:

        print(f"Nalagam glavno datoteko | {race_name} {i}")

        request = loader.request(f"{classes.URL}race/{race_name}/{i}")

        if(request.status_code != 200):
            assert(f"Podatkov o dirki iz leta {i} ni bilo mogoče pridobiti."
                   f" Statusna koda: {request.status_code}")
            continue

        current_race = classes.Race(i, request.url, race_name)


        current_race.climbs = find_climbs(current_race)
        races.append(current_race)

    return races




def find_climbs(race: classes.Race) -> list:

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





giro = general_race_information(range(1930, 2025), "giro-d-italia")
vuelta = general_race_information(range(1930, 2025), "vuelta-a-espana")
tdf  = general_race_information(range(1930, 2025), "tour-de-france")

list_all = giro + vuelta + tdf

for x in list_all:
    find_climbs(x)
    scraper_stages.get_stages(x)
    scraper_stages.stages_information_tdf(x)


export.export_climbs(list_all)

export.export_stages(list_all)