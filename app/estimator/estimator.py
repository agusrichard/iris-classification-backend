# Essentials
import pickle
import os
import pandas as pd 
import numpy as np
from flask import current_app
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def create_estimator():
    # Load the data
    dataset_path = os.path.join(current_app.root_path, 'static/estimator/iris.csv')
    df = pd.read_csv(dataset_path)
    X = df.iloc[:, 0:-1].values
    y = df['variety'].replace({'Setosa': 0, 'Versicolor': 1, 'Virginica': 2}).values

    # Split it to training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

    # Initialize the estimator and train it
    model = RandomForestClassifier().fit(X_train, y_train)

    # Test set score evaluation
    score = model.score(X_test, y_test)
    print("Score on test set: ", score)

    # Estimator using all dataset
    model = RandomForestClassifier().fit(X, y)

    # Save the model
    estimator_path = os.path.join(current_app.root_path, 'static/estimator/finalized_model.sav')
    pickle.dump(model, open(estimator_path, 'wb'))