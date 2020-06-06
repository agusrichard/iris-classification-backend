from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config


db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	CORS(app)
	db.init_app(app)
	

	from .views.user import user
	from .views.iris import iris
	app.register_blueprint(user)
	app.register_blueprint(iris)

	return app
