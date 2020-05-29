import os
from dotenv import load_dotenv
from app import create_app, db
from app.model import User, Iris
from app.utilities.iris import populate_iris
from app.estimator.estimator import create_estimator

load_dotenv()
app = create_app()

@app.shell_context_processor
def make_shell_context():
	return dict(
		db=db, 
		User=User, 
		Iris=Iris, 
		populate_iris=populate_iris, 
		create_estimator=create_estimator
	)


if __name__ == '__main__':
	app.run(debug=bool(os.getenv('DEVELOPMENT')))