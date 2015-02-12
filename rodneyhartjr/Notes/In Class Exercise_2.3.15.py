# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import division

import numpy
import sqlite3
import pandas
from sklearn.neighbors import KNeighborsClassifier

cross_validation_amount = .2

conn = sqlite3.connect('/Users/admin/documents/SQLite/lahman2013.sqlite')

sql = 'SELECT playerID, ballots, votes, inducted FROM HallofFame WHERE yearID <2000;'

df = pandas.read_sql(sql, conn)

conn.close()

df.dropna(inplace = True)

df['percent_of_ballots'] = df.votes / df.ballots
df.head()

response_series = df.inducted
explanatory_variables = df[['ballots','votes','percent_of_ballots']]

holdout_num = round(len(df.index) * cross_validation_amount, 0)

test_indices = numpy.random.choice(df.index, holdout_num, replace = False)

train_indices = df.index[~df.index.isin(test_indices)]

response_train = response_series.ix[train_indices,]
explanatory_train = explanatory_variables.ix[train_indices,]

response_test = response_series.ix[test_indices,]
explanatory_test = explanatory_variables.ix[test_indices,]

KNN_classifier = KNeighborsClassifier(n_neighbors=3, p = 2)

KNN_classifier.fit(explanatory_train, response_train)

predicted_response = KNN_classifier.predict(explanatory_test)

number_correct = len(response_test[response_test == predicted_response])
total_in_test_set = len(response_test)
accuracy = number_correct / total_in_test_set
print accuracy * 100

# Class Exercise 2

test_indices = numpy.random.choice(df.index, holdout_num, replace = False)
train_indices = df.index[~df.index.isin(test_indices)]

response_train = response_series.ix[train_indices,]
explanatory_train = explanatory_variables.ix[train_indices,]
response_test = response_series.ix[test_indices,]
explanatory_test = explanatory_variables.ix[test_indices,]

KNN_classifier = KNeighborsClassifier(n_neighbors=3, p = 2)
KNN_classifier.fit(explanatory_train, response_train)

predicted_response = KNN_classifier.predict(explanatory_test)
number_correct = len(response_test[response_test == predicted_response])
total_in_test_set = len(response_test)
new_accuracy = number_correct / total_in_test_set
print new_accuracy * 100

# 10 fold cross validation

from sklearn.cross_validation import cross_val_score
KNN_classifier = KNeighborsClassifier(n_neighbors=3, p = 2)

scores = cross_val_score(KNN_classifier, explanatory_variables, response_series, cv=10, scoring='accuracy')
print scores

mean_accuracy = numpy.mean(scores)
print mean_accuracy * 100
print new_accuracy * 100
print accuracy * 100


k_range = range(1, 30, 2)
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k, p = 2)
    scores.append(numpy.mean(cross_val_score(knn, explanatory_variables, response_series, cv=10, scoring='accuracy')))

import matplotlib.pyplot as plt
plt.figure()
plt.plot(k_range, scores)

from sklearn.grid_search import GridSearchCV
knn = KNeighborsClassifier(p = 2)
k_range = range (1, 30, 2)
param_grid = dict(n_neighbors=k_range)
grid = GridSearchCV(knn, param_grid, cv=10, scoring='accuracy')
grid.fit(explanatory_variables, response_series)

grid.grid_scores_
grid_mean_scores = [result[1] for result in grid.grid_scores_]
plt.figure()
plt.plot(k_range, grid_mean_scores)
best_oob_score = grid.best_score_
grid.best_params_
Knn_optimal = grid.best_estimator_


# pull in data from 2000 onwards

conn = sqlite3.connect('/Users/admin/documents/SQLite/lahman2013.sqlite')

sql = 'SELECT playerID, ballots, votes, inducted FROM HallofFame WHERE yearID >=2000;'
df = pandas.read_sql(sql, conn)

conn.close()

df.dropna(inplace = True)

df['percent_of_ballots'] = df.votes / df.ballots
df.head()

response_series = df.inducted
explanatory_variables = df[['ballots','votes','percent_of_ballots']]

optimal_knn_preds = Knn_optimal.predict(explanatory_variables)

number_correct = len(response_series[response_series == optimal_knn_preds])
total_in_test_set = len(response_series)
accuracy = number_correct / total_in_test_set

print accuracy * 100
print best_oob_score


