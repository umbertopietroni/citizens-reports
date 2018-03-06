import sys
import os
import pprint
import pickle

import pandas as pd
from pandas.core.series import Series

from classes import *
from wsinterface import clarifai_interface

args = sys.argv
if len(args) < 2:
	print("Usage: python3 test_image_classification.py <file_path>")
	exit("\nExample: python3 test_image_classification.py /tmp/wood.jpg")
	
filename = args[1]

if not os.path.isfile(filename):
	exit("Error: File {} does not exist".format(filename))
	

issue = Issue()
issue.setInfo("phone_number", "3219876543")
try:
	issue.addImage("hello!")
except NameError as err:
	print("Oops. This is not correct!... : ", err)
issueimage = IssueImage(filename)

# this block is only to try the addImage, getImages and getFilename methods
issue.addImage(issueimage)
for ii in issue.getImages():
	print (ii.getFilename())
try:
	issue.setInfo("color", "red")
except NameError as err:
	print("Oops. This is not correct!... : ", err)
#####

print("Classifing...", issue.getInfo())

apikey = open('apikey.txt', 'r').read().replace("\r", "").replace("\n", "")
print("...using apikey '{}'".format(apikey))
classification_dict = clarifai_interface.clarifai_prediction(issueimage, apikey=apikey)
print("\nRESULTS:\n")
pprint.pprint(classification_dict)

print("save results into IssueImage object")
ii.setClassificationDict(classification_dict)

print("classification with nb_classifier")

# we could use only tokens associated to concepts with high values...
tokens = [elem['name'] for elem in classification_dict['outputs'][0]['data']['concepts']]
print("TOKENS = ", tokens)
s = Series(' '.join(tokens))
print("String representation of s:", str(s))

# load classifier from pickle object
with open('nb_classifier.pickle', 'rb') as handle:
	clf = pickle.load(handle)
	
# load vectorizer from pickle object
with open('nb_vectorizer.pickle', 'rb') as handle:
	vectorizer = pickle.load(handle)

# transform s into an array with thr trained vectorizer
v = vectorizer.transform(s).toarray()

print("Predicted class: ", clf.predict(v))

class_probabilities = clf.predict_proba(v)[0]
print("Class probabilities:", class_probabilities)
