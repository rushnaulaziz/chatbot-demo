from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import random
import itertools
from PyDictionary import PyDictionary

def synonyms_gen(word):
    
    dictionary=PyDictionary()
    synonyms = dictionary.synonym(word)
    if synonyms:
        synonyms = [synonym for synonym in synonyms if len(synonym.split()) < 2]
    return synonyms

# print(synonyms_gen("cost")) 

patterns = ["chatbot", "habit",  "sleep",  "early"]
pattern_org = patterns
def ok():
    final_pattern = []

    for index, token in enumerate(patterns):
        synonyms = synonyms_gen(token)
        for synonym in synonyms:
            new_phrase = patterns.copy()
            new_phrase[index] = synonym
            new_pattern = " ".join(new_phrase)
            print(new_pattern)

            # final_pattern.append(new_pattern)

    # print(final_pattern)

synonyms = synonyms_gen("chatbot")
# print(synonyms)