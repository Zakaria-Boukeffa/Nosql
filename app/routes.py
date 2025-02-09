from flask import jsonify, request,  render_template
from app import app, db
from flask import jsonify, request, render_template
from app import app
from models import (
    get_all_users, get_user_by_id, create_user, update_user, delete_user,
    get_all_accounts, get_account_by_id, create_account, update_account, delete_account,
    get_all_transactions, get_transaction_by_id, create_transaction,
    get_all_logs
)

# HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')


# USER ROUTES
@app.route('/users', methods=['GET'])
def get_users():
    users = get_all_users()
    return jsonify([{**user, '_id': str(user['_id'])} for user in users])

@app.route('/users', methods=['POST'])
def add_user():
    user_id = create_user(request.json)
    return jsonify({'id': str(user_id)}), 201

@app.route('/users/<id>', methods=['GET'])
def fetch_user(id):
    user = get_user_by_id(id)
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<id>', methods=['PUT'])
def modify_user(id):
    result = update_user(id, request.json)
    return jsonify({'message': 'User updated successfully'}) if result.modified_count else jsonify({'error': 'User not found'}), 404

@app.route('/users/<id>', methods=['DELETE'])
def remove_user(id):
    result = delete_user(id)
    return jsonify({'message': 'User deleted successfully'}) if result.deleted_count else jsonify({'error': 'User not found'}), 404


# ACCOUNT ROUTES
@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = get_all_accounts()
    return jsonify([{**account, '_id': str(account['_id'])} for account in accounts])

@app.route('/accounts', methods=['POST'])
def add_account():
    account_id = create_account(request.json)
    return jsonify({'id': str(account_id)}), 201

@app.route('/accounts/<id>', methods=['GET'])
def fetch_account(id):
    account = get_account_by_id(id)
    if account:
        account['_id'] = str(account['_id'])
        return jsonify(account)
    return jsonify({'error': 'Account not found'}), 404

@app.route('/accounts/<id>', methods=['PUT'])
def modify_account(id):
    result = update_account(id, request.json)
    return jsonify({'message': 'Account updated successfully'}) if result.modified_count else jsonify({'error': 'Account not found'}), 404

@app.route('/accounts/<id>', methods=['DELETE'])
def remove_account(id):
    result = delete_account(id)
    return jsonify({'message': 'Account deleted successfully'}) if result.deleted_count else jsonify({'error': 'Account not found'}), 404


# TRANSACTION ROUTES
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = get_all_transactions()
    return jsonify([{**transaction, '_id': str(transaction['_id'])} for transaction in transactions])

@app.route('/transactions', methods=['POST'])
def add_transaction():
    transaction_id = create_transaction(request.json)
    return jsonify({'id': str(transaction_id)}), 201

@app.route('/transactions/<id>', methods=['GET'])
def fetch_transaction(id):
    transaction = get_transaction_by_id(id)
    if transaction:
        transaction['_id'] = str(transaction['_id'])
        return jsonify(transaction)
    return jsonify({'error': 'Transaction not found'}), 404


# LOG ROUTES
@app.route('/logs', methods=['GET'])
def get_logs():
    logs = get_all_logs()
    return jsonify([{**log, '_id': str(log['_id'])} for log in logs])
