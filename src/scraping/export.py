import classes
import os
import json

def export_tdf_cvs(tour_de_france):

    # splošne informacije o tour de francu sprava zapišemo v json.

    dir_path = os.path.join(f"{classes.DATA_FOLDER}/csv/{tour_de_france.year}/")

    os.makedirs(dir_path, exist_ok=True)

