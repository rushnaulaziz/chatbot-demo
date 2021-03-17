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




def form_json(socketio, data, target):
    """
    Appends new pharses to basic intent structure
    """
    intents = []
    for intent in pre_defined_intents:
        intents.append(intent)

    num =  int(90 / len(data))
    count = 0
    # for query, response, Context_set, Context_filter in data: 
    for query, response in data: 

        count+=num
        socketio.emit('message', count)
        
        pattern_tokens = word_tokenize(query.lower())
        patterns_without_sw = list(set([word for word in pattern_tokens if not word in stopwords]))
        # print(patterns_without_sw)

        tag = "_".join(patterns_without_sw)

        same_queries = query.splitlines()
        final_patterns = []
        for query in same_queries:
            pattern_tokens = word_tokenize(query.lower())
            unique_pattern_tokens = dict.fromkeys(pattern_tokens)
            pattern_without_sw = [word for word in unique_pattern_tokens if not word in stopwords]
            query_processed = " ".join(pattern_without_sw)
            if query_processed:
                final_patterns.append(query_processed)


        response = response.splitlines()
        response = "<br/>".join(response)



        # patterns = [" ".join(subset) for L in range(0, len(patterns_without_sw)+1) for subset in itertools.combinations(patterns_without_sw, L) if subset]
        # final_patterns = [" ".join(subset) for L in range(2, len(patterns_without_sw)+1) for subset in itertools.combinations(patterns_without_sw, L) if subset]

        # patterns = []
        # patterns.append(patterns_without_sw)
        # for token in patterns_without_sw:
        #     new = random.sample(patterns_without_sw, len(patterns_without_sw))
        #     pattern = (" ".join(new))
        #     patterns.append(pattern)

        # final_patterns = []
        # for index, token in enumerate(patterns_without_sw):
        #     synonyms = synonyms_gen(token)
        #     for synonym in synonyms:
        #         new_phrase = patterns_without_sw.copy()
        #         new_phrase[index] = synonym
        #         new_pattern = " ".join(new_phrase)
        #         # print(new_pattern)
        #         final_patterns.append(new_pattern)

        print(final_patterns)
        # if Context_set:
        intent = {
            "tag": tag,
            "patterns": final_patterns,
            "responses": [response]
        }

        # if str(Context_set) != 'nan':
        #         intent["Context_set"] = Context_set
        
        # if str(Context_filter) != 'nan':
        #         intent["Context_filter"] = Context_filter

        intents.append(intent)


    json_data = {"intents":intents}
    with open(target, 'w') as resfl:
        json.dump(json_data, resfl,  indent = 2)
        resfl.close()


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xlsx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def intent_generator_function(socketio, file_path, sheet_name, json_path,question_column, response_colum ):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name,question_column, response_colum )
        if not os.path.exists(json_path):
            form_json(socketio,fileContent, json_path)
        else:
            print('File {fp} already exists.'.format(fp=json_path))
            prompt = "yes"
            if prompt.strip().casefold() in {'y', 'yes'}:
                form_json(socketio,fileContent, json_path)
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
    # intent_generator_function(socketio, file_path, sheet_name, json_path,question_column, response_colum )
    
    
    
    # fileContent = parse_file(file_path,sheet_name)
    # print(fileContent[0])
    # for query, response, Context_set, Context_filter in fileContent: 
    #     # if Context_set != None:
    #     print(str(Context_set))
