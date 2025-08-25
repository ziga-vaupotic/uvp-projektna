from src.scraping import find_race, find_climbs, find_stages, find_stage_data, export


races = []

for race in ["giro-d-italia", "vuelta-a-espana", "tour-de-france"]:
    for i in range(2000, 2026):
        current = find_race(i, race)
        current.climbs = find_climbs(current)

        for stage in find_stages(current):

            stage_data = find_stage_data(stage, current)
            print(stage_data)
            if stage_data != []:
                stage.set_data(stage_data[0], stage_data[2], stage_data[1], 
                            stage_data[4], stage_data[5], stage_data[3])  
            
            current.add_stage(stage)

        races.append(current)


export.export_climbs(races)
export.export_stages(races)

