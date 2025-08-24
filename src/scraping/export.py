import classes
import os
import json
import csv

def export_climbs(list_of_tours, type):

    # splošne informacije o tour de francu sprava zapišemo v json.

    dir_path = os.path.join(f"{classes.DATA_FOLDER}csv/")
    os.makedirs(dir_path, exist_ok=True)

    print(dir_path)

    with open(dir_path + "climbs.csv", "w+", encoding="utf-8") as csvfile:

        keys = classes.Climb.get_keys() + ["Year", "Race"]

        csvwriter = csv.DictWriter(csvfile, fieldnames=keys)
        csvwriter.writeheader()
        for tour in list_of_tours:
            for climb in tour.climbs:
                writable_dict = climb.to_map()
                writable_dict.update({"Year": tour.year, "Race": tour.name})
                print(writable_dict.values())
                csvwriter.writerow(writable_dict)


def export_stages(list_of_tours, type):

    # splošne informacije o tour de francu sprava zapišemo v json.

    dir_path = os.path.join(f"{classes.DATA_FOLDER}csv/")
    os.makedirs(dir_path, exist_ok=True)

    print(dir_path)

    with open(dir_path + "stages.csv", "w+", encoding="utf-8") as csvfile:

        keys = classes.Stage.get_keys() + ["Year", "Race"]

        csvwriter = csv.DictWriter(csvfile, fieldnames=keys)
        csvwriter.writeheader()
        for tour in list_of_tours:
            for stage in tour.stages:
                writable_dict = stage.to_map()
                writable_dict.update({"Year": tour.year, "Race": tour.name})
                print(writable_dict.values())
                csvwriter.writerow(writable_dict)                


