'''
Druhá seminární práce.

Postup:

Máme hlasové signály pacientů a jejich diagnozy.

Naším úkolem je:

1. načíst signál
2. získat z něj vhodné příznaky
3. podle nich signály automaticky rozdělit
4. porovnat výsledek s realitou (anotacemi)

Načtení dat bude probíhat pomocí WFDB. Výstupem bude pole vzorků signálu, vzorkovácí frekvence, diagnoza / třída.

Předzpracování signálu. Odstranění DC složky, normalizace amplitudy, případně okenování.

Ektrakce příznaků. 
Časová oblast: RMS hodnota, energie signálu, variance, zero-crossing fate, jitter.
Frekvenční oblast: FFT spektrum, spektrální centroid, šířka pasma, dominantní frekvence, poměr energie v pásmech.
Kepstrální analýza: log(FFT), IFFT -> kepstrum, hledaní periodicity. 

Klasifikace.
Prahování, vzdálenost středu třídy, k-means, jednoduchý kNN, PCA -> vizualizace, oddělení: normální x patologický,
typy patologií.

Vyhodnocení úspěšnosti. Porovnání našeho výsledku a anotací jako tabulka.

Grafické výstupy: signál v čase, FFT spektrum, kepstrum, PCA scatter plot, rozhodovací hranice.
'''

