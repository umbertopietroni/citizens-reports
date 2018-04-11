import sys
import os
import pprint
import pickle
sys.path.insert(0, '../dbinterface/')
from classes import *

sys.path.insert(0, '../classifiers/')
from text_classification import *

import pandas as pd
from pandas.core.series import Series

import clarifai_interface

def predict_image(filename):

	if not os.path.isfile(filename):
		exit("Error: File {} does not exist".format(filename))
		

	
	issueimage = IssueImage(filename)

	apikey = open('../wsinterface/apikey.txt', 'r').read().replace("\r", "").replace("\n", "")
	
	classification_dict = clarifai_interface.clarifai_prediction(issueimage, apikey=apikey)
	
	

	# we could use only tokens associated to concepts with high values...
	
	#prendo i token della classificazione per immagini e li uso dentro il nostro classificatore
	tokens = [elem['name'] for elem in classification_dict['outputs'][0]['data']['concepts']]
	
	#s = Series(' '.join(tokens))
	s = ' '.join(tokens).strip()
	print("String representation of s:", str(s))
	"""
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
	
	"""
	prediction, class_probabilities = predict_text(s)
	
	return prediction,class_probabilities


#def create_prob_dict(class_prob):
	#dict_issue = {}
	#dict_issue["ambiente"] = class_prob[0]
	#dict_issue["illuminazione"] = class_prob[1]
	#dict_issue["manutenzione"] = class_prob[2]
	#dict_issue["sicurezza"] = class_prob[3]
	#return dict_issue
