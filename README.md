# Banking API Documentation

## 1. Overview

This API allows users to manage banking operations, including account creation, transactions, authentication, and role-based access control.

## 2. Dependencies and Environment Setup

### Required Dependencies

Ensure you have the following dependencies installed:

- Python 3.8+
- Flask
- Flask-JWT-Extended
- PyMongo
- MongoDB (local or cloud instance)

Install dependencies using:


```bash
pip install -r requirements.txt
```


### Database Setup

1. Start MongoDB and create a database named `bank_db`.
2. Import the following collections (a reference dump is available in the `data` folder):
   - users
   - logs
   - accounts
   - transactions
   - roles

### Running the Application
```
python app.py
```
The API will be available at http://localhost:5000.


## 3. Authentication and Session Management
This API uses **JWT (JSON Web Tokens)** for authentication. 
Upon successful signup or login, users receive an **Access Token** and a **Refresh Token**.
The **Access Token** is used to authenticate API requests, while the **Refresh Token** allows obtaining a new access token without requiring re-authentication.


## 4. Role and Access Management

In this application, we manage roles and permissions using a JSON file, `permissions.py`. A `Role` class is responsible for handling operations such as modifying role permissions and retrieving the associated permissions for each role.

Roles define the specific permissions granted, and each route is protected by JWT authentication to ensure secure access. For example, to restrict access to a specific route based on the user's role and permissions, we use the following approach:

```
@app.route('/users', methods=['POST'])
@jwt_required()
@require_permission('users', 'create')
```

Here, the jwt_required() decorator ensures that only authenticated users can access the route, while the require_permission('users', 'create') decorator checks that the user has the necessary permissions to perform the operation (in this case, creating a user).


## 5. Logging System

All API actions are logged for traceability. The logs collection stores information about operations performed by users.

Log Schema Example:
{
"user_id": "ObjectId",
"action": "CREATE_ACCOUNT",
"timestamp": "2025-02-23T12:00:00Z"
}

## 6. CRUD Operations:

### User Class
- **Create**: Creates a new user and an associated account.
- **Read**: Retrieves a user by ID or fetches all users.
- **Update**: Updates a user's data.
- **Delete**: Deletes a user.

### Account Class
- **Create**: Creates a new account.
- **Read**: Retrieves an account by ID or fetches all accounts.
- **Update**: Updates account information.
- **Delete**: Deletes an account.

### Transaction Class
- **Create**: Records a new transaction.
- **Read**: Retrieves a transaction by ID or fetches all transactions.
- **Update**: Updates transaction details.
- **Delete**: Deletes a transaction.

### Log Class
- **Read**: Fetches logs in descending order by timestamp.

### Role Class
- **Read**: Retrieves all roles or fetches permissions of a specific role.
- **Update**: Updates the permissions of a given role.


## 7. User Stories

### Super Administrator
**As a super administrator, I want to manage user access and permissions across the platform and oversee the overall activity to ensure the security and proper functioning of the banking system.**

**Example**: When the super administrator wants to delete an account, using the `DELETE` method, the `remove_account` function in `routes.py` calls the `delete_account` function in `models.py`. The `delete_account` function removes the specified account from the `accounts` collection.

---

### Administrator
**As an administrator, I want to create, modify, and delete user accounts (clients, employees, managers, etc.), and configure security settings to ensure effective role management and compliance with banking and cybersecurity regulations.**

**Example**: When the administrator wants to create a user account, using the `POST` method, the `add_account` function in `routes.py` calls the `create_account` function in `models.py`. The `create_account` function inserts a new account into the `accounts` collection.

---

### Gestionnaire ( role manager)
**As a manager, I want to view the list of client accounts and their transaction history, so I can assist clients in case of issues or detected anomalies.**

**Example**: When the manager wants to view the list of user accounts, using the `GET` method, the `get_accounts` function in `routes.py` calls the `get_all_accounts` function in `models.py`. The `get_all_accounts` function returns the list of user accounts from the `accounts` collection.

---

### Manager
**As a manager, I want to view a consolidated view of team performance and banking activities to make strategic decisions for service improvement.**

**Example**: When the manager wants to view the list of transactions, using the `GET` method, the `get_transactions` function in `routes.py` calls the `get_all_transactions` function in `models.py`. The `get_all_transactions` function returns the list of transactions from the `transactions` collection.

---

### System Analyst
**As a system analyst, I want to analyze system logs and performance to detect anomalies and prevent potential technical incidents.**

**Example**: When the system analyst wants to view the logs, using the `GET` method, the `get_logs` function in `routes.py` calls the `get_all_logs` function in `models.py`. The `get_all_logs` function returns the logs from the `logs` collection.

---

### Marketing Analyst
**As a marketing analyst, I want to view data on user account balances and transactions to analyze their behavior and the effectiveness of marketing campaigns.**

**Example**: When the marketing analyst wants to analyze the behavior of client accounts, using the `GET` method, the `fetch_transaction` function in `routes.py` calls the `get_transaction_by_id` function in `models.py`. The `get_transaction_by_id` function allows the analyst to examine the transaction history of specific accounts to analyze the impact of marketing efforts.

---

### Client (User)
**As a client, I want to view my personal information, account balance, and transaction history to check my activities and ensure proper account management.**

**Example**: When the client wants to perform a transaction, using the `POST` method, the `add_transaction` function in `routes.py` calls the `create_transaction` function in `models.py`. The `create_transaction` function inserts a new transaction into the `transactions` collection.


