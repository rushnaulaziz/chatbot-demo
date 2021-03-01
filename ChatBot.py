
#Meet Robo: chatbot that answeres queries regarding chatbot only.

#import necessary libraries
import io
import random
import string 
import numpy as np
# Tfidf is abbreviation of "Term Frequency * Inverse-Document Frequency"
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')

# for downloading popular, punkt and wordnet packages
nltk.download('popular', quiet=True)

# NLTK data package includes a pre-trained Punkt and wordnet tokenizer for English
# uncomment the following only the first time
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only


       
# Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()


#Tokenisation
"""
Tokenization is the process of converting the normal text strings into a list of tokens i.e words that we actually want.
Sentence tokenizer can be used to find the list of sentences and Word tokenizer can be used to find the list of words in strings.
"""
sent_tokens = nltk.sent_tokenize(raw)        
word_tokens = nltk.word_tokenize(raw)   


# Preprocessing
""" includes conversion to lower case, removing punctuations, stemming & lemmatizing (reducing words to their base or root form"""
def lem_tokens(tokens):
    lemmer = WordNetLemmatizer()
    # reducing inflected (or sometimes derived) words to their stem, base or root form
    return [lemmer.lemmatize(token) for token in tokens]                        

# ord returns the Unicode code of a specific character.
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)   
def lem_normalize(text):
    # converting the string to lowercase & Removing Stop words.
    my_tokens = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    # lemmatizing the tokens
    return lem_tokens(my_tokens)    

# Keyword Matching for Greetings
"""If user's input is a greeting, return a random greeting response"""
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
 
# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)

    # to rescale the frequency of words by how often they appear in all documents so that the scores for frequent words like “the” whih is frequent across all documents are penalized.
    tfidf_vec = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')
    tfidf = tfidf_vec.fit_transform(sent_tokens)
    
    # transformation applied to texts to get two real-valued vectors in vector space.
    simililarity_values = cosine_similarity(tfidf[-1], tfidf)
    
    indexes = simililarity_values.argsort()[0][-2]
    flat    = simililarity_values.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf==0):
        # if can't find correlation, respond randomly from a response_choices list
        response_choices = ["I am sorry! I don't understand you", "Sorry, can't understand you", "Please give me more info", "Not sure I understand"]
        robo_response = random.choice(response_choices)
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[indexes]
        return robo_response
        
if __name__ == "__main__":
    flag=True
    print("Bot: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye")
    while(flag==True):
        user_response = input("You: ")
        
        # Converting the entire text into lowercase, so that the algorithm does not treat the same words in different cases as different
        user_response = user_response.lower()
        if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you' ):
                #flag=False
                print("Bot: You are welcome..")
            else:
                if(greeting(user_response)!=None):
                    print("Bot: "+ greeting(user_response))
                else:
                    print("Bot: ",end="")
                    print(response(user_response))
                    print("")
                    sent_tokens.remove(user_response)
        else:
            flag=False
            print("Bot: Bye! Leaving for now, take care..")
            
            
