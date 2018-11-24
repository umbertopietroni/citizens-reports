import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

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
    # print(tokens)

    return ' '.join(tokens).strip()


def predict_text(x):
    x = [preprocess(x)]
    with open('../classifiers/nb_classifier.pickle', 'rb') as handle:
        clf = pickle.load(handle)
    with open('../classifiers/nb_vectorizer.pickle', 'rb') as handle:
        vectorizer = pickle.load(handle)

    # transform s into an array with thr trained vectorizer
    v = vectorizer.transform(x).toarray()
    category = clf.predict(v)[0]
    categories = clf.predict_proba(v)[0]
    # print("Predicted class: Ambiente Illuminazione Manutenzione Sicurezza \n", clf.predict_proba(v)[0])
    return category, categories


def create_prob_dict(class_prob):
    dict_issue = {}
    dict_issue["ambiente"] = class_prob[0]
    dict_issue["illuminazione"] = class_prob[1]
    dict_issue["manutenzione"] = class_prob[2]
    dict_issue["sicurezza"] = class_prob[3]
    return dict_issue
