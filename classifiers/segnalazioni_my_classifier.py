import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


#from sklearn.ensemble import RandomForestClassifier

#stemming
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

import pickle
import seaborn as sns
import pprint
from collections import Counter

def preprocess(txt):
	txt = txt.replace("?", " ")
	txt = txt.replace("!", " ")
	txt = txt.replace("'", " ")
	txt = txt.replace(".", " ")
	txt = txt.replace(",", " ")
	txt = txt.replace("<br />", " ")
	txt = txt.replace("\\n", " ")
	txt = txt.replace("</td>", " ")
	txt = txt.replace("<td>", " ")
	
	tmp = ''
	
	
	for ch in txt:
		if ch in (' ') or \
		(ord(ch) >= 65 and ord(ch) <= 90) or \
		(ord(ch) >= 97 and ord(ch) <= 122) or \
		0:
			tmp += ch
	sno = SnowballStemmer('italian')
	tokens = [sno.stem(t) for t in tmp.lower().split() if len(t) > 3]
	#print(tokens)
	

	return ' '.join(tokens).strip()
	
	
def remove_unfrequent(txt,dic):
	tokens = [t for t in txt.lower().split() if t in dic]
	
	return ' '.join(tokens).strip()
	

data = pd.read_csv('processed_dataset.csv',low_memory=False) 
#data = pd.read_csv('dataset.csv',low_memory=False) 

X = data["text"]
y = data["infoclass"]

#print(X.shape)
#print(X.head(10))
# remove short words and lowercasing

X = X.apply(lambda x: preprocess(x))



# lista delle classi ordinata in ordine alfabetico
# serve per confronto con clf.predict_proba  che le restituisce in ordine alfabetico ( qua non è usato)

ordered_class_list = list(set(y))
ordered_class_list.sort()


print("#"*100+ "\nTEST SPLIT")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
print (X_train.shape, y_train.shape)
print (X_test.shape, y_test.shape)

print(X_train.head(10),y_train.head(10))

print(X_test.head(10),y_test.head(10))


"""
RIMUOVERE PAROLE POCO FREQUENTI

array=[]
for row in X_train:
	array += row.split()
	#print(array)
	
d = Counter(array)
word = []
for key, value in d.items():
	if value>5:
		print(key,value)
		word.append(key)
	#print(key,value)

X_train = X_train.apply(lambda x: remove_unfrequent(x, word))
"""


# convert x_train to vectorized text
vectorizer_train = CountVectorizer(min_df=0)
vectorizer_train.fit(X_train)   #salvo dentro vectorized_train i token del traintest

x_train_array = vectorizer_train.transform(X_train).toarray() 
#converto le stringhe in un array di 0 o 1 a seconda che la parola corrispondente nella lista dei token sia presente
x_test_array = vectorizer_train.transform(X_test).toarray()


print ("VECTOR TOKENS")
#print (vectorizer_train.get_feature_names())
print("number of tokens: ", len(vectorizer_train.get_feature_names()))

#clf viene addestrato 
clf = MultinomialNB().fit(x_train_array, y_train)

# test on train set
predictions = clf.predict(x_test_array)
print(predictions)

s = accuracy_score(y_test, predictions)
print(s)

"""
#RANDOM FOREST ALGORITHM
precision: 0.792
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
rf.fit(x_train_array, y_train)

predicted = rf.predict(x_test_array)
accuracy = accuracy_score(y_test, predicted)
print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
print(f'Mean accuracy score: {accuracy:.3}')
"""


with open('nb_classifier.pickle', 'wb') as output:
    pickle.dump(clf, output, pickle.HIGHEST_PROTOCOL)
    
with open('nb_vectorizer.pickle', 'wb') as output:
    pickle.dump(vectorizer_train, output, pickle.HIGHEST_PROTOCOL)
    
    
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
#cnf_matrix = confusion_matrix(y_test, predictions)
#print(cnf_matrix)

print(pd.crosstab(y_test, predictions, rownames=['True'], colnames=['Predicted'], margins=True))
cm = pd.DataFrame(confusion_matrix(y_test, predictions), columns=ordered_class_list, index=ordered_class_list)
sns.heatmap(cm, annot=True)
