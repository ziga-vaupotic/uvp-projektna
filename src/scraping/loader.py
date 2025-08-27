from .classes import SAVE_HTMLS, DATA_FOLDER


import re
import requests
import os


def request(url) -> requests.Request:
    """
    Vrne request razred za podan URL. 
    Če je datoteka iz URL-ja že na računalniku jo naloži 
    iz data/html, drugače pošlje GET request  na URL
    in shrani datoteko. V kolikor SAVE_HTMLS ni vklopljen 
    enostavno vedno pošlje GET request na naslov.
    """

    if not SAVE_HTMLS:
        return requests.get(url)

    # pogleda, če je URL pravilne oblike
    match_url = re.search(r"procyclingstats.com/(.*)/(.*)", url)

    if(not match_url):
        assert "URL mora biti v obliki procyclingstats.com/..."

    # naredi datoteko oblike html/{relative_url_patj} 
    try:
        dir_path, buffer_file = [match_url.group(1), match_url.group(2)]
    except:
        assert f"Prišlo je do napake pri pregledovanju URL! {url}"
        return None

    dir_path = os.path.join(f"{DATA_FOLDER}/html/{dir_path}")
    buffer_file = f"{dir_path}/{buffer_file}.html"


    # Če datoteka že obstaja, jo naložimo iz data/html
    if os.path.exists(buffer_file):
        response = requests.Response()

        response._content = open(buffer_file, "rb").read()
        response.encoding ="utf-8"
        response.url = url
        response.status_code = 200

        return response
    
    # V nasportnem primeru jo pridobimo in shranimo.    
    os.makedirs(dir_path, exist_ok=True)
    response = requests.get(url)
    with open(buffer_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    return response
