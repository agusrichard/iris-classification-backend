import os
from flask import current_app
from app import db
from ..model import Iris

def populate_iris():
    file_path = os.path.join(current_app.root_path, 'static/estimator/iris.csv')
    with open(file_path, 'r') as file:
        row = file.readline()
        while True:
            row = file.readline()
            components = row.strip().replace('"', '').split(',')
            if not row:
                break
            print(components)
            iris = Iris(
                sepal_length = float(components[0]),
                sepal_width = float(components[1]),
                petal_length = float(components[2]),
                petal_width = float(components[3]),
                label = components[4]
            )
            db.session.add(iris)
        db.session.commit()