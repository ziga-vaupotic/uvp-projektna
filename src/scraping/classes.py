### V tej datoteki se nahajaj glavni razred za analizo dirke

class Stage:
    """Razred za etape dirke Tour de France."""

    def __init__(self, stage_url):
        # inicializacija etape je podana samo z URL-jem, saj je unikaten.
        self.stage_url = stage_url


class TourDeFrance:
    """Razred za posamezen Tour de France."""

    def __init__(self, year, url):
        self.year = year
        self.url = url
        self.stages = [] # seznam vseh etap dirke

    def __repr__(self):
        return f"Tour de France {self.year} ({self.url})"

    def add_stage(self, stage_url):
        self.stages.append(Stage(stage_url))

