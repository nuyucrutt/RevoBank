# RevoBank API

## Overview
RevoBank API is a RESTful API for managing user accounts and transactions in a banking application. It provides endpoints for user management, account management, and transaction management, with built-in authentication and authorization.

## Features
### User Management:
- Create user accounts with secure password hashing
- User profile with:
  - Unique username and email
  - Account creation timestamps
  - Password reset functionality

### Account Management:
- Multiple account types (savings, checking)
- Unique account numbers
- Balance tracking with decimal precision
- Account creation/update timestamps

### Transaction Management:
- Secure transaction processing
- Support for:
  - Deposits
  - Withdrawals
  - Transfers between accounts
- Transaction history with:
  - Timestamps
  - Descriptions
  - Amount tracking

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd RevoBank
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Database Setup:
   - Install MySQL and create a database:
     ```bash
     mysql -u root -p
     CREATE DATABASE revo_bank;
     ```
   - Configure environment variables in `.env` file:
     ```ini
     DATABASE_URL=mysql://username:password@localhost/revo_bank
     SECRET_KEY=your-secret-key
     ```

4. Initialize the database:
   ```bash
   python app.py
   ```

5. Run the application:
   ```bash
   flask run
   ```

## API Usage
### User Management:
- `POST /users`: 
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- `GET /users/me`: Get authenticated user profile
- `PUT /users/me`: Update profile

### Account Management:
- `GET /accounts`: List all user accounts
- `POST /accounts`: 
  ```json
  {
    "account_type": "savings|checking",
    "account_number": "string",
    "initial_balance": 0.00
  }
  ```
- `PUT /accounts/<id>`: Update account
- `DELETE /accounts/<id>`: Delete account

### Transaction Management:
- `GET /transactions`: List all transactions
- `POST /transactions`: 
  ```json
  {
    "amount": 100.00,
    "transaction_type": "deposit|withdrawal|transfer",
    "description": "string",
    "from_account_id": 1,  // optional
    "to_account_id": 2     // optional
  }
  ```

## Database Schema
![Database Schema Diagram]

### Relationships:
- One User → Many Accounts
- One Account → Many Transactions
- Transactions link Accounts (optional for deposits/transfers)

## Deployment
1. Set up MySQL on cloud provider (AWS RDS, Google Cloud SQL)
2. Update `.env` with production credentials:
   ```ini
   DATABASE_URL=mysql://prod_user:securepass@db-host/revo_bank_prod
   FLASK_ENV=production
   SECRET_KEY=your-production-secret
   ```
3. Configure WSGI server (Gunicorn, uWSGI)
4. Set up reverse proxy (Nginx, Apache)

## Authentication
JWT authentication is required for protected endpoints. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## License
This project is licensed under the MIT License.

## Collection details
- **URL for published documentation:**
https://documenter.getpostman.com/view/43110513/2sAYkBrfsa
- **Collection name:** RevoBank API
- **Versions:** CURRENT
- **Environment:** No Environment
