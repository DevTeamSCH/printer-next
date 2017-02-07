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
