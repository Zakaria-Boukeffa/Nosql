from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['bank_db']


# LOGGING FUNCTION
def log_action(action, collection, data=None, user_id=None):
    """Log API actions for auditing."""
    log_entry = {
        "timestamp": datetime.utcnow(),
        "action": action,
        "collection": collection,
        "data": data,
        "user_id": user_id
    }
    db.logs.insert_one(log_entry)


# USER MODEL (CRUD)
def get_all_users():
    return list(db.users.find())

def create_user(user_data):
    user_id = db.users.insert_one(user_data).inserted_id
    log_action("CREATE", "users", user_data, str(user_id))  # Log user creation
    return user_id

def get_user_by_id(user_id):
    return db.users.find_one({'_id': ObjectId(user_id)})

def update_user(user_id, user_data):
    result = db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user_data})
    if result.modified_count:
        log_action("UPDATE", "users", user_data, user_id)
    return result

def delete_user(user_id):
    result = db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count:
        log_action("DELETE", "users", user_id=user_id)
    return result


# ACCOUNT MODEL (CRUD)
def get_all_accounts():
    return list(db.accounts.find())

def create_account(account_data):
    account_id = db.accounts.insert_one(account_data).inserted_id
    log_action("CREATE", "accounts", account_data, str(account_id))
    return account_id

def get_account_by_id(account_id):
    return db.accounts.find_one({'_id': ObjectId(account_id)})

def update_account(account_id, account_data):
    result = db.accounts.update_one({'_id': ObjectId(account_id)}, {'$set': account_data})
    if result.modified_count:
        log_action("UPDATE", "accounts", account_data, account_id)
    return result

def delete_account(account_id):
    result = db.accounts.delete_one({'_id': ObjectId(account_id)})
    if result.deleted_count:
        log_action("DELETE", "accounts", user_id=account_id)
    return result


# TRANSACTION MODEL (CRUD)
def get_all_transactions():
    return list(db.transactions.find())

def create_transaction(transaction_data):
    transaction_id = db.transactions.insert_one(transaction_data).inserted_id
    log_action("CREATE", "transactions", transaction_data, str(transaction_id))
    return transaction_id

def get_transaction_by_id(transaction_id):
    return db.transactions.find_one({'_id': ObjectId(transaction_id)})

# LOG MODEL (READ)
def get_all_logs():
    return list(db.logs.find().sort("timestamp", -1))
