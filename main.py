import src.scraping as scraping

def main():    # Scrape data for the Tour de France from 2015 to 2024
    a = scraping.scraper.general_information_tdf([2015, 2024], True)

    print(a)
    #scraper.stages_tdf([2015, 2024])
