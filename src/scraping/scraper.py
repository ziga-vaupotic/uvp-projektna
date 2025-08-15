import re
import requests
import datetime
import classes
import loader

URL = "https://www.procyclingstats.com/"
TDF_FIRST_YEAR = 1903


def general_information_tdf(years = []):
    # funkcija vrne vse obstoječe podatke od dirkah

    tdf_end = datetime.datetime.now().year #leto konca

    tdfs = []

    for i in (range(TDF_FIRST_YEAR, tdf_end) if years == [] else years):

        print(f"Nalagam glavno datoteko | Tour de france {i}")

        request = loader.request(f"{URL}race/tour-de-france/{i}")

        if(request.status_code != 200):
            assert(f"Podatkov o dirki iz leta {i} ni bilo mogoče pridobiti."
                   f" Statusna koda: {request.status_code}")
            continue

        current_tdf = classes.TourDeFrance(i, request.url)

        for x in find_stages_by_list(request):
            current_tdf.add_stage(x)

        tdfs.append(current_tdf)

    return tdfs


def find_stages_by_list(request):
    pattern = r'<tr class=""><td>\d{0,2}/\d{0,2}</td>.*?href="(.*?)".*?</tr>'
    # samo url za zdaj, več podatkov dobimo na urlju.
    for match in re.findall(pattern, request.text):                
        # match je lahko empty, to pomeni, da je rest day!
        yield match
        

def stages_tdf(tdf):
    for i, stage in enumerate(tdf.stages):

        print(f"Nalagam etapo {i} | Tour de france {tdf.year}")
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
            r'<div class="title ">Distance: </div><div class=" value" >(\d+\.?\d+).*?</div>.*?'
            r'<div class="title ">Vertical meters: </div><div class=" value" >(\d+\.?\d+).*?</div>.*?'
            r'</ul>'
        )

        data = re.findall(pattern, request.text, re.DOTALL)

        print(data)


        if(not data):
            assert(f"Etapa {i + 1} iz leta {tdf.year} nima splošnih informacij!")
            continue
        
        stage.set_data(data[0][0], data[0][1], data[0][2])  

        ## Za vsako etapo imamo različne seštevke. Skozi leta so se te seštevki spreminjali,
        ##  zato jih je treba najprej klasificirati.
        

        for x in find_gcs(request):
            find_leaderboard_stage(x[0])


        #    tdf.add_gcs(x)

        #for gc in tdf.gcs:
        #    print(gc)
        #    find_leaderboard_stage(gc[0])

def find_gcs(request):
    #(^[A-Z]+$)
    pattern_sestevki = (
        r'<a class="selectResultTab" data-id=".*?" data-stagetype="\d{1}" href="(.*?)">.*?</center>(.*?)</a>.*?'
    )

    data_sestevki = re.findall(pattern_sestevki, request.text, re.DOTALL)

    return data_sestevki


def find_leaderboard_stage(url_gc):
    request = loader.request(f"{URL}{url_gc}")

    pattern_time = (
        r'<tr>.*?</tr>'
)



tour = general_information_tdf([2025])

for x in tour:
    stages_tdf(x)
