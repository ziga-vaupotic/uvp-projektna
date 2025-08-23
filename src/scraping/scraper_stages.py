import re
import requests
import datetime
import classes
import loader
import export


def stages_information_tdf(tdf):
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