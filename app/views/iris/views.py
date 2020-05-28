from flask import jsonify, request
from . import iris
from ...model import Iris
from ... import db

@iris.route('/iris', methods=['GET'])
def get_all_iris():
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

@iris.route('/iris/<iris_id>', methods=['GET'])
def get_one_iris(iris_id):
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

@iris.route('/iris', methods=['POST'])
def create_iris():
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
        label=data.get('label')
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