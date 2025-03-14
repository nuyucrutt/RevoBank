# RevoBank API

## Overview
RevoBank API is a RESTful API for managing user accounts and transactions in a banking application. It provides endpoints for user management, account management, and transaction management, with built-in authentication and authorization.

## Features
- User Management:
  - Create a new user account
  - Retrieve and update the authenticated user's profile
- Account Management:
  - Retrieve a list of accounts for the authenticated user
  - Create, update, and delete accounts
- Transaction Management:
  - Retrieve a list of transactions for the authenticated user's accounts
  - Initiate new transactions (deposits, withdrawals, transfers)

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

3. Set up the database (e.g., using SQLite or another database of your choice).

4. Run the application:
   ```bash
   python app.py
   ```

## API Usage
- **User Management:**
  - `POST /users`: Create a new user account.
  - `GET /users/me`: Retrieve the authenticated user's profile.
  - `PUT /users/me`: Update the authenticated user's profile.

- **Account Management:**
  - `GET /accounts`: Retrieve all accounts for the authenticated user.
  - `POST /accounts`: Create a new account.
  - `PUT /accounts/<id>`: Update an existing account.
  - `DELETE /accounts/<id>`: Delete an account.

- **Transaction Management:**
  - `GET /transactions`: Retrieve all transactions for the authenticated user's accounts.
  - `POST /transactions`: Initiate a new transaction.

## Authentication
Authentication is required for certain endpoints. Ensure to include the necessary authentication tokens in your requests.

## License
This project is licensed under the MIT License.

## Collection details

- **URL for published documentation :**
https://documenter.getpostman.com/view/43110513/2sAYkBrfsa

- **Collection name :**
RevoBank API

- **Versions :**
CURRENT

- **Environment :**
No Environment

- **SEO** 
- **Title :**
RevoBank API

- **Description :**
You have’t added a description tag. By default, the documentation content will be displayed in markdown format.


