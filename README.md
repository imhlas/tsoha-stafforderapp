# StaffOrder App

Sovelluksen avulla työntekijät voivat tehdä henkilökuntatilauksia yrityksen tuotteista. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Tämänhetkiset ominaisuudet
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksessa yrityksen tuotteet ja niiden henkilökuntahinnat.

## Tulevat ominaisuudet
- Käyttäjä voi lisätä tuotteita omaan tilaukseensa sekä muokata tilaustaan tilausajan päättymiseen asti.
- Käyttäjä pystyy näkemään tilaston oman tilauksensa sisällöstä.
- Ylläpitäjä voi lisätä ja poistaa tuotteita sekä muuttaa tuotteiden henkilökuntahintoja.
- Ylläpitäjä pystyy näkemään yhteenvedon kaikista tilauksista joko työntekijäkohtaisesti tai tuotekohtaisesti.

## Sovelluksen testaaminen
Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:
```bash
DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>
```
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```
Määritä tietokannan skeema komennolla:
```bash
psql < schema.sql
```
Nyt voit käynnistää sovelluksen komennolla:
```bash
flask run
```
