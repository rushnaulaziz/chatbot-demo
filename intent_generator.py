#!/usr/bin/python3
import argparse
import json
import os
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import random
import itertools
from pre_defined_json import pre_defined_intents
from PyDictionary import PyDictionary
import time
ALLOWED_EXTENSIONS = {'xlsx'}
stopwords = ["included","what", "why","when", "will", "would","of", "or","and", "if","a","an","is", "am", \
            "are", "has","have", "does", "in", "the", "i", "me", "to", "tell", "about","with", "more", "want", "know", "?", "!"]
def parse_file(file_path, sheet_name1,question_column, response_column ):
    """
    Input file parser
    """
    import pandas as pd

    df = pd.read_excel (file_path, sheet_name=sheet_name1)
    questions = df[question_column]
    responses = df[response_column]
    data = list(zip(questions, responses))
    return data

def synonyms_gen(word):
    try:
        dictionary=PyDictionary()
        synonyms = dictionary.synonym(word)
        if synonyms:
            synonyms = [synonym for synonym in synonyms if len(synonym.split()) < 2]
            return synonyms 
        return [word]

    except:
        return [word]




def form_json(data, target):
    """
    Appends new pharses to basic intent structure
    """
    intents = []
    for intent in pre_defined_intents:
        intents.append(intent)


    for query, response in data:

        patter_tokens = word_tokenize(query.lower())
        patterns_without_sw = list(set([lemmatizer.lemmatize(word.lower()) for word in patter_tokens if not word in stopwords]))
        tag = "_".join(patterns_without_sw)

        response = response.splitlines()
        response = "<br/>".join(response)


        final_patterns = []

        for index, token in enumerate(patterns_without_sw):
            synonyms = synonyms_gen(token)
            for synonym in synonyms:
                new_phrase = patterns_without_sw.copy()
                new_phrase[index] = synonym
                new_pattern = " ".join(new_phrase)
                final_patterns.append(new_pattern)

        intent = {
            "tag": tag,
            "patterns": final_patterns,
            "responses": [response],
            "context": []
        }

        intents.append(intent)


    json_data = {"intents":intents}
    with open(target, 'w') as resfl:
        json.dump(json_data, resfl,  indent = 5)
        resfl.close()


def intent_progress_estimate(file_path,socketio, sheet_name,question_column, response_column, stop):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name,question_column, response_column)

        questions_count = len(fileContent)
        time_for_a_single_question = 10
        total_etsimated_time = questions_count * time_for_a_single_question
        
        start_time1 = time.time()
        while True:
            time.sleep(2)
            time_spent_till_now = time.time() - start_time1
            progress = int((time_spent_till_now/total_etsimated_time)*100) 
            socketio.emit('message', progress)
            print(f"--- progress : {progress} % ---")

            if stop():
                progress = 100
                socketio.emit('message', progress)
                print(f"--- progress : {progress} % ---")
                break
    else:
        print('File {fp} not found'.format(fp=file_path)) 
     

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def intent_generator_function(file_path, sheet_name, json_path,question_column, response_colum ):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name,question_column, response_colum )
        if not os.path.exists(json_path):
            form_json(fileContent, json_path)
        else:
            print('File {fp} already exists.'.format(fp=json_path))
            prompt = "yes"
            if prompt.strip().casefold() in {'y', 'yes'}:
                form_json(fileContent, json_path)
            else:
                exit(0)
    else:
        print('File {fp} not found'.format(fp=file_path))

if __name__ == '__main__':
    file_path = './data.xlsx'
    sheet_name = "Sheet2"
    json_path =  "./intents.json"