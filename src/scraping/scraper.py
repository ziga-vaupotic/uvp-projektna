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
    #print(table_buffer)
    pattern_table_row = re.compile(
        r'<tr[^>]+><td>(\d+)</td><td><a  href="([^<]*)">([^<]*)</a></td>'
        r'<td>(\d+(?:\.\d+)?)</td><td>(\d+(?:\.\d+)?)</td><td>(\d+)</td><td>(-?\d+)</td>.*?</tr>'
    , re.DOTALL)

    rows = pattern_table_row.findall(table_buffer)

    return_list = []

    for row in rows:
        return_list.append(classes.Climb(row[1], row[2], row[3], row[4], row[5], row[6]))

    return return_list

def stages_tdf(tdf):
    for i, stage in enumerate(tdf.stages):

        print(f"Nalagam etapo {i} | {tdf.name} {tdf.year}")
        if(stage.stage_url == ""):
            assert(f"Etapa {stage.stage_url} je rest day! ")
            continue

        request = loader.request(f"{URL}{stage.stage_url}")

        if(request.status_code != 200):
            assert(f"Podatkov o etapi {i + 1} iz leta {tdf.year} ni bilo mogoče pridobiti."
                f" Statusna koda: {request.status_code}")
            continue

        ## Splošne informaicje, tj. datum, tip etape, dolžina, višinska razlika

        pattern = (
            r'<ul class="list keyvalueList lineh16 fs12" >.*?'
            r'<div class="title ">Date:  </div><div class=" value" >(.*?)</div>.*?'
            r'<div class="title ">Distance: </div><div class=" value" >(\d+(?:\.\d+)?).*?</div>.*?'
            r'<div class="title ">Vertical meters: </div><div class=" value" >(\d+(?:\.\d+)?).*?</div>.*?'
            r'</ul>'
        )

        data = re.find(pattern, request.text, re.DOTALL)

        print(data)


        if(not data):
            assert(f"Etapa {i + 1} iz leta {tdf.year} nima splošnih informacij!")
            continue
        
        stage.set_data(data.group(1), data.group(2), data.group(3))  

        ## Za vsako etapo imamo različne seštevke. Skozi leta so se te seštevki spreminjali,
        ##  zato jih je treba najprej klasificirati.
        

        for x in find_gcs(request):
            find_leaderboard_stage(request, x[0])

        pass

        #    tdf.add_gcs(x)

        #for gc in tdf.gcs:
        #    print(gc)
        #    find_leaderboard_stage(gc[0])

def find_gcs(request):
    # The function returns a tuple (data_id, gc_type, url_get_request, 'gc name')
    #(^[A-Z]+$)
    pattern_sestevki = (
        r'<a class="selectResultTab" data-id="(\d+)" data-stagetype="(\d{1})" href="(.*?)">.*?</center>(.*?)</a>.*?'
    )

    data_sestevki = re.findall(pattern_sestevki, request.text, re.DOTALL)

    #print(data_sestevki)

    return data_sestevki


def find_leaderboard_stage(request: requests.Request, data_id: int ):

    #print(data_id)
    pattern_table = (
        rF'<div id="resultsCont"><div class=".*?" data-id="{data_id}".*?'
        r'</div></div>'
    )

    table = (re.findall(pattern_table, request.text, re.DOTALL))

    if (table == []):
        assert(f"Tabela za {data_id} ni na voljo!")
        return None


    pattern_table_quary  = (
        r'<td class="ridername ">.*?'
        r'<a data-ct=".*?" href="(.?*)">.*?'
        r'</td>>'
    )

    table_enteries = (re.findall(pattern_table, request.text, re.DOTALL))

    #request = loader.request(f"{URL}{url_gc}")

    #pattern_time = (
    #    r'<tr>.*?</tr>'
#)
    pass


# giro-d-italia, tour-de-france, vuelta-a-espana


giro = general_race_information(range(2000, 2026), "giro-d-italia")
vuelta = general_race_information(range(2000, 2026), "vuelta-a-espana")
tdf  = general_race_information(range(2000, 2026), "tour-de-france")
#for x in tour:
#    print(x)
#    stages_tdf(x)

export.export_climbs(tdf + vuelta + giro, "tdf")
