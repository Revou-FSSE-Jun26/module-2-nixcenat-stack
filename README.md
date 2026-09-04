# RevoShop API

Backend REST API untuk aplikasi e-commerce RevoShop.

Project ini dibuat menggunakan Flask dan PostgreSQL/SQLAlchemy, dengan fitur:

- User registration
- User login
- CRUD Products
- CRUD Categories
- CRUD Orders
- Order items
- Validasi data
- Pytest automated testing
- Locust load testing

---

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- SQLAlchemy
- Pytest
- Locust

---

## Project Structure

```text
revoshop-db/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes.py
│
├── migrations/
│
├── tests/
│   └── test_category.py
│
├── venv/
│
├── run.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignores