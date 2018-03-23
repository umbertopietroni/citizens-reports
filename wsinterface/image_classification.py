import sys
import os
import pprint
import pickle
sys.path.insert(0, '../dbinterface/')
from classes import *

import pandas as pd
from pandas.core.series import Series

import clarifai_interface

def predict_image(filename):

	if not os.path.isfile(filename):
		exit("Error: File {} does not exist".format(filename))
		

	
	issueimage = IssueImage(filename)

	apikey = open('../wsinterface/apikey.txt', 'r').read().replace("\r", "").replace("\n", "")

	print("...using apikey '{}'".format(apikey))
	classification_dict = clarifai_interface.clarifai_prediction(issueimage, apikey=apikey)
	
	#pprint.pprint(classification_dict)
	
	#ii.setClassificationDict(classification_dict)

	# we could use only tokens associated to concepts with high values...
	
	#prendo i token della classificazione per immagini e li uso dentro il nostro classificatore
	tokens = [elem['name'] for elem in classification_dict['outputs'][0]['data']['concepts']]
	
	s = Series(' '.join(tokens))
	print("String representation of s:", str(s))

	# load classifier from pickle object
	with open('../classifiers/nb_classifier.pickle', 'rb') as handle:
		clf = pickle.load(handle)
		
	# load vectorizer from pickle object
	with open('../classifiers/nb_vectorizer.pickle', 'rb') as handle:
		vectorizer = pickle.load(handle)

	# transform s into an array with thr trained vectorizer
	v = vectorizer.transform(s).toarray()
	prediction = clf.predict(v)
	print("Predicted class: ", prediction)
	
	class_probabilities = clf.predict_proba(v)[0]
	print("Class probabilities:", class_probabilities)
	
	return prediction,class_probabilities
