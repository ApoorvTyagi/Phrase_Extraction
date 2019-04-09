from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def main_ML_model():
    data = pd.read_csv(('training_data.tsv'), header=0, delimiter="\t", quoting=3)

    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    data.loc[data['label'] != 'Not Found', 'label'] = 'Found'
    X = data['sent']
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, random_state=0)

    clean_train_data = []
    ###### prepareing the data for count vectoriser ######
    # print("Cleaning and parsing the training data...\n")
    for i in (X_train):
        clean_train_data.append(i)
    ###### Create a bag of words from the training set ######
    print("Creating the bag of words...\n")

    # initialize the count vectorizer to represent bag of words tool.
    
    vectorizer = CountVectorizer(ngram_range=(1, 2), lowercase='false')   # n-grams Bag of word

    train_data_features = vectorizer.fit_transform(clean_train_data)   # expects a list of strings

    np.asarray(train_data_features)   #Tfidf expects an array hence we convert it

    ###### representing the n-grams wrt to the frequency of occurence ######
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(train_data_features)

    ###### traing the stocastic gradient descent model ######
    clf = svm.LinearSVC(loss='hinge').fit(X_train_tfidf, y_train)
    mlp = MLPClassifier(activation='relu', solver='lbfgs').fit(X_train_tfidf, y_train)

    clean_test_data = []
    for i in X_test:
        clean_test_data.append(i)

    test_data_features = vectorizer.transform(clean_test_data)
    np.asarray(test_data_features)

    tfidf_transformer = TfidfTransformer()
    X_test_tfidf = tfidf_transformer.fit_transform(test_data_features)

    predict = clf.predict(X_test_tfidf)
    print("Accuracy with SVM is :" + str(accuracy_score(y_test, predict)))
    predict = mlp.predict(X_test_tfidf)
    print("Accuracy score with Multi Layer Perceptron: " + str(accuracy_score(y_test, predict)))

    import pickle
    f = open('svm_classifier.pickle', 'wb')
    pickle.dump(clf, f)
    f.close()

    f = open('mlp_classifier.pickle', 'wb')
    pickle.dump(mlp, f)
    f.close()

    f = open('my_vectorizer.pickle', 'wb')
    pickle.dump(vectorizer, f)
    f.close()
