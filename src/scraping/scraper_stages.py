import re
import requests
import datetime
import classes
import loader
import export



def get_stages(race):
    request = loader.request(race.url)

    for x in find_stages_by_list(race, request):
            print(x)
            race.add_stage(x)

def find_stages_by_list(race, request):

    pattern_table = (
        r'<h4>Stages</h4>.*?<tbody>(.*?)'
        r'</tbody></table></div>'
    )

    table = (re.search(pattern_table, request.text, re.DOTALL))
    if (not table):
        print(f"Tabela etap {race.name} leta {race.year} ni na voljo!")
        return None


    pattern = r'<tr class=""><td>\d{0,2}/\d{0,2}</td>.*?href="(.*?)".*?</tr>'
    # samo url za zdaj, več podatkov dobimo na urlju.
    for match in re.findall(pattern, table.group(1)):                
        # match je lahko empty, to pomeni, da je rest day!
        yield match


def stages_information_tdf(tdf):
    for i, stage in enumerate(tdf.stages):

        print(f"Nalagam etapo {i} | {tdf.name} {tdf.year}")
        if(stage.stage_url == ""):
            assert(f"Etapa {stage.stage_url} je rest day! ")
            continue

        request = loader.request(f"{classes.URL}{stage.stage_url}")

        if(request.status_code != 200):
            assert(f"Podatkov o etapi {i + 1} iz leta {tdf.year} ni bilo mogoče pridobiti."
                f" Statusna koda: {request.status_code}")
            continue

        ## Splošne informaicje, tj. datum, tip etape, dolžina, višinska razlika

        pattern = (
            r'<ul class="list keyvalueList lineh16 fs12" >.*?'
            r'<div class="title ">Date:  </div><div class=" value" >(.*?)</div>.*?'
            r'<div class="title ">Avg. speed winner: </div><div class=" value" >(\d*(?:\.\d+)?).*?</div>.*?'
            r'<div class="title ">Distance: </div><div class=" value" >(\d+(?:\.\d+)?).*?</div>.*?'
            r'<div class="title ">Parcours type: </div><div class=" value" ><span class="icon profile p(\d) mg_rp4 "></span></div>.*?'
            r'<div class="title ">ProfileScore: </div><div class=" value" >(\d*).*?</div>.*?'
            r'<div class="title ">Vertical meters: </div><div class=" value" >(\d*(?:\.\d+)?).*?</div>.*?'
            r'</ul>'
        )

        ## Parcourse type (tip etape) je zapisan v obliki icon packa. Zato pogledamo ime ikone

        data = re.search(pattern, request.text, re.DOTALL)

        print(data)


        if(not data):
            assert(f"Etapa {i + 1} iz leta {tdf.year} nima splošnih informacij!")
            continue
        
        try:
            stage.set_data(data.group(1), data.group(3), data.group(2), data.group(5), data.group(6), data.group(4))  
        except:
            pass
        ## Za vsako etapo imamo različne seštevke. Skozi leta so se te seštevki spreminjali,
        ##  zato jih je treba najprej klasificirati.
        

        #for x in find_gcs(request):
        #    find_leaderboard_stage(request, x[0])

        #pass


def find_gcs(request):
    # The function returns a tuple (data_id, gc_type, url_get_request, 'gc name')
    #(^[A-Z]+$)
    pattern_sestevki = (
        r'<a class="selectResultTab" data-id="(\d+)" data-stagetype="(\d{1})" href="[^<]*">.*?</center>(.*?)</a>.*?'
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

    table = (re.search(pattern_table, request.text, re.DOTALL))

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