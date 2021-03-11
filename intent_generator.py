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
stopwords = ["included","what", "why","when", "will", "would","of", "or","and", "if","a","an","is", "am", \
            "are", "has","have", "does", "in", "the", "i", "me", "to", "tell", "about","with", "more", "want", "know", "?", "!"]
def parse_file(file_path, sheet_name1):
    """
    Input file parser
    """
    import pandas as pd

    df = pd.read_excel (file_path, sheet_name=sheet_name1)
    questions = df['Questions']
    responses = df['Response']
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
    # print(data)

    for query, response in data:

        patter_tokens = word_tokenize(query.lower())
        patterns_without_sw = list(set([word for word in patter_tokens if not word in stopwords]))
        # print(patterns_without_sw)

        tag = "_".join(patterns_without_sw)

        # patterns = patterns_without_sw

        response = response.splitlines()
        response = "<br/>".join(response)


        # patterns = [" ".join(subset) for L in range(0, len(patterns_without_sw)+1) for subset in itertools.combinations(patterns_without_sw, L) if subset]
        # patterns = [" ".join(subset) for L in range(2, len(patterns_without_sw)+1) for subset in itertools.combinations(patterns_without_sw, L) if subset]

        # patterns = []
        # patterns.append(patterns_without_sw)
        # for token in patterns_without_sw:
        #     new = random.sample(patterns_without_sw, len(patterns_without_sw))
        #     pattern = (" ".join(new))
        #     patterns.append(pattern)

        final_patterns = []

        for index, token in enumerate(patterns_without_sw):
            synonyms = synonyms_gen(token)
            for synonym in synonyms:
                new_phrase = patterns_without_sw.copy()
                new_phrase[index] = synonym
                new_pattern = " ".join(new_phrase)
                # print(new_pattern)
                final_patterns.append(new_pattern)


        print(final_patterns)
        intent = {
            "tag": tag,
            "patterns": final_patterns,
            "responses": [response],
            "context": []
        }

        intents.append(intent)


    json_data = {"intents":intents}
    # print(json_data)
    with open(target, 'w') as resfl:
        json.dump(json_data, resfl,  indent = 5)
        resfl.close()


def intent_progress_estimate(file_path, sheet_name):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name)

        # all_tokens = []
        # for query, response in fileContent:
        #     patter_tokens = word_tokenize(query.lower())
        #     patterns_without_sw = list(set([word for word in patter_tokens if not word in stopwords]))
        #     all_tokens += patterns_without_sw
        # print(len(all_tokens))
        # words_count = len(all_tokens)

        questions_count = len(fileContent)
        time_for_a_single_question = 10
        total_etsimated_time = questions_count * time_for_a_single_question
        
        start_time1 = time.time()
        while True:
            print("#"*15)
            time.sleep(2)
            time_spent_till_now = time.time() - start_time1
            print(f"--- progress {int((time_spent_till_now/total_etsimated_time)*100)} % ---")
            print("#"*15)

    else:
        print('File {fp} not found'.format(fp=file_path))    

def intent_generator_function(file_path, sheet_name, json_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fileContent = parse_file(file_path,sheet_name)
        if not os.path.exists(json_path):
            form_json(fileContent, json_path)
        else:
            print('File {fp} already exists.'.format(fp=json_path))
            # prompt = input('Overwrite? Y/N\n')
            prompt = "yes"
            if prompt.strip().casefold() in {'y', 'yes'}:
                print('Overwriting...')
                form_json(fileContent, json_path)
            else:
                print('Exiting...')
                exit(0)
    else:
        print('File {fp} not found'.format(fp=file_path))

if __name__ == '__main__':
    file_path = './data.xlsx'
    sheet_name = "Sheet2"
    json_path =  "./intents.json"
    # intent_generator_function(file_path, sheet_name, json_path)
    intent_progress_estimate(file_path, sheet_name)