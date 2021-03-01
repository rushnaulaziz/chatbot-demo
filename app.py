from flask import Flask, session, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS

from ChatBot import *

app = Flask(__name__)
CORS(app)

# Setting the secret key to some random bytes
app.secret_key = "any random string"
# command for generating random secrete key : python -c 'import os; print(os.urandom(16))'
# session['username'] can be set using with username entered while logging in 
# session.pop('username', None) can remove the username from the session if it's there

@app.route('/')
def index():
    return render_template("index.html")

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
                # print("Bot: ",end="")
                bot_response  = "Bot: "+ response(user_response)
                sent_tokens.remove(user_response)
    else:
        bot_response  = "I"
    return jsonify({'response' : bot_response}),200

if __name__ == "__main__":
    app.run(port=3000, debug = True)