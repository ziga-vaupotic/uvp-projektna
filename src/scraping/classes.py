### V tej datoteki se nahajaj glavni razred za analizo dirke
from enum import Enum


DATA_FOLDER = "data/"
SAVE_HTMLS = True
URL = "https://www.procyclingstats.com/"


## Vzeto iz https://www.procyclingstats.com/info/profile-score-explained

class StageType(Enum):
    RESTDAY = -1
    NONE = 0
    FLAT = 1
    HILLSFLATFINISH = 2
    HILLSUPHILLFINISH = 3
    MOUNTAINSFLATFINISH = 4
    MOUNTAINSUPHILLFINISH = 5



class Stage:
    """Razred za etape dirke Tour de France."""


    def __init__(self, stage_num, stage_url):
        """ Inicializacija etape je podana samo z URL-jem, saj je unikaten."""

        self.stage_num = stage_num
        self.stage_url = stage_url
        self.set_data()

    def __str__(self):
        return str(self.to_map)

    def set_data(self, date: str = -1, distance: int = -1, average_speed: int = -1, 
                 profile_score: int = -1, vertical_meters: int = -1, stage_type: int = -1):
        """Nastavi splošne informacije o etapi."""

        self.date = date
        self.distance = distance
        self.average_speed = average_speed
        self.profile_score = profile_score
        self.vertical_meters = vertical_meters
        self.stage_type = stage_type

    def to_map(self):
        # Vrne 
        return {"Number": self.stage_num, "Date": self.date, "Distance": self.distance, 
                "Average Speed": self.average_speed, "Vertical": self.vertical_meters,
                "Profile score": self.profile_score, "Stage type": self.stage_type}
    
    @staticmethod
    def get_keys():
        return ["Number", "Date", "Distance", "Average Speed", "Vertical", "Profile score", "Stage type"]
    


class Climb:
    """Razred za vzpon."""

    def __init__(self, id: str, name: str, length: int,
                  steepness: int, top: int, finish: int):

        self.id = id
        self.name = name
        self.length = length
        self.steepness = steepness
        self.top = top
        self.finish = finish

    def __str__(self):
        return str(self.to_map())

    def to_map(self):
        return {"Name": self.name, "Length": self.length, 
                "Steepness": self.steepness, "Vertical": self.top}
    
    @staticmethod
    def get_keys():
        return ["Name", "Length", "Steepness", "Vertical"]



class Cyclist:
    """ Razred za kolesarja. """
    def  __init__(self, id):
        self.id = id
        pass


class Race:
    """Razred za posamezeno Dirko."""

    def __init__(self, year: int, url: str, name: str):
        self.year = year
        self.url = url
        self.stages = [] # seznam vseh etap dirke
        self.climbs = []
        self.name = name
        self.type = ""
        
    def __repr__(self):
        return f"Dirka {self.type} {self.year} ({self.url})"

    def add_stage(self, stage: Stage) -> None:
        self.stages.append(stage)




