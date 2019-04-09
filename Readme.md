# Printer-next

## Requirements

- python 3.5+
- pip, pipenv
- npm

## Development
1. Install dependencies from the pipfile

2. Install node dependecies

```` npm install````

3. Setup environmental variables

```` cp example.env .env````

```` source .env ````

4. Migrate and run server

```` python3 -Wall manage.py migrate ````

```` python3 -Wall manage.py runserver ````

## REST API
### Active printers
* Url: `/api/v1/active-printers`
* Supported methods: `GET`

Returns a list of user objects. Each user object contains the user's name, room number, and a list of active printers belonging to that user. Each printer object contains the printer's id, name, status (boolean), type (BW/CL, black and white/color), and a comment, if there is one.

### User's printers
This endpoint requires authentication in the form of an `Authorization` header that contains the string `Token` followed by the user's token, which can be obtained from the profile page. For example:

`Authorization: Token b89262e9d7a4c98fff9baed4c5fca2a660ae2a19   `

Only printers owned by the user whose token is in this header are accessible.

* Url: `/api/v1/my-printers`
* Supported methods: `GET`, `POST`


* Url: `/api/v1/my-printers/:id`
* Supported methods: `GET`, `PUT`, `PATCH`, `DELETE`
