from flask import jsonify, request,  render_template
from app import app, db
from bson import ObjectId

# Routes pour les utilisateurs
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.find())
    return jsonify([{**user, '_id': str(user['_id'])} for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    result = db.users.insert_one(user)
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = request.json
    result = db.users.update_one({'_id': ObjectId(id)}, {'$set': user})
    if result.modified_count:
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = db.users.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

# Routes pour les comptes
@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = list(db.accounts.find())
    return jsonify([{**account, '_id': str(account['_id'])} for account in accounts])

@app.route('/accounts', methods=['POST'])
def create_account():
    account = request.json
    result = db.accounts.insert_one(account)
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/accounts/<id>', methods=['GET'])
def get_account(id):
    account = db.accounts.find_one({'_id': ObjectId(id)})
    if account:
        account['_id'] = str(account['_id'])
        return jsonify(account)
    return jsonify({'error': 'Account not found'}), 404

@app.route('/accounts/<id>', methods=['PUT'])
def update_account(id):
    account = request.json
    result = db.accounts.update_one({'_id': ObjectId(id)}, {'$set': account})
    if result.modified_count:
        return jsonify({'message': 'Account updated successfully'})
    return jsonify({'error': 'Account not found'}), 404

@app.route('/accounts/<id>', methods=['DELETE'])
def delete_account(id):
    result = db.accounts.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Account deleted successfully'})
    return jsonify({'error': 'Account not found'}), 404

# Routes pour les transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = list(db.transactions.find())
    return jsonify([{**transaction, '_id': str(transaction['_id'])} for transaction in transactions])

@app.route('/transactions', methods=['POST'])
def create_transaction():
    transaction = request.json
    result = db.transactions.insert_one(transaction)
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/transactions/<id>', methods=['GET'])
def get_transaction(id):
    transaction = db.transactions.find_one({'_id': ObjectId(id)})
    if transaction:
        transaction['_id'] = str(transaction['_id'])
        return jsonify(transaction)
    return jsonify({'error': 'Transaction not found'}), 404
