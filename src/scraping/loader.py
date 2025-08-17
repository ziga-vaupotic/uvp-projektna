### Lazy loader za get requeste

import re
import requests
import os
import classes


def request(url):

    if classes.SAVE_HTMLS == False:
        return requests.get(url)

    """Pošlje GET request na podani URL in vrne odgovor."""

    match_url = re.findall(r"procyclingstats.com/(.*)/(.*)", url)

    if(not match_url):
        assert("URL mora biti v obliki procyclingstats.com/...")

    dir_path, buffer_file = match_url[0]

    dir_path = os.path.join(f"{classes.DATA_FOLDER}/html/{dir_path}")
    buffer_file = f"{dir_path}/{buffer_file}.html"


    if os.path.exists(buffer_file):

        # Mimika requests response za datoteko, ki je že na računalniku

        response = requests.Response()

        response._content = open(buffer_file, "rb").read()
        response.encoding ="utf-8"
        response.url = url
        response.status_code = 200

        return response
    else:
        #print(f"Shranjujem buffer v: {buffer_file} {dir_path}")
        os.makedirs(dir_path, exist_ok=True)
        response = requests.get(url)
        with open(buffer_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        return response
