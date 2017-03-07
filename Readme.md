# Printer-next

## Követelmények

- python 3.5
- pip
- npm

## Fejlesztés
```` pip -r requirements/development.txt ````
> Érdemes virtualenv-et használni

```` npm install````

```` cp example.env .env````

> Ki kell tölteni a környezeti változokat.

```` source .env ````

```` python3 -Wall manage.py migrate ````

```` python3 -Wall manage.py runserver ````

## REST API
Az api csak azonosítással használható. A profil oldalon generálható auth-tokent el kell küldeni minden kérés fejlécében, például:

````Authorization: Token b89262e9d7a4c98fff9baed4c5fca2a660ae2a19````

A felhasználó összes nyomtatója lekérhető a ``/api/my-printers/`` címen. A formátuma:

````
[
    {
        "id": 1,
        "name": "nev1",
        "status": false
    },
    {
        "id": 2,
        "name": "nev2",
        "status": true
    }
]
````

A nyomtató státusza módosítható a ``/api/my-printers/<id>/`` címen. A címre küldött GET kérésre csak a megadott id-jű nyomtató adatait adja vissza. PUT kéréssel a status mező értékét meg lehet adni. Erre a címre küldött kérésekre 404-es hibakódú válasz jön, ha hibás id van megadva és 403, ha a megadott id-jű nyomtató más felhasználóé.