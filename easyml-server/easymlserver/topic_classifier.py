import unicodedata
import numpy as np
import sys
from time import time
from nltk.probability import FreqDist
from nltk.classify import SklearnClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from nltk.util import bigrams
from nltk.util import ngrams
import web
import cPickle
import csv

all_topics = ['Topic1','Topic2','Topic3']

pipeline = Pipeline([('tfidf', TfidfTransformer()),
                     ('chi2', SelectKBest(chi2, k=500)),
                     ('nb', MultinomialNB())])

classif = SklearnClassifier(pipeline)


def benchmark(clf):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    if hasattr(clf, 'coef_'):
        print("dimensionality: %d" % clf.coef_.shape[1])
        print("density: %f" % density(clf.coef_))

        if feature_names is not None:
            print("top 10 keywords per class:")
            for i, category in enumerate(categories):
                print str(i)+' '+category
                top10 = np.argsort(clf.coef_[i])[-10:]
                print(trim("%d %s: %s"
                      % (i, category, " ".join(feature_names[top10]))))
        print()

    if True:
        print("classification report:")
        print(metrics.classification_report(y_test, pred,
                                            target_names=categories))

    if opts.print_cm:
        print("confusion matrix:")
        print(metrics.confusion_matrix(y_test, pred))

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time


def get_training_data():
    global data_train_data,data_test_data,data_train_target,data_test_target,categories
    training_set = {}
    docs = {}
    topic_list = all_topics
    topics = []
    import app_search
    for topic in topic_list:
        #topic = t['name']
        topics.append(topic)
        print topic
        results = app_search.search_text(topic,type='links',exact=True,results=250)
        docs[topic] = results
        print len(results)
        dists = []
        for r in results:
            dists.append(process_document_text(r))
            
        training_set[topic] = dists
    
    add_label = lambda lst, lab: [(x, lab) for x in lst]
    data_train_data = []
    data_train_target = []
    #labelled = []
    categories = []
    for topic in topics:
        print 'Training '+topic+' from: '+str(len(training_set[topic]))+' results'
        if len(training_set[topic])>9:
            #labelled = labelled + add_label(training_set[topic], topic)
            data_train_data = data_train_data + training_set[topic]
            topic_list = len(training_set[topic])*[topic]
            data_train_target = data_train_target + topic_list
            if not topic in categories:
                categories.append(topic)
        else:
            print "Skipping topic: "+topic
    categories = sorted(categories)
    #use training set as test set for now
    data_test_data = data_train_data
    data_test_target = data_train_target
    joblib.dump(data_train_target, 'data_train_target.pkl', compress=9)
    joblib.dump(data_train_data, 'data_train_data.pkl', compress=9)
    joblib.dump(categories, 'categories.pkl', compress=9)

def classify_probabilistic(doc):
    docs_vectorized = vectorizer.transform([doc])
    docs_vectorized = ch2.transform(docs_vectorized)
    #print clf.predict(docs_vectorized)#decision_function(docs_vectorized)
    df = clf.decision_function(docs_vectorized)
    zipped = zip(categories,df[0])
    zipped.sort(key = lambda t: t[1],reverse=True)
    return [z[0] for z in zipped[0:3]]

def do_training():
    global X_train, X_test, feature_names, ch2
    print("Extracting features from the training data using a sparse vectorizer")
    t0 = time()
    if opts.use_hashing:
        vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                       n_features=opts.n_features)
        X_train = vectorizer.transform(data_train_data)
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.25,
                                     stop_words='english')
        X_train = vectorizer.fit_transform(data_train_data)
    duration = time() - t0
    #print("done in %fs at %0.3fMB/s" % (duration, data_train_size_mb / duration))
    print("n_samples: %d, n_features: %d" % X_train.shape)
    print()

    print("Extracting features from the test data using the same vectorizer")
    t0 = time()
    X_test = vectorizer.transform(data_test_data)
    duration = time() - t0
    #print("done in %fs at %0.3fMB/s" % (duration, data_test_size_mb / duration))
    print("n_samples: %d, n_features: %d" % X_test.shape)
    print()

    # mapping from integer feature name to original token string
    if opts.use_hashing:
        feature_names = None
    else:
        feature_names = vectorizer.get_feature_names()

    if True:#opts.select_chi2:
        print("Extracting %d best features by a chi-squared test" % 20000)
        t0 = time()
        ch2 = SelectKBest(chi2, k=20000)
        X_train = ch2.fit_transform(X_train, y_train)
        X_test = ch2.transform(X_test)
        if feature_names:
            # keep selected feature names
            feature_names = [feature_names[i] for i
                             in ch2.get_support(indices=True)]
        print("done in %fs" % (time() - t0))
        print()
    
    if feature_names:
        feature_names = np.asarray(feature_names)

    results = []

    #for penalty in ["l2", "l1"]:
    penalty = 'l2'
    print('=' * 80)
    print("%s penalty" % penalty.upper())
    # Train Liblinear model
    clf = LinearSVC(loss='l2', penalty=penalty,dual=False, tol=1e-3)
    results.append(benchmark(clf))
        
    joblib.dump(vectorizer, 'vectorizer.pkl', compress=9)
    joblib.dump(ch2, 'feature_selector.pkl', compress=9)
    joblib.dump(clf, 'linearsvc_classifier.pkl', compress=9)



# parse commandline arguments

if __name__=='__main__':
    pass
