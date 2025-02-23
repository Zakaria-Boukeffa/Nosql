from flask import jsonify, request, render_template, redirect, url_for, Response

from app import app
from models import User, Account, Transaction, Log, Role
from bson import ObjectId, json_util
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
from decorators import require_permission


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user_model = User()
    user = user_model.collection.find_one({'username': username, 'password': password})
    if user:
        access_token = create_access_token(identity=str(user['_id']))
        refresh_token = create_refresh_token(identity=str(user['_id']))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200


@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    user_model = User()  
    user_id = user_model.create(user_data)
    user = user_model.collection.find_one({'_id': ObjectId(user_id)})
    if user:
        access_token = create_access_token(identity=str(user['_id']))
        refresh_token = create_refresh_token(identity=str(user['_id']))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 201  
    else:
        return jsonify({'message': 'Failed to create user or retrieve user ID'}), 500


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


# User routes   
# Create user route
@app.route('/users', methods=['POST'])
@jwt_required()
@require_permission('users', 'create')
def add_user():
    user_model = User()
    try:
        user_data = request.get_json() 
        user_id = user_model.create(user_data)
        return jsonify({'message': 'User created successfully', 'user_id': str(user_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
     
# Read all users route
@app.route('/users', methods=['GET'])
@jwt_required()
@require_permission('users', 'read')
def get_users():
    user_model = User()
    users = user_model.get_all() # Calls the get_all() method of the User class.
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return jsonify(users)

# Read a single user route
@app.route('/users/<id>', methods=['GET'])
@jwt_required()
@require_permission('users', 'read')
def fetch_user(id):
    user_model = User()
    user = user_model.get_by_id(id)
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# Update user route
@app.route('/users/<id>', methods=['PUT'])
@jwt_required()
@require_permission('users', 'update')
def modify_user(id):
    user_model = User()
    result = user_model.update(id, request.json)
    return jsonify({'message': 'User updated successfully'}) if result.modified_count else jsonify({'error': 'User not found'}), 404

# Delete user route
@app.route('/users/<id>', methods=['DELETE'])
@jwt_required()
@require_permission('users', 'delete')
def remove_user(id):
    user_model = User()
    result = user_model.delete(id)
    return jsonify({'message': 'User deleted successfully'}) if result.deleted_count else jsonify({'error': 'User not found'}), 404


# Account routes
# Create account route
@app.route('/accounts', methods=['POST'])
@jwt_required()
@require_permission('accounts', 'create')
def add_account():
    account_model = Account()
    account_id = account_model.create(request.json)
    return jsonify({'id': str(account_id)}), 201

# Read all accounts route
@app.route('/accounts', methods=['GET'])
@jwt_required()
@require_permission('accounts', 'read')
def get_accounts():
    account_model = Account()
    accounts = account_model.get_all()
    return jsonify([{**account, '_id': str(account['_id'])} for account in accounts])

# Read a single account route
@app.route('/accounts/<id>', methods=['GET'])
@jwt_required()
@require_permission('accounts', 'read')
def fetch_account(id):
    account_model = Account()
    account = account_model.get_by_id(id)
    if account:
        account['_id'] = str(account['_id'])
        return jsonify(account)
    return jsonify({'error': 'Account not found'}), 404

# Update account route
@app.route('/accounts/<id>', methods=['PUT'])
@jwt_required()
@require_permission('accounts', 'update')
def modify_account(id):
    account_model = Account()
    result = account_model.update(id, request.json)
    return jsonify({'message': 'Account updated successfully'}) if result.modified_count else jsonify({'error': 'Account not found'}), 404

# Delete account route
@app.route('/accounts/<id>', methods=['DELETE'])
@jwt_required()
@require_permission('accounts', 'delete')
def remove_account(id):
    account_model = Account()
    result = account_model.delete(id)
    return jsonify({'message': 'Account deleted successfully'}) if result.deleted_count else jsonify({'error': 'Account not found'}), 404


# Transaction routes
# Create transaction route
@app.route('/transactions', methods=['POST'])
@jwt_required()
@require_permission('transactions', 'create')
def add_transaction():
    transaction_model = Transaction()
    transaction_id = transaction_model.create(request.json)
    return jsonify({'id': str(transaction_id)}), 201

# Read all transactions route
@app.route('/transactions', methods=['GET'])
@jwt_required()
@require_permission('transactions', 'read')
def get_transactions():
    transaction_model = Transaction()
    transactions = transaction_model.get_all()
    return jsonify([{**transaction, '_id': str(transaction['_id'])} for transaction in transactions])

# Read a single transaction route
@app.route('/transactions/<id>', methods=['GET'])
@jwt_required()
@require_permission('transactions', 'read')
def fetch_transaction(id):
    transaction_model = Transaction()
    transaction = transaction_model.get_by_id(id)
    if transaction:
        transaction['_id'] = str(transaction['_id'])
        return jsonify(transaction)
    return jsonify({'error': 'Transaction not found'}), 404

# Update transaction route
@app.route('/transactions/<id>', methods=['PUT'])
@jwt_required()
@require_permission('transactions', 'update')
def modify_transaction(id):
    transaction_model = Transaction()
    result = transaction_model.update(id, request.json)
    return jsonify({'message': 'Transaction updated successfully'}) if result.modified_count else jsonify({'error': 'Transaction not found'}), 404

# Delete transaction route
@app.route('/transactions/<id>', methods=['DELETE'])
@jwt_required()
@require_permission('transactions', 'delete')
def delete_transaction(id):
    transaction_model = Transaction()
    result = transaction_model.delete(id)
    return jsonify({'message': 'Transaction deleted successfully'}) if result.deleted_count else jsonify({'error': 'Transaction not found'}), 404

# Logs routes
# Read all logs route
@app.route('/logs', methods=['GET'])
@jwt_required()
@require_permission('logs', 'read')
def get_logs():
    log_model = Log()
    logs = log_model.get_all()
    return Response(
        json_util.dumps(logs, default=str),
        mimetype='application/json'
    )
    
# Roles routes
@app.route('/roles', methods=['GET'])
@jwt_required()
@require_permission('roles', 'read')
def get_roles():
    role_model = Role()
    roles = role_model.get_all_roles()
    return jsonify([{**role, '_id': str(role['_id'])} for role in roles])

@app.route('/roles/<name>', methods=['GET'])
@jwt_required()
@require_permission('roles', 'read')
def get_role(name):
    role_model = Role()
    role = role_model.get_by_name(name)
    if role:
        role['_id'] = str(role['_id'])
        return jsonify(role)
    return jsonify({'error': 'Role not found'}), 404

@app.route('/roles/<name>/permissions', methods=['GET'])
@jwt_required()
@require_permission('roles', 'read')
def get_role_permissions(name):
    role_model = Role()
    permissions = role_model.get_permissions(name)
    if permissions:
        return jsonify(permissions)
    return jsonify({'error': 'Role not found'}), 404

@app.route('/roles/<name>/permissions', methods=['PUT'])
@jwt_required()
@require_permission('roles', 'update')
def update_role_permissions(name):
    role_model = Role()
    new_permissions = request.json
    result = role_model.update_permissions(name, new_permissions)
    if result.modified_count:
        return jsonify({'message': 'Permissions updated successfully'})
    return jsonify({'error': 'Role not found'}), 404
