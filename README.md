# StaffOrder App

Sovelluksen avulla työntekijät voivat tehdä henkilökuntatilauksia yrityksen tuotteista. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Sovelluksen ominaisuudet peruskäyttäjälle
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee sovelluksen etusivulla yrityksen brändit. Brändiä klikkaamalla pääsee tarkastelemaan brändikohtaista tuotevalikoimaa.
- Käyttäjä näkee brändikohtaisilla sivuilla  yrityksen tuotteet ja niiden henkilökuntahinnat.
- Käyttäjä voi lisätä tuotteita omaan tilaukseensa.
- Käyttäjä näkee listauksen tilauksensa sisällöstä ja voi lisätä/poistaa tuotteita tilausajan päättymiseen asti.

## Sovelluksen ominaisuudet ylläpitäjälle
- Ylläpitäjä voi lisätä uusia brändejä.
- Ylläpitäjä voi lisätä uusia tuotteita.
- Ylläpitäjä näkee listauksen kaikista tuotteista sekä niiden hinnoista.
- Ylläpitäjä voi poistaa tuotteita sekä muuttaa tuotteiden henkilökuntahintoja.
- Ylläpitäjä voi sulkea tilausajan, jonka jälkeen tilauksia ei pysty enää muuttamaan.
- Ylläpitäjä näkee yhteenvedon tehdyista tilauksista käyttäjäkohtaisesti tilausajan sulkeuduttua.
- Ylläpitäjä voi siirtää yksittäisen käyttäjän tilauksen tilaan 'Laskutettu', jolloin tilaus poistuu tehtyjen tilausten listalta

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
Sovellusta testatessa kannattaa ensin kirjautua admin-tunnuksilla ja lisätä sovellukseen brändejä ja tuotteita. Repositorion 'logot' kansio sisältää esimerkkikuvia logoista, joita voi hyödyntää brändikuvina.
