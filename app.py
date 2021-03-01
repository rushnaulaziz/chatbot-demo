from flask import Flask,jsonify, request
from flask_cors import CORS

from ChatBot import *

app = Flask(__name__)
CORS(app)

@app.route('/message' , methods=['POST'])
def message():
    request_data = request.get_json()
    print(request_data)
    # Converting the entire text into lowercase, so that the algorithm does not treat the same words in different cases as different
    user_response = request_data['user_response'].lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            #flag=False
            bot_response = "Bot: You are welcome.."
        else:
            if(greeting(user_response)!=None):
                bot_response  = "Bot: "+ greeting(user_response)
            else:
                print("Bot: ",end="")
                bot_response  = "Bot: "+ response(user_response)
                sent_tokens.remove(user_response)
    else:
        flag=False
        bot_response  = "Bot: "+ "Bot: Bye! Leaving for now, take care.."
        

    return jsonify({'response':bot_response}),200




app.run(port=3000)