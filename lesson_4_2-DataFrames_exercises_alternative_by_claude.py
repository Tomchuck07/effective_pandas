import pandas as pd
import numpy as np
from io import StringIO

# =============================================================================
# 🎯 JAK KORZYSTAĆ Z TEGO PLIKU:
# =============================================================================
# 1. Czytaj sekcję "TWOJE ZADANIE"
# 2. Spróbuj sam napisać kod
# 3. Uruchom kod i zobacz czy działa
# 4. Jak nie wychodzi - przejdź do sekcji "ROZWIĄZANIE"
# 5. Porównaj swoje rozwiązanie z moim
# 
# 💡 Klucz do nauki: NAJPIERW PRÓBUJ SAM, dopiero potem patrz na rozwiązanie!
# =============================================================================

# =============================================================================
# SCENARIUSZ 1: Łączenie wielu plików CSV
# =============================================================================
# 📖 KONTEKST: 
# Pracujesz w dziale sprzedaży. Każdy miesiąc dostajesz nowy plik CSV 
# z transakcjami. Na koniec kwartału musisz połączyć wszystkie pliki w jeden.

print("="*80)
print("SCENARIUSZ 1: Łączenie wielu plików (concat)")
print("="*80)

# DANE DO PRACY (nie zmieniaj tego!)
sprzedaz_styczen = """data,produkt,wartosc,region
2024-01-05,Laptop,3500,Północ
2024-01-12,Telefon,1200,Południe
2024-01-20,Tablet,800,Wschód"""

sprzedaz_luty = """data,produkt,wartosc,region
2024-02-03,Laptop,3200,Południe
2024-02-15,Monitor,450,Północ
2024-02-28,Telefon,1100,Zachód"""

sprzedaz_marzec = """data,produkt,wartosc,region
2024-03-10,Tablet,850,Wschód
2024-03-18,Laptop,3600,Północ
2024-03-25,Monitor,500,Południe"""

# --- TWOJE ZADANIE ---
print("\n🎯 TWOJE ZADANIE:")
print("1. Wczytaj każdy plik do osobnego DataFrame (użyj pd.read_csv i StringIO)")
print("2. Połącz wszystkie 3 DataFrame'y w jeden (użyj pd.concat)")
print("3. Wyświetl: ile wierszy ma każdy DataFrame i ile ma połączony")
print("4. BONUS: Zamień kolumnę 'data' na datetime i policz sumę wartości dla każdego produktu")

# TWÓJ KOD TUTAJ (zacznij pisać poniżej):
df_jan = pd.read_csv(StringIO(sprzedaz_styczen), dtype_backend='pyarrow')
df_feb = pd.read_csv(StringIO(sprzedaz_luty), dtype_backend='pyarrow')
df_mar = pd.read_csv(StringIO(sprzedaz_marzec), dtype_backend='pyarrow')

df_q1=pd.concat([df_jan, df_feb, df_mar], ignore_index=True)
df_q1
len(df_q1)
df_q1["data"] = pd.to_datetime(df_q1['data'])
df_q1.dtypes

df_q1.groupby('produkt')['wartosc'].sum()






# -------------------------------------------------
# 💡 WSKAZÓWKA (jak utkniesz):
# - pd.read_csv(StringIO(text)) - wczytuje string jako CSV
# - pd.concat([df1, df2, df3], ignore_index=True) - łączy pionowo
# - pd.to_datetime(df['kolumna']) - zamienia na daty
# - df.groupby('kolumna')['inna'].sum() - sumuje według grup
# -------------------------------------------------

print("\n" + "="*80)
print("✅ ROZWIĄZANIE SCENARIUSZ 1:")
print("="*80)

# Wczytaj pliki
df_jan = pd.read_csv(StringIO(sprzedaz_styczen))
df_feb = pd.read_csv(StringIO(sprzedaz_luty))
df_mar = pd.read_csv(StringIO(sprzedaz_marzec))

print(f"Styczeń: {len(df_jan)} wierszy")
print(f"Luty: {len(df_feb)} wierszy")
print(f"Marzec: {len(df_mar)} wierszy")

# Połącz wszystkie
df_q1 = pd.concat([df_jan, df_feb, df_mar], ignore_index=True)
print(f"\nPo połączeniu: {len(df_q1)} wierszy")
print(df_q1)

# BONUS
df_q1['data'] = pd.to_datetime(df_q1['data'])
print("\n📊 Sprzedaż według produktu:")
print(df_q1.groupby('produkt')['wartosc'].sum().sort_values(ascending=False))

input("\n⏸️  Naciśnij ENTER aby przejść do następnego scenariusza...")

# =============================================================================
# SCENARIUSZ 2: Łączenie tabel (merge/join)
# =============================================================================
# 📖 KONTEKST:
# Masz tabelę zamówień (z ID produktu) i osobną tabelę z katalogiem produktów.
# Chcesz zobaczyć nazwy produktów w zamówieniach (jak JOIN w SQL).

print("\n" + "="*80)
print("SCENARIUSZ 2: Łączenie tabel (merge/join)")
print("="*80)

# DANE DO PRACY
zamowienia = """id_zamowienia,id_produktu,ilosc,data
ORD001,P101,2,2024-01-15
ORD002,P102,1,2024-01-16
ORD003,P103,5,2024-01-17
ORD004,P101,3,2024-01-18
ORD005,P104,1,2024-01-19"""

produkty = """id_produktu,nazwa,kategoria,cena
P101,Klawiatura,Peryferia,150
P102,Mysz,Peryferia,80
P103,Kabel USB,Akcesoria,15
P104,Słuchawki,Audio,250"""

df_orders = pd.read_csv(StringIO(zamowienia))
df_products = pd.read_csv(StringIO(produkty))

print("\nTabela zamówień:")
print(df_orders)
print("\nKatalog produktów:")
print(df_products)

# --- TWOJE ZADANIE ---
print("\n🎯 TWOJE ZADANIE:")
print("1. Połącz df_orders z df_products używając kolumny 'id_produktu'")
print("2. Stwórz nową kolumnę 'wartosc' = ilosc * cena")
print("3. Wyświetl: id_zamowienia, nazwa, ilosc, cena, wartosc")

# TWÓJ KOD TUTAJ:

def dodaj_nazwe(df_):
        a = []
        for i in df_.id_produktu:
                # print(i ,'\n')
                l=0
                for j in df_products.id_produktu:
                    #   print(j ,'\n')
                      if i==j: a.append(df_products.nazwa.iloc[l])
                      l+=1
        return a

dodaj_nazwe(df_orders)

 df_complete = (df_orders
                .assign(
                 nazwa = lambda df_: dodaj_nazwe(df_)
                )
 )









# -------------------------------------------------
# 💡 WSKAZÓWKA:
# - df1.merge(df2, on='wspólna_kolumna', how='left') - łączy jak SQL JOIN
# - df['nowa'] = df['col1'] * df['col2'] - tworzy nową kolumnę
# - df[['col1', 'col2', 'col3']] - wybiera konkretne kolumny
# -------------------------------------------------

print("\n" + "="*80)
print("✅ ROZWIĄZANIE SCENARIUSZ 2:")
print("="*80)

df_complete = df_orders.merge(df_products, on='id_produktu', how='left')
df_complete['wartosc'] = df_complete['ilosc'] * df_complete['cena']

print("\nPołączone dane:")
print(df_complete[['id_zamowienia', 'nazwa', 'ilosc', 'cena', 'wartosc']])

input("\n⏸️  Naciśnij ENTER aby przejść do następnego scenariusza...")

# =============================================================================
# SCENARIUSZ 3: CSV z różnymi separatorami
# =============================================================================
# 📖 KONTEKST:
# Kolega z księgowości wysłał Ci plik wyeksportowany z Excela.
# Ma średniki zamiast przecinków (typowe w Polsce/Europie).

print("\n" + "="*80)
print("SCENARIUSZ 3: Import CSV z średnikami")
print("="*80)

dane_pl = """imie;nazwisko;miasto;pensja
Jan;Kowalski;Kraków;5500
Anna;Nowak;Warszawa;6200
Piotr;Wiśniewski;Gdańsk;5800"""

print("PLIK CSV (zwróć uwagę na średniki!):")
print(dane_pl)

# --- TWOJE ZADANIE ---
print("\n🎯 TWOJE ZADANIE:")
print("1. Wczytaj ten plik CSV (pamietaj o separatorze!)")
print("2. Oblicz średnią pensję")
print("3. Wyświetl pracowników posortowanych po pensji (od najwyższej)")

# TWÓJ KOD TUTAJ:
# df_pracownicy = ...









# -------------------------------------------------
# 💡 WSKAZÓWKA:
# - pd.read_csv(StringIO(text), sep=';') - dla średników
# - df['kolumna'].mean() - średnia
# - df.sort_values('kolumna', ascending=False) - sortowanie malejąco
# -------------------------------------------------

print("\n" + "="*80)
print("✅ ROZWIĄZANIE SCENARIUSZ 3:")
print("="*80)

df_pracownicy = pd.read_csv(StringIO(dane_pl), sep=';')
print(df_pracownicy)
print(f"\nŚrednia pensja: {df_pracownicy['pensja'].mean():.0f} PLN")
print("\nPosortowani po pensji:")
print(df_pracownicy.sort_values('pensja', ascending=False))

input("\n⏸️  Naciśnij ENTER aby przejść do następnego scenariusza...")

# =============================================================================
# SCENARIUSZ 4: Pivot Table (long → wide)
# =============================================================================
# 📖 KONTEKST:
# Dane z bazy są w formacie "długim" (każdy wiersz to jedna obserwacja).
# Szef chce tabelę przestawną: regiony w wierszach, produkty w kolumnach.

print("\n" + "="*80)
print("SCENARIUSZ 4: Pivot Table")
print("="*80)

sprzedaz_long = """data,region,produkt,wartosc
2024-01,Północ,Laptop,10500
2024-01,Północ,Telefon,3600
2024-01,Południe,Laptop,8400
2024-01,Południe,Telefon,4800
2024-02,Północ,Laptop,12000
2024-02,Północ,Telefon,4200
2024-02,Południe,Laptop,9000
2024-02,Południe,Telefon,5400"""

df_long = pd.read_csv(StringIO(sprzedaz_long))

print("DANE (format LONG - każdy wiersz = jedna obserwacja):")
print(df_long)

# --- TWOJE ZADANIE ---
print("\n🎯 TWOJE ZADANIE:")
print("Stwórz pivot table gdzie:")
print("- Wiersze (index) = region")
print("- Kolumny (columns) = produkt")
print("- Wartości (values) = suma wartości")

# TWÓJ KOD TUTAJ:
# df_pivot = ...









# -------------------------------------------------
# 💡 WSKAZÓWKA:
# - df.pivot_table(values='co_liczymy', index='wiersze', columns='kolumny', aggfunc='sum')
# - Alternatywa: df.groupby(['A', 'B'])['C'].sum().unstack()
# -------------------------------------------------

print("\n" + "="*80)
print("✅ ROZWIĄZANIE SCENARIUSZ 4:")
print("="*80)

df_pivot = df_long.pivot_table(
    values='wartosc',
    index='region',
    columns='produkt',
    aggfunc='sum'
)
print("PIVOT TABLE (format WIDE - łatwiejszy do czytania):")
print(df_pivot)

input("\n⏸️  Naciśnij ENTER aby przejść do następnego scenariusza...")

# =============================================================================
# SCENARIUSZ 5: Melt (wide → long)
# =============================================================================
# 📖 KONTEKST:
# Dostałeś Excel z miesiącami jako kolumnami. Potrzebujesz formatu long
# do zrobienia wykresów i analiz.

print("\n" + "="*80)
print("SCENARIUSZ 5: Melt (odwrotność pivot)")
print("="*80)

dane_wide = """produkt,styczen,luty,marzec
Laptop,10500,12000,11500
Telefon,3600,4200,3900
Tablet,2400,2800,2600"""

df_wide = pd.read_csv(StringIO(dane_wide))

print("DANE (format WIDE - z Excela):")
print(df_wide)

# --- TWOJE ZADANIE ---
print("\n🎯 TWOJE ZADANIE:")
print("Przekształć tabelę do formatu LONG gdzie będziesz miał:")
print("- kolumna 'produkt' (zostaje)")
print("- kolumna 'miesiac' (nowa - z nazw kolumn)")
print("- kolumna 'sprzedaz' (nowa - z wartości)")

# TWÓJ KOD TUTAJ:
# df_melted = ...









# -------------------------------------------------
# 💡 WSKAZÓWKA:
# - df.melt(id_vars=['co_zostaje'], var_name='nazwa_dla_kolumn', value_name='nazwa_dla_wartości')
# -------------------------------------------------

print("\n" + "="*80)
print("✅ ROZWIĄZANIE SCENARIUSZ 5:")
print("="*80)

df_melted = df_wide.melt(
    id_vars=['produkt'],
    var_name='miesiac',
    value_name='sprzedaz'
)
print("Po MELT (format LONG):")
print(df_melted)

print("\nTeraz łatwo policzyć średnią:")
print(df_melted.groupby('produkt')['sprzedaz'].mean())

input("\n⏸️  Naciśnij ENTER aby przejść do FINAŁOWEGO wyzwania...")

# =============================================================================
# SCENARIUSZ 6: FINAŁOWE WYZWANIE - Wszystko razem!
# =============================================================================
# 📖 KONTEKST:
# Musisz stworzyć raport sprzedażowy łącząc dane z 3 systemów:
# - Transakcje (z bazy danych)
# - Klienci (z CRM)
# - Produkty (z ERP)

print("\n" + "="*80)
print("SCENARIUSZ 6: 🏆 FINAŁOWE WYZWANIE")
print("="*80)

transakcje = """transaction_id,customer_id,product_id,quantity,date
T001,C101,P201,2,2024-03-01
T002,C102,P202,1,2024-03-02
T003,C101,P203,3,2024-03-03
T004,C103,P201,1,2024-03-04"""

klienci = """customer_id,name,segment,city
C101,Jan Kowalski,Premium,Warszawa
C102,Anna Nowak,Standard,Kraków
C103,Piotr Zieliński,Premium,Gdańsk"""

produkty_erp = """product_id,product_name,category,unit_price
P201,Laptop Dell,Komputery,3500
P202,Monitor Samsung,Monitory,800
P203,Mysz Logitech,Akcesoria,120"""

df_trans = pd.read_csv(StringIO(transakcje))
df_cust = pd.read_csv(StringIO(klienci))
df_prod = pd.read_csv(StringIO(produkty_erp))

print("MASZ 3 TABELE:")
print("\n1. Transakcje:")
print(df_trans)
print("\n2. Klienci:")
print(df_cust)
print("\n3. Produkty:")
print(df_prod)

# --- TWOJE ZADANIE ---
print("\n🎯 TWOJE FINAŁOWE ZADANIE:")
print("1. Połącz wszystkie 3 tabele (najpierw transakcje+klienci, potem +produkty)")
print("2. Dodaj kolumnę 'total_value' = quantity * unit_price")
print("3. Zamień 'date' na datetime")
print("4. Wyświetl raport z kolumnami: transaction_id, name, product_name, total_value")
print("5. Policz całkowitą wartość sprzedaży")
print("6. Pokaż wartość według segmentu klienta")

# TWÓJ KOD TUTAJ - spróbuj sam połączyć wszystko!
# df_raport = ...









# -------------------------------------------------
# 💡 WSKAZÓWKI:
# - Merge możesz łączyć w łańcuch: df1.merge(df2).merge(df3)
# - .assign() pozwala dodać wiele kolumn naraz
# - lambda x: ... w assign pozwala używać innych kolumn
# -------------------------------------------------

print("\n" + "="*80)
print("✅ ROZWIĄZANIE SCENARIUSZ 6:")
print("="*80)

df_raport = (df_trans
    .merge(df_cust, on='customer_id', how='left')
    .merge(df_prod, on='product_id', how='left')
    .assign(
        total_value=lambda x: x['quantity'] * x['unit_price'],
        date=lambda x: pd.to_datetime(x['date'])
    )
)

print("FINALNY RAPORT:")
print(df_raport[['transaction_id', 'name', 'product_name', 'total_value']])

print("\n📊 ANALIZA:")
print(f"Całkowita wartość: {df_raport['total_value'].sum():,.0f} PLN")
print(f"\nWartość według segmentu:")
print(df_raport.groupby('segment')['total_value'].sum())

# =============================================================================
# 🎓 PODSUMOWANIE - Co się nauczyłeś
# =============================================================================

print("\n" + "="*80)
print("🎓 GRATULACJE! Przeszedłeś wszystkie scenariusze!")
print("="*80)
print("""
Nauczyłeś się 6 najważniejszych technik pracy z danymi:

✅ 1. pd.concat() - łączenie wielu plików pionowo
✅ 2. .merge() - łączenie tabel jak JOIN w SQL
✅ 3. pd.read_csv(sep=';') - różne formaty importu
✅ 4. .pivot_table() - przekształcenie long → wide
✅ 5. .melt() - przekształcenie wide → long
✅ 6. Pipeline merge+assign - kompletny raport z wielu źródeł

💡 Te 6 technik to 80% codziennej pracy z danymi!

🚀 NASTĘPNE KROKI:
- Przećwicz każdy scenariusz 2-3 razy
- Spróbuj na swoich własnych danych
- Eksperymentuj z parametrami (how='inner', aggfunc='mean', etc.)
""")