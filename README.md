# RevoShop Database

PostgreSQL database schema for the RevoShop online store.

## Database

Database name:

```text
revoshop_db
```

## Tables

The database contains five tables:

* `users` — stores customer account information.
* `categories` — stores product categories.
* `products` — stores products available in the store.
* `orders` — stores customer orders.
* `order_items` — junction table connecting orders and products.

The `order_items` table creates a many-to-many relationship between `orders` and `products`.

> Note: The `users` table intentionally does not contain a `role` column. The `role` column will be introduced in Checkpoint 2.

## Requirements

* PostgreSQL
* pgAdmin 4
* Git

## Setup

### 1. Create the database

Open pgAdmin and create a database named:

```text
revoshop_db
```

### 2. Create the tables

Open Query Tool for `revoshop_db` and execute:

```text
schema.sql
```

### 3. Insert sample data

Execute:

```text
seed.sql
```

This inserts sample users, categories, products, orders, and order items.

### 4. Run queries

Execute:

```text
queries.sql
```

The query file contains examples using `WHERE`, `ORDER BY`, `LIMIT`, and table joins.

## Database Relationships

```text
users
  │
  │ 1:N
  ▼
orders
  │
  │ 1:N
  ▼
order_items
  ▲
  │ N:1
  │
products
  ▲
  │ N:1
  │
categories
```

## Verification

After running `schema.sql`, refresh:

```text
Databases
└── revoshop_db
    └── Schemas
        └── public
            └── Tables
```

The following tables should be visible:

```text
users
categories
products
orders
order_items
```

## Project Structure

```text
revoshop-database/
├── schema.sql
├── seed.sql
├── queries.sql
├── README.md
└── .gitignore
```
