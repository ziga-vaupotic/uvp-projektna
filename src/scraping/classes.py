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


    def __init__(self, stage_url):
        """ Inicializacija etape je podana samo z URL-jem, saj je unikaten."""

        self.stage_url = stage_url
        self.set_data()

    def set_data(self, date = -1, distance = -1, average_speed = -1, 
                 profile_score = -1, vertical_meters = -1, stage_type = -1):
        """Nastavi splošne informacije o etapi."""

        self.date = date
        self.distance = distance
        self.average_speed = average_speed
        self.profile_score = profile_score
        self.vertical_meters = vertical_meters
        self.stage_type = stage_type

    def to_map(self):
        return {"Date": self.date, "Distance": self.distance, 
                "Average Speed": self.average_speed, "Vertical": self.vertical_meters,
                "Profile score": self.profile_score, "Stage type": self.stage_type}
    
    @staticmethod
    def get_keys():
        return ["Date", "Distance", "Average Speed", "Vertical", "Profile score", "Stage type"]
    


class Climb:
    """Razred za vzpon."""

    def __init__(self, id, name, length, steepness, top, finish):

        self.id = id
        self.name = name
        self.length = length
        self.steepness = steepness
        self.top = top
        self.finish = finish

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

    def __init__(self, year, url, name):
        self.year = year
        self.url = url
        self.stages = [] # seznam vseh etap dirke
        self.gcs = []
        self.climbs = []
        self.name = name
        self.type = ""
        
    def __repr__(self):
        return f"Dirka {self.type} {self.year} ({self.url})"

    def add_stage(self, stage_url) -> None:
        self.stages.append(Stage(stage_url))

    def add_gcs(self, gc: tuple[str, str]) -> None:

        if not isinstance(gc, tuple):
            raise TypeError("Expected tuple")

        self.gcs.append(gc)

    #def save_to_csv(self):



