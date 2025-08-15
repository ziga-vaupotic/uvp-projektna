### V tej datoteki se nahajaj glavni razred za analizo dirke

DATA_FOLDER = "data/"
SAVE_HTMLS = True


class Stage:
    """Razred za etape dirke Tour de France."""

    def __init__(self, stage_url):
        """ inicializacija etape je podana samo z URL-jem, saj je unikaten."""

        self.stage_url = stage_url

    def set_data(self, date, distance, vertical_meters):
        """Nastavi splošne informacije o etapi."""

        self.date = date
        self.distance = distance
        self.vertical_meters = vertical_meters


class Cyclist:

    def  __init__(self, id):
        self.id = id
        pass


class TourDeFrance:
    """Razred za posamezen Tour de France."""

    def __init__(self, year, url):
        self.year = year
        self.url = url
        self.stages = [] # seznam vseh etap dirke
        self.gcs = []

    def __repr__(self):
        return f"Tour de France {self.year} ({self.url})"

    def add_stage(self, stage_url):
        self.stages.append(Stage(stage_url))

    def add_gcs(self, gc: tuple[str, str]):

        if not isinstance(gc, tuple):
            raise TypeError("Expected tuple")

        self.gcs.append(gc)

    #def save_to_csv(self):



