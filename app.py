from flask import Flask, session, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from chatbotkeras import *
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
    user_response = request.form['user_response']
    # Converting the entire text into lowercase, so that the algorithm does not treat the same words in different cases as different
    user_response = user_response.lower()
    
    bot_response  = chatbot_response(user_response)
        # , 200 , {'ContentType':'application/json'} 

    return jsonify({'response' : bot_response})
if __name__ == "__main__":
    app.run(port=3000, debug = True)