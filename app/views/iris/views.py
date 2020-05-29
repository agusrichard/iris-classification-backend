import numpy as np
from flask import jsonify, request
from . import iris
from ... import db
from ...model import Iris
from ...utilities.user import token_required
from ...estimator.make_prediction import make_prediction


@iris.route('/iris', methods=['GET'])
@token_required
def get_all_iris(current_user):
    try:
        irises = Iris.query.all()

        if not irises:
            return jsonify({
                'sucess': False,
                'message': 'Irises not found'
            }), 404

        output = [{
            'id': iris.id,
            'sepal_length': iris.sepal_length,
            'sepal_width': iris.sepal_width,
            'petal_length': iris.petal_length,
            'petal_width': iris.petal_width,
            'label': iris.label,
            'user_id': iris.user_id
        } for iris in irises]

        return jsonify({
            'success': True,
            'message': 'Success get all irises',
            'data': output
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@iris.route('/iris/<iris_id>', methods=['GET'])
@token_required
def get_one_iris(current_user, iris_id):
    try:
        iris = Iris.query.filter_by(id=iris_id).first()

        if not iris:
            return jsonify({
                'success': False,
                'message': 'Iris not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Success to get iris',
            'data': {
                'id': iris.id,
                'sepal_length': iris.sepal_length,
                'sepal_width': iris.sepal_width,
                'petal_length': iris.petal_length,
                'petal_width': iris.petal_width,
                'label': iris.label,
                'user_id': iris.user_id
            }
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@iris.route('/iris', methods=['POST'])
@token_required
def create_iris(current_user):
    try:
        data = request.get_json()
        print('create iris', data)

        if not data.get('sepal_length') or not data.get('sepal_width') \
                or not data.get('petal_length') or not data.get('petal_width') \
                or not data.get('label'):
            return jsonify({
                'success': False,
                'message': 'Please provide the required fields'
            }), 400

        iris = Iris(
            sepal_length=float(data.get('sepal_length')),
            sepal_width=float(data.get('sepal_width')),
            petal_length=float(data.get('petal_length')),
            petal_width=float(data.get('petal_width')),
            label=data.get('label'),
            user_id=current_user.id
        )

        db.session.add(iris)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Success to create iris',
            'data': {
                'sepal_length': float(iris.sepal_length),
                'sepal_width': float(iris.sepal_width),
                'petal_length': float(iris.petal_length),
                'petal_width': float(iris.petal_width),
                'label': iris.label,
            }
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@iris.route('/iris/<iris_id>', methods=['DELETE'])
@token_required
def delete_iris(current_user, iris_id):
    try:
        iris = Iris.query.filter_by(id=iris_id).first()
        if not iris:
            return jsonify({
                'success': False,
                'message': 'Iris not found'
            }), 404
        
        db.session.delete(iris)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Success to delete iris'
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500


@iris.route('/iris/predict', methods=['POST'])
@token_required
def get_prediction(current_user):
    try:
        data = request.get_json()
        arr = [data.get('sepal_length'), data.get('sepal_width'), data.get('petal_length'), data.get('petal_width')]
        arr = np.array(arr).reshape(1, -1)
        prediction = make_prediction(arr)
        return jsonify({
            'success': True,
            'message': 'Success to get the prediction',
            'data': prediction
        })
    except:
        return jsonify({
            'success': False,
            'message': 'Internal error'
        }), 500
