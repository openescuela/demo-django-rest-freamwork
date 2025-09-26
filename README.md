# Autocars Marketplace

A web application to buy and sell cars using **Django REST Framework** for the backend and **Django + Bootstrap** for the frontend.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- User registration and login using JWT authentication
- Seller accounts can add cars
- List of cars with details: make, model, year, price, description, image
- Frontend template using Bootstrap
- Only logged-in users can view cars
- REST API for frontend and external consumption
- CORS enabled for frontend-backend separation
- Image upload for car listings

---

## Tech Stack

- Backend: Django, Django REST Framework, PostgreSQL (or SQLite)
- Frontend: Django templates, Bootstrap 5
- Authentication: JWT (via `djangorestframework-simplejwt`)
- HTTP requests in frontend: Python `requests` library
- CORS handling: `django-cors-headers`

---

## Project Structure

autocars_api/ # Backend project
├─ autocars_api/
│ ├─ settings.py
│ ├─ urls.py
│ └─ ...
├─ cars/
│ ├─ models.py
│ ├─ serializers.py
│ ├─ views.py
│ └─ urls.py
├─ users/
│ ├─ models.py
│ ├─ serializers.py
│ ├─ views.py
│ └─ urls.py
└─ manage.py

autocars_frontend/ # Frontend project
├─ web/
│ ├─ templates/web/
│ │ ├─ base.html
│ │ ├─ login.html
│ │ ├─ register.html
│ │ ├─ cars.html
│ │ └─ addcar.html
│ ├─ views.py
│ └─ urls.py
└─ manage.py


---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/openescuela/demo-django-rest-freamwork.git
cd demo-django-rest-freamwork

2. Create a virtual environment:

python -m venv .myenv
source .myenv/bin/activate      # Linux/Mac
.myenv\Scripts\activate         # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Apply migrations:
python manage.py migrate

5. Create a superuser (optional, for backend admin):
python manage.py createsuperuser

## Running the Project
Backend

cd autocars_api
python manage.py runserver

API will be available at http://127.0.0.1:8000/api/.

Frontend

cd autocars_frontend
python manage.py runserver 8001

Frontend will be available at http://127.0.0.1:8001/.

## Usage

Open the frontend URL in your browser.

Register as a new user. Optionally, register as a seller to be able to add cars.

Login with your credentials.

Sellers can click Add Car in the navbar to post new cars.

View the list of cars under Cars.

## Contributing

Fork the repository

Create a feature branch: git checkout -b feature-name

Commit your changes: git commit -m "Add new feature"

Push to the branch: git push origin feature-name

Open a pull request

## License

MIT License






