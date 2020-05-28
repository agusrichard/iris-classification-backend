from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import user
from ... import db
from ...model import User


@user.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    print('register data', data)

    if not data and not data['username'] and not data['password']:
        return jsonify({'message': 'Please provide the required fields'})
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(                    
        username=data['username'],       
        email=data['email'],             
        fullname=data['username'],       
        password=hashed_password       
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Register success',
        'data': {
            'username': data['username'],
            'email': data['email'],
            'fullname': data['username']
        }
    })

@user.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    return ''

@user.route('/user', methods=['GET'])
def get_all_users():
    return jsonify({'message': 'Is it working?'})

@user.route('/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    return ''

