import os
import pickle

path = os.path.join(os.path.abspath('./app'), 'static/estimator/finalized_model.sav')
model = pickle.load(open(path, 'rb'))

def make_prediction(x):
	prediction = model.predict(x)
	if prediction == 0:
		return "Iris Setosa"
	elif prediction == 1:
		return "Iris Versicolor"
	else:
		return "Iris Virginica"