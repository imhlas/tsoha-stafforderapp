# StaffOrder App

Sovelluksen avulla työntekijät voivat tehdä henkilökuntatilauksia yrityksen tuotteista. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Tämänhetkiset ominaisuudet
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksessa yrityksen tuotteet ja niiden henkilökuntahinnat.
- Käyttäjä voi lisätä tuotteita omaan tilaukseensa.
- Käyttäjä näkee listauksen tilauksensa sisällöstä ja voi lisätä/poistaa tuotteita tilausajan päättymiseen asti.
- Ylläpitäjä näkee listauksen kaikista tuotteista sekä niiden hinnoista.
- Ylläpitäjä voi lisätä uusia tuotteita.

## Tulevat ominaisuudet
- Ylläpitäjä voi poistaa tuotteita sekä muuttaa tuotteiden henkilökuntahintoja.
- Ylläpitäjä voi sulkea tilausajan, jonka jälkeen tilauksia ei pysty enää muuttamaan.
- Ylläpitäjä näkee yhteenvedon tehdyista tilauksista tilausajan sulkeuduttua.

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
Sovelluksen kautta pystyy rekisteröimään vain tavallisia käyttäjiä, joten lisää admin-ominaisuuksien testaamista varten tunnus tietokantaan:
```bash
$ psql
user=# INSERT INTO users (name, password, role) VALUES ('admin', 'admin123', 1);
```

Nyt voit käynnistää sovelluksen komennolla:
```bash
flask run
```
