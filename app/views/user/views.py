from . import user
from flask import jsonify



@user.route('/auth/login', methods=['POST'])
def register():
    return ''

@user.route('/auth/register', methods=['POST'])
def login():
    return ''

@user.route('/user', methods=['GET'])
def get_all_users():
    return jsonify({'message': 'Is it working?'})

@user.route('/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
    return ''

