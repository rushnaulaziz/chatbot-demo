#!/usr/bin/env python
 
import argparse
import nltk
from argparse import ArgumentParser
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import random

def train(file_path):
    """Trains the chatbot on intent file"""
    """
    Args:
    Json file path: File should have json in the following format
    {
     "intents": [
          {
               "tag": "string",
               "patterns": ["string"],
               "responses": ["string"],
               "context": ["string"]
          }
        ]
    }
    """
    words=[]
    classes = []
    documents = []
    ignore_words = ['?', '!']
    data_file = open(file_path).read()
    intents = json.loads(data_file)


    for intent in intents['intents']:
        for pattern in intent['patterns']:

            #tokenize each word
            """
            Tokenization is the process by which a large quantity of text is divided into smaller parts called tokens.
            These tokens are very useful for finding patterns and are considered as a base step for stemming and lemmatization. 
            """
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            #add documents in the corpus
            documents.append((w, intent['tag']))

            # add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # lemmaztize and lower each word and remove duplicates
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    # sort classes
    classes = sorted(list(set(classes)))
    # documents = combination between patterns and tags
    print (len(documents), "documents")
    # classes = intents
    print (len(classes), "classes", classes)
    # words = all words, vocabulary
    print (len(words), "unique lemmatized words", words)


    pickle.dump(words, open('words.pkl','wb'))
    pickle.dump(classes, open('classes.pkl','wb'))

    # create our training data
    training = []
    # create an empty array for our output
    output_empty = [0] * len(classes)
    # training set, bag of words for each sentence
    for doc in documents:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # lemmatize each word - create base word, in attempt to represent related words
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        # create our bag of words array with 1, if word match found in current pattern
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
        
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        
        training.append([bag, output_row])
    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # create train and test lists. X - patterns, Y - intents
    train_x = list(training[:,0])
    train_y = list(training[:,1])
    print("Training data created")


    # Create model - 3 layers.
    model = Sequential()

    # First layer 128 neurons (a classification layer with relu as activation).
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu', name="layer1"))
    model.add(Dropout(0.5))

    # second layer 64 neurons (a classification layer with relu as activation)
    model.add(Dense(64, activation='relu', name="layer2"))
    model.add(Dropout(0.5))

    # 3rd output layer contains number of neurons equal to number of intents
    #  to predict output intent with softmax (a classification layer with softmax as activation.
    model.add(Dense(len(train_y[0]), activation='softmax', name="layer3"))

    model.summary()

    # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    #fitting and saving the model 
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    model.save('chatbot_model.h5', hist)

def getargs():
    usage_message = """train.py [--file] -f file"""
    parser = ArgumentParser(conflict_handler='resolve', usage=usage_message)
    parser.add_argument('-f', '--file', action='store', type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = getargs()
    train(args.file)