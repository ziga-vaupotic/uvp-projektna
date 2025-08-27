from .classes import DATA_FOLDER, Climb, Stage
import os
import json
import csv

def export_climbs(list_of_tours) -> bool: 

    # najprej naredimo mape v data/ 

    dir_path = os.path.join(f"{DATA_FOLDER}csv/")
    os.makedirs(dir_path, exist_ok=True)

    print(dir_path)

    with open(dir_path + "climbs.csv", "w+", encoding="utf-8") as csvfile:

        keys = Climb.get_keys() + ["Year", "Race"]

        csvwriter = csv.DictWriter(csvfile, fieldnames=keys)
        csvwriter.writeheader()
        for tour in list_of_tours:
            for climb in tour.climbs:
                writable_dict = climb.to_map()
                writable_dict.update({"Year": tour.year, "Race": tour.name})
                print(writable_dict.values())
                csvwriter.writerow(writable_dict)

    return True


def export_stages(list_of_tours) -> bool:

    # najprej naredimo mape v data/ 

    dir_path = os.path.join(f"{DATA_FOLDER}csv/")
    os.makedirs(dir_path, exist_ok=True)

    print(dir_path)

    with open(dir_path + "stages.csv", "w+", encoding="utf-8") as csvfile:

        keys = Stage.get_keys() + ["Year", "Race"]

        csvwriter = csv.DictWriter(csvfile, fieldnames=keys)
        csvwriter.writeheader()
        for tour in list_of_tours:
            for stage in tour.stages:
                writable_dict = stage.to_map()
                writable_dict.update({"Year": tour.year, "Race": tour.name})
                print(writable_dict.values())
                csvwriter.writerow(writable_dict)           

    return True     


