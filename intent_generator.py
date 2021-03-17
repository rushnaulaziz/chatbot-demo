#!/usr/bin/python3
import argparse
import json
import os
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import random
import itertools
from pre_defined_json import pre_defined_intents
from PyDictionary import PyDictionary
import time
import pandas as pd
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()


stopwords = ["included","what", "why","when", "will", "would","of", "or","and", "if","a","an","is", "am", \
            "are",",", "has","have", "does", "in", "the", "i", "me", "to", "tell", "about","with", "more", "want", "know", "?", "!"]

# def parse_file(file_path, sheet_name1,question_column, response_column, Context_parent_coloumn = "Context_parent", Context_child_coloumn = "Context_child"):
#     """
#     Input file parser
#     """

#     df = pd.read_excel (file_path, sheet_name=sheet_name1)
#     questions = df[question_column]
#     responses = df[response_column]

#     Context_set = df[Context_parent_coloumn]
#     Context_filter = df[Context_child_coloumn]
#     data = list(zip(questions, responses, Context_set, Context_filter))
#     return data

def parse_file(file_path, sheet_name1,question_column, response_column):
    """
    Input file parser
    """

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




def form_json(socketio,data, target, trainingType):
    """
    Appends new pharses to basic intent structure
    """

    intents = []

    # if training type is append load existing intent file data
    if(trainingType == 'APPEND'):
        with open(target, 'r') as resfl:
            intents = json.load(resfl)['intents']

    # if training type is replace load new intents data
    else:    
        for intent in pre_defined_intents:
            intents.append(intent)

    
    # initialize new dictionary with key as intents.tag
    intentsDict = {x['tag']:x for x in intents}            

    num =  int(90 / len(data))
    count = 0
    # for query, response, Context_set, Context_filter in data: 
    for query, response in data: 

        count+=num
        socketio.emit('message', count)
        
        patter_tokens = word_tokenize(query.lower())
        patterns_without_sw = sorted(list(set([lemmatizer.lemmatize(word.lower()) for word in patter_tokens if not word in stopwords])))
        tag = "_".join(patterns_without_sw)

        # dont search for synonym if tag is already in intents.json 
        if tag not in intentsDict.keys():
            final_patterns = []
            response = response.splitlines()
            response = "<br/>".join(response)
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

            intentsDict[tag]=intent


    json_data = {"intents":[val for val in intentsDict.values()]}
    with open(target, 'w') as resfl:
        json.dump(json_data, resfl,  indent = 2)
        resfl.close()


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xlsx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def intent_generator_function(socketio, file_path, sheet_name, json_path,question_column, response_colum, training_type ):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name,question_column, response_colum)
        if not os.path.exists(json_path):
            form_json(socketio,fileContent, json_path, training_type)
        else:
            print('File {fp} already exists.'.format(fp=json_path))
            prompt = "yes"
            if prompt.strip().casefold() in {'y', 'yes'}:
                form_json(socketio,fileContent, json_path, training_type)
            else:
                exit(0)
    else:
        print('File {fp} not found'.format(fp=file_path))

def getargs():
    usage_message = """excel_tuning.py [--file] -f file  [--sheet] -s sheetname [--qcol] -q questioncolumn [--rcol] -r responsecolumn"""
    parser = ArgumentParser(conflict_handler='resolve', usage=usage_message)
    parser.add_argument('-f', '--file', action='store', type=str, required=True)
    parser.add_argument('-s', '--sheet', action='store', type=str, required=True)
    parser.add_argument('-q', '--qcol', action='store', type=str, required=True)
    parser.add_argument('-r', '--rcol', action='store', type=str, required=True)
    parser.add_argument('-j', '--jsonpath', action='store', type=str, required=True)
    return parser.parse_args()

# if __name__ == '__main__':
    # args = getargs()
    # file_path = args.file
    # sheet_name = args.sheet
    # json_path = args.jsonpath
    
    # file_path = './data.xlsx'
    # sheet_name = "Sheet2"
    # json_path =  "./intents.json"
    # question_column = "Input"
    # response_colum = "Chatbot Response"

    # intent_generator_function(socketio, file_path, sheet_name, json_path, question_column, response_colum )
    
    
    
    # fileContent = parse_file(file_path,sheet_name)
    # print(fileContent[0])
    # for query, response, Context_set, Context_filter in fileContent: 
    #     # if Context_set != None:
    #     print(str(Context_set))
