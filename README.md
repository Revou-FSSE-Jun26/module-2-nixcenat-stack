# RevoShop Database

Backend database design and schema setup for the RevoShop e-commerce platform using PostgreSQL.

## Repository Structure
revoshop-db/
├── schema.sql        # Table definitions and foreign key relationships
├── seed.sql          # Sample data for all tables
├── queries.sql       # Test queries demonstrating WHERE, ORDER BY, and LIMIT
├── erd_diagram.png   # Entity-Relationship Diagram (ERD)
├── .gitignore        # Ignored files configuration
└── README.md         # Project documentation and local setup instructions
## Setup & Local Installation

### Prerequisites
- PostgreSQL 14+ installed locally
- pgAdmin 4 or `psql` CLI

### 1. Create Database
Open pgAdmin or run via `psql`:
```sql
CREATE DATABASE revoshop_db;
### 2. Run Schema & Seed Files
Execute the SQL files in the following order using pgAdmin Query Tool or terminal:

1. `schema.sql`
2. `seed.sql`
3. `queries.sql`

