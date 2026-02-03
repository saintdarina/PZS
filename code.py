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

'''
Předzpracování signálu. 

1. Odstranení DC složky
Pokud signál nemá nenulový průměr, potřebujeme ho odečíst, aby nerušil další zpracování signálu.

2. Normalizace amplitudy
Normalizace zajišťuje srovnatelnost záznamů mezi subjekty. Normalizace na maximální amplitudu, RMS nebo jednotkovou energii.

3. Výběr stabilní části signálu 
Vynechat první a poslední část. Vybrat si střed signálu.

4. Okenování
Vynásobení signálu oknem, abychom snižili spektrální únik při frekvenční analýze.

5. Filtrace
High-pass filtr, případně band-pass, ale filtrace musí být jemná, aby se nezničí patologické znaky.

6. Sjednocení delky signálu.

'''

'''
Příznaky
Časová oblast -> stabilita a energie hlasu
Frekvenční oblast -> rozložení spektra a šum

Patologický hlas typicky: je méně stabilní, má rozmazané spektrum, vyšší šumovou složku a narušenou periodicitu.

Časová oblast:
1. RMS hodnota - efektivní hodnota signálu. Patologické hlasy často kolísají a mají nižší efektivní energii.
2. Variance / směrodatná odchylka. Nestabilní hlas má větší kolísání.
3. Zero Crossing Rate. ZCR nepřímo popisuje míru šumovosti hlasu. Patologický hlas má víc náhodných složek.
4. Krátkodobá energie. Průměr a rozptyl energie. 


Frekvenční oblast (FFT):
5. Dominantní frekvence - frekvence s maximální energií. Patologie bude se lišit od základní frekvenci hlásu.
6. Spektrální centroid. Spektrální centroid vyjadřuje percepční jasnost hlasu.
7. Spektrální šířka (bandwidth). Patologický hlas má šírší spektrum, více vyšších harmonických + šum.
8. Poměr energie v pásmech. U patologického hlasu víc energie ve vyšších frekvencích.

Kepstrální příznak:
9. Maximální keprstální peak
Kepstrální analýza umožňuje oddělit obálku spektra od periodicity hlasového signálu. Patologický hlas má peak nízký / rozmazaný.


Výsledný vektor příznaků:
[RMS,
 variance,
 ZCR,
 dominant_freq,
 centroid,
 bandwidth,
 band_energy_ratio,
 cepstral_peak]
'''