import numpy as np
import pandas as pd
import sys
print sys.path
from sklearn import preprocessing
from sklearn import linear_model
from sklearn.grid_search import GridSearchCV
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from modeldb.sklearn_native.ModelDbSyncer import *
from modeldb.sklearn_native import SyncableMetrics

#This is a sample usage of GridSearch in scikit, adapted from http://scikit-learn.org/stable/auto_examples/model_selection/grid_search_digits.html
name = "grid search"
author = "srinidhi"
description = "digits dataset"
SyncerObj = Syncer(
    NewOrExistingProject(name, author, description),
    DefaultExperiment(),
    NewExperimentRun("Abc"))

# Loading the Digits dataset
digits = datasets.load_digits()

# To apply an classifier on this data, we need to flatten the image, to
# turn the data in a (samples, feature) matrix:
n_samples = len(digits.images)
X = digits.images.reshape((n_samples, -1))
y = digits.target

# Split the dataset in two equal parts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=0)

# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5)
clf.fitSync(X_train, y_train)

print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")

SyncableMetrics.computeMetrics(clf, "precision", X_test, "", "",y_test)

Syncer.instance.sync()