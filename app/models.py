from app import db
from bson import ObjectId
from datetime import datetime

class BaseModel:
    def __init__(self, collection):
        self.collection = collection

    def log_action(self, action, data=None, user_id=None):
        log_entry = {
            "timestamp": datetime.utcnow(),
            "action": action,
            "collection": self.collection.name,
            "data": data,
            "user_id": user_id
        }
        db.logs.insert_one(log_entry)
 
class User(BaseModel):
    def __init__(self):
        super().__init__(db.users)
        
    # Create user function
    def create(self, user_data):
        user_data['account'] = []
        result = self.collection.insert_one(user_data)
        user_id = str(result.inserted_id)
        self.log_action("CREATE", user_data, user_id)
        
        # Create an account for the user
        account_model = Account()
        account_data = {
            "owner_id": user_id,  # Link the account to the user
            "balance": 0,
            "currency": "USD"
        }
        account_id = account_model.create(account_data)

        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$push': {'account': account_id}}
        )
        
        return user_id 
    
    #Read a single user function
    def get_by_id(self, user_id):
        return self.collection.find_one({'_id': ObjectId(user_id)})  
      
    # Read all users function
    def get_all(self):
        return list(self.collection.find()) # retrieves all documents from the users collection and converts them to a list

    # Update user function
    def update(self, user_id, user_data):
        result = self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_data})
        if result.modified_count:
            self.log_action("UPDATE", user_data, user_id)
        return result

    # Delete user function
    def delete(self, user_id):
        result = self.collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count:
            self.log_action("DELETE", user_id=user_id)
        return result
    
    # get role function, Not among the crud, but to be used in "Roles and Permissions handling"
    def get_role(self, user_id):
        user = self.get_by_id(user_id)
        return user.get('role') if user else None    

class Account(BaseModel):
    def __init__(self):
        super().__init__(db.accounts)

    def get_all(self):
        return list(self.collection.find())

    def create(self, account_data):
        result = self.collection.insert_one(account_data)
        self.log_action("CREATE", account_data, str(result.inserted_id))
        return result.inserted_id

    def get_by_id(self, account_id):
        return self.collection.find_one({'_id': ObjectId(account_id)})

    def update(self, account_id, account_data):
        result = self.collection.update_one({'_id': ObjectId(account_id)}, {'$set': account_data})
        if result.modified_count:
            self.log_action("UPDATE", account_data, account_id)
        return result

    def delete(self, account_id):
        result = self.collection.delete_one({'_id': ObjectId(account_id)})
        if result.deleted_count:
            self.log_action("DELETE", user_id=account_id)
        return result

class Transaction(BaseModel):
    def __init__(self):
        super().__init__(db.transactions)

    def get_all(self):
        return list(self.collection.find())

    def create(self, transaction_data):
        result = self.collection.insert_one(transaction_data)
        self.log_action("CREATE", transaction_data, str(result.inserted_id))
        return result.inserted_id

    def get_by_id(self, transaction_id):
        return self.collection.find_one({'_id': ObjectId(transaction_id)})

    def update(self, transaction_id, transaction_data):
        result = self.collection.update_one({'_id': ObjectId(transaction_id)}, {'$set': transaction_data})
        if result.modified_count:
            self.log_action("UPDATE", transaction_data, transaction_id)
        return result

    def delete(self, transaction_id):
        result = self.collection.delete_one({'_id': ObjectId(transaction_id)})
        if result.deleted_count:
            self.log_action("DELETE", user_id=transaction_id)
        return result
    
class Log(BaseModel):
    def __init__(self):
        super().__init__(db.logs)

    def get_all(self):
        return list(self.collection.find().sort("timestamp", -1))

# Class to handle roles and permissions
class Role(BaseModel):
    def __init__(self):
        super().__init__(db.roles)

    # To get the list of all roles and there permissions
    def get_all_roles(self):
        return list(self.collection.find())

    def get_by_name(self, name):
        return self.collection.find_one({'name': name})
    
    def get_permissions(self, role_name):
        role = self.get_by_name(role_name)
        return role['permissions'] if role else {}

    def update_permissions(self, role_name, new_permissions):
        return self.collection.update_one(
            {'name': role_name},
            {'$set': {'permissions': new_permissions}}
        )
