#!/usr/bin/python3
import argparse
import json
import os
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import random
import itertools
from pre_defined_json import pre_defined_intents


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

def synonms_gen(word):
    synonms = set()
    for syns in wordnet.synsets(word):
        for s in syns.lemma_names():
            synonms.add(s)
    if synonms:
        synonms = [synonym.replace("_"," ") for synonym in synonyms if "_" in synonym]
        return synonms
    else:
        return [word]




def form_json(data, target):
    """
    Appends new pharses to basic intent structure
    """
    intents = []
    for intent in pre_defined_intents:
        intents.append(intent)
    # print(data)
    stopwords = ["included","what", "why","when", "will", "would","of", "or","and", "if","a","an","is", "am", \
                "are", "has","have", "does", "in", "the", "i", "me", "to", "tell", "about","with", "more", "want", "know", "?", "!"]
    for query, response in data:
        patter_tokens = word_tokenize(query.lower())
        patterns_without_sw = list(set([word for word in patter_tokens if not word in stopwords]))
        # print(tokens_without_sw)
        tag = "_".join(patterns_without_sw)



        patterns = [" ".join(subset) for L in range(0, len(patterns_without_sw)+1) for subset in itertools.combinations(patterns_without_sw, L) if subset]

        # patterns = []
        # patterns.append(patterns_without_sw)
        # for token in patterns_without_sw:
        #     new = random.sample(patterns_without_sw, len(patterns_without_sw))
        #     pattern = (" ".join(new))
        #     patterns.append(pattern)

        intent = {
            "tag": tag,
            "patterns": patterns,
            "responses": [response],
            "context": []
        }

        intents.append(intent)


    json_data = {"intents":intents}
    # print(json_data)
    with open(target, 'w') as resfl:
        json.dump(json_data, resfl,  indent = 5)
        resfl.close()



if __name__ == '__main__':
    file_path = r'./data.xlsx'
    sheet_name = "Sheet1"
    json_path =  "./intents.json"
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
        exit(1)
