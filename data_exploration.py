'''
Questions
- What are the correlations of the variables? (correlation matrix/ pairsplot)
- What are the mean prices for different groups of offers?
-
'''



#import packages
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
import numpy as np
import re
import seaborn
import datetime


import copy


#read data
df_cars = pd.read_hdf('data/cars_cleaned.h5', mode='r')
df_cars.head()
##create numeric feature with ange
df_cars['age_in_days'] = df_cars.build.apply(lambda x: (datetime.datetime.today() - x).days)


df_for_pairsplot = df_cars.loc[:,['price',
                                'horsepower',
                                'kilometers',
                                'age_in_days',
                                'body_shape']]
body_shapes = df_cars.body_shape.unique()

fig_pairs = seaborn.pairplot(df_for_pairsplot, hue='body_shape',
                         hue_order=body_shapes,
                         vars= df_for_pairsplot.drop(['body_shape'],axis = 1).columns.values,
                         plot_kws={'alpha': .3},
                         diag_kind = 'reg')
#fig_pairs.savefig("Figures_high_def/CFA_pairsplot_clusters.png", dpi=1000)



df_cars.columns
X = df_cars[['build','horsepower','kilometers','owners']]
X.loc[:,'build'] = pd.to_numeric(X.build)
y = df_cars[['price']]




from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics
from sklearn.metrics import r2_score
from adspy_shared_utilities import plot_decision_tree
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y, random_state = 1)
clf = DecisionTreeClassifier().fit(X_train, y_train)

print('R2 of Decision Tree classifier on training set: {:.2f}'
     .format(r2_score(clf.predict(X_train),y_train)))
print('R2 of Decision Tree classifier on test set: {:.2f}'
     .format(r2_score(clf.predict(X_test),y_test)))

clf2 = DecisionTreeClassifier(max_depth = 15).fit(X_train, y_train)

print('R2 of Decision Tree classifier on training set: {:.2f}'
     .format(r2_score(clf2.predict(X_train),y_train)))
print('R2 of Decision Tree classifier on test set: {:.2f}'
     .format(r2_score(clf2.predict(X_test),y_test)))

tree.export_graphviz(clf2,out_file='tree.dot',impurity = False, filled = True, 
                    label = None)
!dot -Tpng tree.dot -o tree.png


iris = load_iris()

X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state = 3)
clf = DecisionTreeClassifier().fit(X_train, y_train)

print('Accuracy of Decision Tree classifier on training set: {:.2f}'
     .format(clf.score(X_train, y_train)))
print('Accuracy of Decision Tree classifier on test set: {:.2f}'
     .format(clf.score(X_test, y_test)))

clf2 = DecisionTreeClassifier(max_depth = 3).fit(X_train, y_train)

print('Accuracy of Decision Tree classifier on training set: {:.2f}'
     .format(clf2.score(X_train, y_train)))
print('Accuracy of Decision Tree classifier on test set: {:.2f}'
     .format(clf2.score(X_test, y_test)))








type(iris.feature_names)
type(iris.target_names)
