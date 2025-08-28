""" V tej datoteki se nahaja glavna koda za pridobivanje podatkov,
ki so uporabljeni za analizo."""

from src.scraping import find_race, find_climbs, find_stages, find_stage_data, find_leaderboard_types,find_leaderboard_stage, export


if __name__ == "__main__":
    races = []

    for race in ["giro-d-italia", "vuelta-a-espana", "tour-de-france"]:
        for i in range(1906, 2026):
            current = find_race(i, race)
            current.climbs = find_climbs(current)

            for stage in find_stages(current):

                stage_data = find_stage_data(stage, current)
                if stage_data != []:
                    stage.set_data(stage_data[0], stage_data[2], stage_data[1], 
                                stage_data[4], stage_data[5], stage_data[3])  
                
                # Primer uporabe drugih funkcij
                #for x in find_leaderboard_types(stage):
                #    print(str(x))
                #    print(find_leaderboard_stage(stage, x.data_id))

                current.add_stage(stage)

            races.append(current)


    export.export_climbs(races)
    export.export_stages(races)

