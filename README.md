# User Authentication App

## Features
- User Registration: Creates new user account and check the uniqueness of username.
- User Login: Verifies user by username and password, tracks login session.
- Password Security: Password hashing and verification using Werkzeug.
- User Logout: Ends the user session safely.
- Form Validation: Manages form data using WTForms and Flask-WTF.
- Test: Unit test and integration test using Pytest


## Quick Start
1. Create an environment with Python 3.10
2. Install all dependencies
```
pip install -r requirements.txt
```
3. Run the app by
```
python app.py
```
4. (Optional) Run test by
```
pytest
```

## API Endpoints
| HTTP Verb | Endpoint | Action |
| --- | --- | --- |
| `GET` | `/register` | Displays the user registration page. |
| `POST` | `/register` | Handles user registration submission. |
| `GET` | `/login` | Displays the user login page. |
| `POST` | `/login` | Handles user login submission. |
| `GET` | `/dashboard` | Displays the user's personal dashboard. |
| `GET` | `/logout` | Clears login status, and redirects to the login page. |

## Tech Stacks
- Backend Framework: Flask
- ORM: Flask-SQLAlchemy
- Form Validation: WTForms, Flask-WTF
- Frontend: HTML
- Test: Pytest


## Reference
- Flask-WTF: https://hackmd.io/@shaoeChen/ByofdR1XG
- Flask-SQLAlchemy: https://github.com/pallets-eco/flask-sqlalchemy
- Werkzeug: https://reurl.cc/MzRv7n
- Pytest on Flask: https://hackmd.io/@payon/S1OixvoN2

