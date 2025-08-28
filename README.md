# Analiza etap na tritedenskih kolesarskih dirkah
 Ta projekt je narejen v sklopu projektne naloge za predmet uvod v programiranje (UVP). Ukvarjal sem se z analizo tritedenskih kolesarskih dirk. Podatke, uporabljene v analizi, sem pridobil iz spletne strani [Procyclingstats](https://www.procyclingstats.com/index.php). V ``src/scraping/`` se nahaja izvirna koda za pridobivanje podatkov. Vsa funkcionalnost napisne kode je opisana spodaj.

 Analiza podatkov je narejena v jupyter zvezeku (``analysis/analiza-dirk.ipynb``). Vključuje analizo časovnih trendov dirke po Franciji, dirke po Italiji in dirke po Španiji. To so recimo povprečna hitrost, dolžina etap, premagana nadmorska višina, ... Poudarek je na primerjavi vseh treh dirk. Posledično analiziramo tudi vzpone, ki se pojavijo na dirkah.


## Navodila za uporabo

Za uporabo projekta so potrebne naslednje knjižnice:

- requests
- matplotlib
- pandas
- scipy.

Vse potrebne knjižnice lahko namestimo z uporabo pip:

```unix
pip install requirements.txt
 ```

Za zagon primera, ki je uporabljen v analizi, preprosto zaženemo:

```unix
python3 main.py
 ```

## Funkcionalnost

Zbiralnik podatkov temelji na podatkih iz strani Procyclingstats. Trenutno omogoča izluščenje sledečih podatkov:

- Podatki o dirki
- Podatki o vzponih
- Podatki o etapeh na posamezni dirki
- Končna razverstitev etape

Primer uporabe:
```python
>>> from scraping import find_race, find_climbs
>>> race = find_race(2025, "giro-d-italia")
>>> climbs = find_climbs(race)
>>> print(climbs[0])
>>> {'Name': 'Monte Grappa', 'Length': '25.1', 'Steepness': '5.7', 'Vertical': '1605'}
 ```

Zbiralnik je bil preverjen le na tritedenskih dirkah, vendar bi moral delati na vseh dirkah s podobno strukturo.