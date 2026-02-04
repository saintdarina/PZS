'''
První seminární prace
První uloha
Úloha má 4 hlavní části:

1. Seznámení se s daty a jejich načtení
2. Návrh vlastního algoritmu pro detekci R-vrcholů
3. Výpočet tepové frekvence
4. Ověření algoritmu na MIT-BIH databázi (validace)

Načtení dat z PhysioNetu

Předzpracování EKG signálu
odstranění DC složky (pro jistotu)
normalizace amplitudy (např. na ⟨-1, 1⟩)
zvýraznění R-vrcholů (derivace / absolutní hodnota)

Detekce R-vrcholů
Krok 1 - zvýraznění peaků
derivace signálu → R-vrchol má strmý náběh
absolutní hodnota
případně klouzavý průměr

Krok 2 - prahování
zvolíme adaptivní práh (např. procento maxima signálu)
odstraníme malé špičky (šum)

Krok 3 - detekce lokálních maxim
bod je R-vrchol, pokud je větší než sousedé, je nad prahem

Krok 4 - refrakterní perioda
dva R-vrcholy nemohou být blíž než např. 200-300 ms (fyziologický limit srdce)

Výpočet tepové frekvence (HR)
Varianta A - z celého signálu
HR = pocet R vrcholu/delka signalu v minutach 
Varianta B - z RR intervalů
spočítáme vzdálenosti mezi R-vrcholy, zprůměrujeme, HR = 60 / průměrný RR interval

Zobrazení výsledků
graf
schéma algoritmu
tabulka měření, počet R-vrcholů, HR

Testování na MIT-BIH databázi
'''