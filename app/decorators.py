from functools import wraps
from flask import jsonify, g
from models import User, Role
from flask_jwt_extended import get_jwt_identity, jwt_required  

def require_permission(resource, action):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user_model = User()
            role_model = Role()

            user_role = user_model.get_role(user_id)
            permissions = role_model.get_permissions(user_role)

            if resource in permissions and action in permissions[resource]:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Permission denied'}), 403
        return decorated_function
    return decorator
