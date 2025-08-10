### Lazy loader za get requeste

import re
import requests
import os


class BufferResponse:
    """ To je wrapper za request razred. Omogoče nalaganje iz datotek """

    def __init__(self, text, url):
        self.text = text
        self.status_code = 200
        self.url = url

def request(url):
    """Pošlje GET request na podani URL in vrne odgovor."""

    match_url = re.findall(r"procyclingstats.com/(.*)/(.*)", url)

    if(not match_url):
        assert("URL mora biti v obliki procyclingstats.com/...")

    dir_path, buffer_file = match_url[0]

    dir_path = os.path.join(f"data/html/{dir_path}")
    buffer_file = f"{dir_path}/{buffer_file}.html"


    if os.path.exists(buffer_file):
        print(f"Nalagam iz datoteke: {dir_path}")
        return BufferResponse(open(buffer_file, "r", encoding="utf-8").read(), url)
    else:
        print(f"Shranjujem buffer v: {buffer_file} {dir_path}")

        os.makedirs(dir_path, exist_ok=True)
        response = requests.get(url)
        with open(buffer_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        return response
