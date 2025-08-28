import re
import requests
import datetime
from .classes import Race, Climb, URL
from .loader import request



TABLE_PATTERN_ROW = re.compile(
    r'<tr[^>]+><td>(\d+)</td><td><a  href="([^<]*)">([^<]*)</a></td>'
    r'<td>(\d+(?:\.\d+)?)</td><td>(\d+(?:\.\d+)?)</td><td>(\d+)</td><td>(-?\d+)</td>.*?</tr>'
, re.DOTALL)


TABLE_PATTERN = re.compile(
    r'<h4>Longest</h4><table[^>]*>(.*?)</table>', re.DOTALL
)


def find_race(year: int, race_name: str) -> Race:
    """
    Funkcija poišče dirko, ki jo poda njen unikaten indeks
    race_name, nato vrne razred Race.
    """

    print(f"Nalagam glavno datoteko | {race_name} {year}")

    req = request(f"{URL}race/{race_name}/{year}")

    if(req.status_code != 200):
        assert(f"Podatkov o dirki iz leta {year} ni bilo mogoče pridobiti."
                f" Statusna koda: {req.status_code}")

    return Race(year, req.url, race_name)



def find_climbs(race: Race) -> list:
    """Funckija poišče vse vzpone ne dirki in vrne seznam teh."""

    req = request(f"{race.url}/route/climbs")

    if(req.status_code != 200):
        assert(f"Podatkov o vzponih dirke {race.name} iz leta {race.year} ni bilo mogoče pridobiti."
                f" Statusna koda: {req.status_code}")
        return []

    ## Poišči pravo tabelo

    table_match = TABLE_PATTERN.search(req.text)

    if not table_match:
        assert f"Tabele vzponov dirke {race.name} iz leta {race.year} ni bilo možno najti!"
        return []

    table_buffer = table_match.group(1)

    rows = TABLE_PATTERN_ROW.findall(table_buffer)

    if not rows:
        assert f"Pri tabeli vzponov {race.name} iz leta {race.year} je prišlo do napake!"
        return []

    return [Climb(row[1], row[2], row[3], row[4], row[5], row[6])
             for row in rows]
