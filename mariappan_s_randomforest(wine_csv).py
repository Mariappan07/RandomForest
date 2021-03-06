# -*- coding: utf-8 -*-
"""Mariappan s -Randomforest(wine.csv)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BaC9aBI8esbv4ygoXgI4sZ4DX2F2LFgB
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
#from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.naive_bayes import GaussianNB
#from sklearn.metrics import roc_curve
#from sklearn.metrics import roc_auc_score
#from sklearn.metrics import auc

# reading the data
data = pd.read_csv("/content/drive/MyDrive/0.MKCE/5.Random Forest/3 Take-Home Assignment/wine.csv")

# displaying the data
data

# VISUALIZE THE FIRST 10 ROWS OF THE DATA SET
data[:10]

#CHECK THE SHAPE OF THE DATA SET
data.shape

#SHOW THE DISTRIBUTION OF THE DATA COLUMNS
fig=data.hist(figsize=(10,10),color='lightblue')
plt.show()

#GENERATE THE CORRELATION MATRIX
data.corr()

#Visualize whether any attributes are related to the target variable
data.corr()['quality']

#Generate a pairplot for the data
sns.pairplot(data)

#Generate a count plot for the target variable (quality)
sns.countplot(x='quality',data=data)

#Converting the target variable 'Quality' to categorical, such that
#Wines having the “Quality” value > 6.5 are assigned value 1, and
#Wines having the “Quality” value < 6.5, are assigned value 0
#Where 0: Ordinary Quality of wine and 1: High quality of wine
quality=data['quality']
values=[]
for k in quality:
  if(k<6.5):
    j='Ordinary Quality of Wine'
    values.append(j)
  elif(k>6.5):
    j='High Quality of Wine'
    values.append(j)
values

#creating a dataframe for the columns
k=pd.DataFrame(values)
data['Wine_Quality']=k
data

# Random Forest classifier, to predict whether a particular wine is ordinary or of high quality. 
# Perform Hyperparameter Tuning to improve the accuracy of the model
data.columns

data.info()

#creating the dummies for the data
data2=pd.get_dummies(data)

#checking the columns
data2.columns

#droping the columns
data2.drop(['Wine_Quality_High Quality of Wine','Wine_Quality_Ordinary Quality of Wine'],axis=1)

data2

# taking a column from x and placing it in y for training the model
x = data2.drop(['quality'],axis=1)
y = data2['quality']

#training the model 
x_train,x_test,y_train,y_test = train_test_split(x,y, test_size=0.2, random_state=0)

print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

#fitting the data to the model
model = RandomForestClassifier()
model.fit(x_train,y_train)

#predicting the model
pre = model.predict(x_test)
model.predict_proba(x_test)

x_test

#accuracy of the model
accuracy_score(y_test,pre)

#confusion matrix of the model
confusion_matrix(y_test,pre)

#classification report 
z = classification_report(y_test,pre)
print(z)

# creating the GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn import decomposition, datasets
from sklearn import tree
from sklearn import ensemble
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
pca = decomposition.PCA()
randomforest= ensemble.RandomForestClassifier()

#creating the pipelines
pipe = Pipeline(steps =[('sc',sc),
                        ('pca',pca),
                        ('randomforest',randomforest)])

#setting up the range for the pipelines
n_components = list(range(1,x.shape[1]+1,1))

criterion = ['gini', 'entropy']
max_depth = [2,4,6,8]

parameters = dict(pca__n_components=n_components,
                 randomforest__criterion=criterion,
                 randomforest__max_depth=max_depth)

clf = GridSearchCV(pipe, parameters)

clf.fit(x,y)

print('Best Criterion:',clf.best_estimator_.get_params()['randomforest__criterion'])

print('Best max_depth:',clf.best_estimator_.get_params()['randomforest__max_depth'])

print('Best No.of components:',clf.best_estimator_.get_params()['pca__n_components'])

print(clf.best_estimator_.get_params()['randomforest'])

CV_result=cross_val_score(clf,x,y,cv=4, n_jobs=-1)

print(CV_result)
print(CV_result.mean())
print(CV_result.std())