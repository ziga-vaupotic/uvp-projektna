from scraping import scraper


def main():    # Scrape data for the Tour de France from 2015 to 2024
    scraper.general_information_tdf([2015, 2024], True)

    #scraper.stages_tdf([2015, 2024])
