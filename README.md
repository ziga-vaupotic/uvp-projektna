# Analiza etap na trotedenskih kolesarskih dirkah


## Viri podatkov

Vsi podatki so bili pridobljeni iz spletne strani [Procyclingstats](https://www.procyclingstats.com/index.php).

## Navodila za uporabo

Za uporabo projekta so potrebne naslednje knjižnice:

- requests
- matplotlib
- pandas
- scipy.

Vse potrebne knjižnice lahko namestimo z uporabo z pip:

```unix
pip install requirements.txt
 ```

Za zagon primera, ki je uporabljen v analizi, preprosto zaženemo:

```unix
python3 main.py
 ```

## Funkcionalnost

Poberalnik podatkov temelji na podatkih iz strani Procyclingstats. Trenutno omogoča izluščenje sledečih podatkov:

- Podatki o dirki
- Podatki o vzponih
- Podatki o etapeh na posamezni dirki
- Končna razverstitev etape

Primer uporabe:
```python
>>> from scraping import scraper_main
>>> giro = scraper_main.general_race_information(2025, "giro-d-italia")
>>> climbs = scraper_main.find_climbs(giro)
>>> print(climbs[0])
>>> {'Name': 'Monte Grappa', 'Length': '25.1', 'Steepness': '5.7', 'Vertical': '1605'}
 ```

Poberalnik je bil preverjen le na tritedenskih dirkah, vendar bi moral delati na vseh dirkah s podobno strukturo.