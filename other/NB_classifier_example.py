import pandas as pd
import numpy as np


from io import StringIO

dataset = StringIO("""text,class
"sole mare caldo","estate"
"mare acqua","estate"
"freddo neve coperte","inverno"
"ghiaccio neve","inverno"
"foglie marrone vendemmia","autunno"
"fiori caldo picnic","primavera"
    """)

#data = pd.read_csv('dataset.csv',low_memory=False) 
data = pd.read_csv(dataset, sep=",")

print ("DATA SET")
print(data.head())
# print(data.shape)

X = data["text"]
y = data["class"]
from sklearn.feature_extraction.text import CountVectorizer


# lista delle classi ordinata in ordine alfabetico
ordered_class_list = list(set(y))
ordered_class_list.sort()


# convert x_train to vectorized text
vectorizer_train = CountVectorizer(min_df=0)
vectorizer_train.fit(X)
x_train_array = vectorizer_train.transform(X).toarray()

# print vectorized text, feature names
# print x_train_array
print ("VECTOR TOKENS")
print (vectorizer_train.get_feature_names())

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(x_train_array, y)
#print(clf)

msgs = ["sole mare",
		"foglie sole vendemmia",
		"freddo pioggia",
		"ghiaccio coperte",
		"fiori stelle picnic",
		]

for msg in msgs:
	print("\n\nMSG : ", msg)
	msg_array = vectorizer_train.transform([msg]).toarray()
	print("MSG tokens : ", msg.split())
	print("MSG array repr: ", msg_array)

	# calcolo confidence per classe
	# il risultato e' una lista di float in ordine alfabetico per classe
	class_probabilities = clf.predict_proba(msg_array)[0]

	class_confidence = list(zip(ordered_class_list, class_probabilities))
	for c in class_confidence:
		print ("{} : {:.3f} %".format(c[0].ljust(10), c[1]))

	r = clf.predict(msg_array)
	print("PREDICTED CLASS :", r[0])

