import nltk
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()
from nltk.tokenize import word_tokenize
from keras.models import load_model

import numpy as np
import json
import random
import pickle


stopwords = ["what", "why","when", "will", "would","of", "or","and", "if","a","an","is", "am", "are", "has","have"]
# import types
# import tensorflow as tf
# if type(tf.contrib) != types.ModuleType:  # if it is LazyLoader
#     tf.contrib._warning = None


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, words, model, classes, ERROR_THRESHOLD):
    # generate probabilities from the model
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]

    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    # print(classes)
    if results:
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    else:
        return_list.append({"intent": classes[-1], "probability": "0"})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    print(tag)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg, trainCompleted):
    global model,intents,words,classes
    if trainCompleted:
        model = load_model('chatbot_model.h5')
        intents = json.loads(open('intents.json').read())
        words = pickle.load(open('words.pkl','rb'))
        classes = pickle.load(open('classes.pkl','rb'))
    
    text_tokens = word_tokenize(msg)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords]
    # print(tokens_without_sw)
    query_sentence = " ".join(tokens_without_sw)

    ERROR_THRESHOLD = 0.65
    results = predict_class(query_sentence, words,  model, classes, ERROR_THRESHOLD)

    res = getResponse(results, intents)
    return res

    # print(ints)

    # if results:
    #     # loop as long as there are matches to process
    #     while results:
    #         for i in intents['intents']:
    #             # find a tag matching the first result
    #             tag = results[0]['intent']
    #             # print(tag)
    #             # if show_details: print ('initial tag:', tag)

    #             if i['tag'] == tag:
    #                 result = random.choice(i['responses'])
    #                 break
    #             return result
                
    #                 # set context for this intent if necessary
    #                 if 'context_set' in i:
    #                     if show_details: print ('context:', i['context_set'])
    #                     context[userID] = i['context_set']

    #                 # check if this intent is contextual and applies to this user's conversation
    #                 if not 'context_filter' in i or \
    #                     (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
    #                     if show_details: print ('tag:', i['tag'])
    #                     # a random response from the intent
    #                     return random.choice(i['responses'])

    #         results.pop(0)


