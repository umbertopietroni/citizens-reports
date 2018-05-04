import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score,precision_score,recall_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict


# from sklearn.ensemble import RandomForestClassifier



import pickle
import seaborn as sns
import pprint
from collections import Counter

data = pd.read_csv('second_dataset.csv', low_memory=False)
# data = pd.read_csv('dataset.csv',low_memory=False)

X = data.iloc[:,0:8]
y = data["infoclass"]


#X = X.apply(lambda x: preprocess(x))


ordered_class_list = list(set(y))
ordered_class_list.sort()

print("#" * 100 + "\nTEST SPLIT")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
print (X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

print(X_train.head(10), y_train.head(10))

print(X_test.head(10), y_test.head(10))


# clf viene addestrato
clf = SVC().fit(X_train, y_train)
#SVM
# test on train set
predictions = clf.predict(X_test)


s = accuracy_score(y_test, predictions)
print("test accuracy score: " ,s)

#p = precision_score(y_test, predictions, average = None)
#print("test precision score: " ,p)

#r = recall_score(y_test, predictions, average = None)
#print("test recall score: " ,r)


with open('second_classifier.pickle', 'wb') as output:
	pickle.dump(clf, output, pickle.HIGHEST_PROTOCOL)


"""
A useful technique for visualising performance is the confusion matrix. 
This is simply a matrix whose diagonal values are true positive counts, 
while off-diagonal values are false positive and false negative counts 
for each class against the other.

The diagonal elements show the number of correct classifications for each class: 3, 1 and 3 for the classes 0, 1 and 2.
The off-diagonal elements provides the misclassifications: for example, 2 of the class 2 were misclassified as 0, none of the class 0 were misclassified as 2, etc.
The total number of classifications for each class in both y_true and y_pred, from the "All" subtotals

ON JUPYTER NOTEBOOK
"""
# confusion matrix
# cnf_matrix = confusion_matrix(y_test, predictions)
# print(cnf_matrix)

print(pd.crosstab(y_test, predictions, rownames=['True'], colnames=['Predicted'], margins=True))
cm = pd.DataFrame(confusion_matrix(y_test, predictions), columns=ordered_class_list, index=ordered_class_list)
sns.heatmap(cm, annot=True)
