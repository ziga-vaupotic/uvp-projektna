from .classes import Race, Stage, URL
from .loader import request

import re
from typing import Iterator

## Nadje pravilno table za etape. Vrne html tabelo
STAGE_FIND_TABLE_PATTERN = re.compile(
        r'<h4>Stages</h4>.*?<tbody>(.*?)'
        r'</tbody></table></div>'
        , re.DOTALL )

## V tabeli poišče vse etape dirke. Vrne url etape
STAGE_TABLE_PATTERN = re.compile(
        r'<tr class=""><td>\d{0,2}/\d{0,2}</td>.*?href="(.*?)".*?</tr>'
        , re.DOTALL )

## Poišče vse seštevke in njihove data indekse.
GCS_PATTERN = re.compile(
        r'<a class="selectResultTab" data-id="(\d+)" data-stagetype="(\d{1})" href="[^<]*">.*?'
        r'</center>(.*?)</a>.*?'
        ,re.DOTALL)

## Splošne informaicje, tj. datum, tip etape, dolžina, višinska razlika
STAGE_INFO_PATTERN = re.compile(
    r'<ul class="list keyvalueList lineh16 fs12" >.*?'
    r'<div class="title ">Date:  </div><div class=" value" >(.*?)</div>.*?'
    r'<div class="title ">Avg. speed winner: </div><div class=" value" >(\d*(?:\.\d+)?).*?</div>.*?'
    r'<div class="title ">Distance: </div><div class=" value" >(\d+(?:\.\d+)?).*?</div>.*?'
    r'<div class="title ">Parcours type: </div><div class=" value" ><span class="icon profile p(\d) mg_rp4 "></span></div>.*?'
    r'<div class="title ">ProfileScore: </div><div class=" value" >(\d*).*?</div>.*?'
    r'<div class="title ">Vertical meters: </div><div class=" value" >(\d*(?:\.\d+)?).*?</div>.*?'
    r'</ul>'
    , re.DOTALL)


def find_stages(race: Race) -> Iterator[str]:
    """ Poišče vse etape na dirki. Funkcija vrača
    Iterator s pomočjo yield in ne seznama, za lažjo
    po uporabo. """

    req = request(race.url)

    table = STAGE_FIND_TABLE_PATTERN.search(req.text)
    if (not table):
        assert f"Tabela etap {race.name} leta {race.year} ni na voljo!"
        return None

    # samo url za zdaj, več podatkov dobimo na urlju.
    for i, match in enumerate(STAGE_TABLE_PATTERN.findall(table.group(1))):                
        # match je lahko empty, to pomeni, da je rest day!
        yield Stage(i + 1, match)


def find_stage_data(stage: Stage, race: Race) -> list:
    """ Poišče podatke o etapi in vrne podatke v obliki seznama. """

    # Funckija poišče vse informacije o dirkah

    print(f"Nalagam etapo {stage.stage_num} | {race.name} {race.year}")

    if(stage.stage_url == ""):
        assert f"Etapa {stage.stage_url} je rest day! "
        return []

    req = request(f"{URL}{stage.stage_url}")

    if(req.status_code != 200):
        assert(f"Podatkov o etapi {stage.stage_num} iz dirke {race.name} {race.year} ni bilo mogoče pridobiti."
            f" Statusna koda: {req.status_code}")
        return []

    ## Parcourse type (tip etape) je zapisan v obliki icon packa. Zato pogledamo ime ikone

    data = STAGE_INFO_PATTERN.search(req.text)

    if(not data):
        assert(f"Etapa {stage.stage_num} dirke {race.name} iz leta {race.year} nima splošnih informacij!")
        return []
    
    return list(data.groups())


def find_gcs(stage: Stage) -> list:
    """
    Poišče vse skupne seštevke in vrne seznam teh.
    Seznam je v obliki (data_id, gc_type, url_get_request, 'gc name')
    """

    print(f"Nalagam seštevke za etapo {stage.stage_num}")

    req = request(f"{URL}{stage.stage_url}")

    data = GCS_PATTERN.findall(req.text)

    if(not data):
        assert(f"Etapa {stage.stage_num} dirke nima seštevkov!")
        return []

    return data


#def find_leaderboard_stage(request: requests.Request, data_id: int) -> list:
    # Funkcija poišče vse seštevke (skupni, gorski, ...)

#    pattern_table = (
#        rF'<div id="resultsCont"><div class=".*?" data-id="{data_id}".*?'
#        r'</div></div>'
#    )

#    table = (re.search(pattern_table, request.text, re.DOTALL))

#    if (table == []):
#        assert(f"Tabela za {data_id} ni na voljo!")
#        return None


#    pattern_table_quary  = (
#        r'<a data-ct=".*?" href="(.?*)">.*?'
#        r'</td>>'
#    )
#
#    table_enteries = (re.findall(pattern_table, request.text, re.DOTALL))
#
#    pass