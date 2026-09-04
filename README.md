# RevoShop API

RevoShop is a RESTful e-commerce backend API built with Flask, SQLAlchemy, and PostgreSQL.

The API manages users, products, categories, orders, and order items. It provides CRUD operations, validation, authentication, database relationships, automated testing, and load testing.

---

## Features

- User registration
- User login
- Product CRUD
- Category CRUD
- Order CRUD
- Order items
- Product stock management
- Data validation
- Error handling
- Password hashing
- PostgreSQL database
- SQLAlchemy ORM
- Database migrations with Flask-Migrate
- Automated testing with pytest
- Load testing with Locust
- Environment configuration with `.env`
- Production WSGI support with Gunicorn

The relationship between orders and products is implemented through the `order_items` table.

---

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Migrate
- PostgreSQL
- psycopg2-binary
- python-dotenv
- Werkzeug
- pytest
- Locust
- Gunicorn

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
│   ├── versions/
│   ├── alembic.ini
│   ├── env.py
│   └── README
│
├── tests/
│   ├── test_category.py
│   ├── test_product.py
│   └── test_order.py
│
├── .env
├── .env.example
├── .gitignore
├── create_tables.py
├── locustfile.py
├── migrations/
├── pytest.ini
├── queries.sql
├── requirements.txt
├── run.py
├── schema.sql
├── seed.sql
└── README.md
```

> The `.env` file must not be committed to GitHub because it contains sensitive configuration.

---

## Database Schema

The project uses PostgreSQL with the following tables:

### users

Stores user account information.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | VARCHAR(100) | User name |
| email | VARCHAR(120) | Unique email |
| password | VARCHAR(255) | Hashed password |
| created_at | TIMESTAMP | Account creation time |

### categories

Stores product categories.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | VARCHAR(100) | Unique category name |

### products

Stores products available in the store.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| name | VARCHAR(150) | Product name |
| description | TEXT | Product description |
| price | NUMERIC(10,2) | Product price |
| stock | Integer | Available stock |
| category_id | Integer | Foreign key to categories |

### orders

Stores customer orders.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| total | NUMERIC(10,2) | Order total |
| status | VARCHAR(50) | Order status |
| created_at | TIMESTAMP | Order creation time |

### order_items

Links orders and products.

| Column | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| order_id | Integer | Foreign key to orders |
| product_id | Integer | Foreign key to products |
| quantity | Integer | Ordered quantity |
| price | NUMERIC(10,2) | Product price at order time |

---

## Relationships

```text
User
 │
 └──< Orders
        │
        └──< OrderItems >── Product
                              │
                              └── Category
```

An order can contain multiple products through the `order_items` table.

---

## API Endpoints

Base URL for local development:

```text
http://127.0.0.1:5000
```

### User Module

#### Register User

```http
POST /users
```

Example request:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "test123"
}
```

Response:

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2026-09-04T10:00:00"
}
```

Status:

```text
201 Created
400 Bad Request
409 Conflict
```

---

### Login

```http
POST /auth/login
```

Example request:

```json
{
  "email": "john@example.com",
  "password": "test123"
}
```

Successful response:

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

Status:

```text
200 OK
400 Bad Request
401 Unauthorized
```

---

# Product Module

### Create Product

```http
POST /products
```

Example:

```json
{
  "name": "Laptop",
  "description": "Business laptop",
  "price": 10000000,
  "stock": 10,
  "category_id": 1
}
```

Status:

```text
201 Created
400 Bad Request
404 Not Found
```

### List Products

```http
GET /products
```

Status:

```text
200 OK
```

### Get Product

```http
GET /products/<id>
```

Example:

```text
GET /products/1
```

Status:

```text
200 OK
404 Not Found
```

### Update Product

```http
PUT /products/<id>
```

Example:

```json
{
  "name": "Updated Laptop",
  "price": 12000000,
  "stock": 8
}
```

Status:

```text
200 OK
400 Bad Request
404 Not Found
```

### Delete Product

```http
DELETE /products/<id>
```

A product linked to existing orders cannot be deleted.

Status:

```text
200 OK
404 Not Found
409 Conflict
```

---

# Category Module

### Create Category

```http
POST /categories
```

Example:

```json
{
  "name": "Electronics"
}
```

Status:

```text
201 Created
400 Bad Request
409 Conflict
```

### List Categories

```http
GET /categories
```

Status:

```text
200 OK
```

### Get Category

```http
GET /categories/<id>
```

Returns category information together with its products.

Status:

```text
200 OK
404 Not Found
```

### Update Category

```http
PUT /categories/<id>
```

Example:

```json
{
  "name": "Updated Electronics"
}
```

Status:

```text
200 OK
400 Bad Request
404 Not Found
409 Conflict
```

### Delete Category

```http
DELETE /categories/<id>
```

A category containing products cannot be deleted.

Status:

```text
200 OK
404 Not Found
409 Conflict
```

---

# Order Module

### Create Order

```http
POST /orders
```

Example:

```json
{
  "user_id": 4,
  "items": [
    {
      "product_id": 66,
      "quantity": 1
    }
  ]
}
```

The API:

1. Validates the user.
2. Validates each product.
3. Validates quantity.
4. Checks available stock.
5. Calculates the order total.
6. Creates the order.
7. Creates the order items.
8. Reduces product stock.

Status:

```text
201 Created
400 Bad Request
404 Not Found
```

### List Orders

```http
GET /orders
```

Optional filter:

```text
GET /orders?user_id=4
```

Status:

```text
200 OK
```

### Get Order

```http
GET /orders/<id>
```

Returns:

- Order information
- Order items
- Product details

Status:

```text
200 OK
404 Not Found
```

### Update Order

```http
PUT /orders/<id>
```

Example:

```json
{
  "status": "processing"
}
```

Allowed statuses:

```text
pending
processing
completed
cancelled
```

Status:

```text
200 OK
400 Bad Request
404 Not Found
```

### Delete Order

```http
DELETE /orders/<id>
```

When an order is deleted, its ordered quantities are restored to product stock.

Status:

```text
200 OK
404 Not Found
```

---

# Local Development Setup

## 1. Clone Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd revoshop-db
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, the virtual environment can still be used directly:

```powershell
.\venv\Scripts\python.exe
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env`:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/revoshop
```

Do not commit `.env` to Git.

Use `.env.example` as a reference:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/revoshop
```

---

## 5. Run Database Migrations

Apply migrations:

```powershell
flask db upgrade
```

For new model changes:

```powershell
flask db migrate -m "describe your changes"
```

Then apply:

```powershell
flask db upgrade
```

---

## 6. Run Flask Application

```powershell
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

Test the API:

```text
GET http://127.0.0.1:5000/api
```

Expected response:

```json
{
  "message": "RevoShop API is running",
  "status": "success"
}
```

---

# Testing

The project uses pytest for automated API testing.

Run all tests:

```powershell
pytest -v
```

Current test coverage includes:

- Category CRUD
- Product CRUD
- Order CRUD
- Validation
- Stock reduction
- Stock restoration
- Not-found handling
- Invalid input handling

Current local test result:

```text
48 passed
```

---

# Load Testing with Locust

The project uses Locust to simulate multiple users following a sequential user journey.

The test flow is:

```text
GET /products
        ↓
GET /products/<id>
        ↓
POST /orders
        ↓
GET /orders/<id>
```

Start Locust:

```powershell
.\venv\Scripts\locust.exe -f locustfile.py --web-port 8090
```

Open:

```text
http://localhost:8090
```

Example load test configuration:

```text
Users: 50
Spawn rate: 5
Host: http://127.0.0.1:5000
```

The test can then be increased to:

```text
Users: 200
Spawn rate: 5
```

The Locust test uses a dedicated product for load testing so the primary product stock is not consumed.

---

# Environment and Security

Sensitive configuration is stored in `.env` and accessed through `python-dotenv` and `os.getenv()`.

Example:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

The `.gitignore` excludes:

```text
.env
__pycache__/
venv/
.venv/
*.log
```

The safe template `.env.example` is included in the repository.

---

# Production Deployment

The final project is intended to use:

```text
Flask
    ↓
Gunicorn
    ↓
Hosted Platform
    ↓
Hosted PostgreSQL
```

Before deployment:

1. Configure the production `DATABASE_URL`.
2. Apply migrations:

```bash
flask db upgrade
```

3. Start the application with Gunicorn.

Example:

```bash
gunicorn "run:app"
```

The exact start command may vary depending on the selected deployment platform.

---

# Production Verification

After deployment, verify:

```text
GET /products
GET /products/<id>
POST /products
PUT /products/<id>
DELETE /products/<id>

GET /categories
GET /categories/<id>
POST /categories
PUT /categories/<id>
DELETE /categories/<id>

POST /orders
GET /orders
GET /orders/<id>
PUT /orders/<id>
DELETE /orders/<id>

POST /users
POST /auth/login
```

The production PostgreSQL database should contain:

```text
users
products
categories
orders
order_items
```

---

# Screenshots

The final submission should include screenshots demonstrating:

## Postman

- GET request
- POST request
- PUT request
- DELETE request
- Product CRUD
- Category CRUD
- Order requests
- Login request

## PostgreSQL / pgAdmin

- Database
- Tables
- Foreign keys
- Relationships
- `order_items` junction table

## Locust

- 50-user test
- 200-user test
- Response times
- Failure rate

## Deployment

- Hosted API
- Hosted database
- Public API URL

Add screenshots below when preparing the final submission.

---

# Project Status

Current implementation includes:

- PostgreSQL database
- SQLAlchemy models
- Flask application
- Flask-Migrate
- Product CRUD
- Category CRUD
- Order CRUD
- User registration
- Authentication login
- Input validation
- Password hashing
- Automated tests
- Locust load testing
- Environment configuration
- Gunicorn support

Remaining finalization work may include:

- Production database deployment
- Flask API deployment
- Public API verification
- GitHub repository finalization
- Postman screenshots
- pgAdmin screenshots
- Deployment screenshots