import datetime
import jwt
from flask import jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import user
from ... import db
from ...model import User
from ...utilities.user import token_required


@user.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print('register data', data)

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Please provide the required fields'}), 400
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
    except Exception as e:
        print(e)
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@user.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print('data', data)
        print('email data', data.get('email'))
        print('password data', data.get('password'))

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Please provide required fields'
            }), 400

        user = User.query.filter_by(email=data.get('email')).first()

        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        if check_password_hash(user.password, data.get('password')):
            token = jwt.encode({
                'id': user.id,
                'email': user.email,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.config['SECRET_KEY'])

            return jsonify({
                'success': True,
                'message': 'Login success',
                'data': {
                    'id': user.id,
                    'email': user.email,
                    'password': user.password
                },
                'token': token.decode('UTF-8')
            })

        return jsonify({
            'success': False,
            'message': 'Failed to login'
        }), 500

    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@user.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    try:
        users = User.query.all()

        if not users:
            return jsonify({
                'success': False,
                'message': 'Users not found'
            }), 404

        output = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        } for user in users]

        return jsonify({
            'success': True,
            'message': 'Success to get all users',
            'data': output
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@user.route('/user/profile', methods=['GET'])
@token_required
def get_one_user(current_user):
    try:
        if not current_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Success to get user with id ' + str(current_user.id),
            'data': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'password': current_user.password
            }
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@user.route('/user', methods=['DELETE'])
@token_required
def delete_user(current_user):
    try:
        print(current_user)
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Success to delete user'
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500

@user.route('/', methods=['GET'])
def home():
    return jsonify({
        'success': True,
        'message': 'Welcome to our REST API'
    })