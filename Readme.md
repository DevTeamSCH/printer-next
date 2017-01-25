# Printer-next

## Követelmények

- python 3.5
- pip
- npm

## Fejlesztés
```` pip -r requirements/development.txt ````
> Érdemes virtualenv-et használni

```` npm install````

> Mivel a UIKit3 még beta ezért kézzel kell lefordítani npm install után node_modules mappában lévő uikit mappa Readme-je alapján.

```` cp example.env .env````

> Ki kell tölteni a környezeti változokat.

```` source .env ````

```` python3 -Wall manage.py migrate ````

```` python3 -Wall manage.py runserver ````
