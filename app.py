from flask import Flask, jsonify, request, render_template,redirect, flash
from flask_cors import CORS
from intent_generator import intent_generator_function, allowed_file
from chatbotkeras import chatbot_response
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO
from train_chatbot import train
import time
import threading

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app,cors_allowed_origins="*", logger=True)

CORS(app)

# Setting the secret key to some random bytes
app.secret_key = "any random string"
# command for generating random secrete key : python -c 'import os; print(os.urandom(16))'

@app.route('/')
def index():
    """Provides template for / URL"""
    return render_template("index.html")

@app.route('/train', methods=['GET'])
def train_template():
    """Provides template for /train URL"""
    return render_template("train.html")

@app.route('/message' , methods=['POST'])
def message():
    """Gives response to user query"""
    """
    Request Parameters:
    user_query: Question asked bt user
    

    It will process the user_query to understand the intent of question and answers accordingly

    """
    user_query = request.form['user_query']
    # Converting the entire text into lowercase, so that the algorithm does not treat the same words in different cases as different
    user_query = user_query.lower()
    bot_response  = chatbot_response(user_query)

    return jsonify({'response' : bot_response})
  
@app.route('/upload', methods=['POST'])
def upload_file():
    """Train the chatbot on the received xlxs file and request parameters"""
    """
    Request Parameters:
    sheet_name: Name of the sheet used for training data
    question_column: Column name used for questions
    response_column: Column name used for responses

    It will generate intent.json file in root directory which will then be used to train chatbot
    
    New model named "chatbot_model.h5" willl be generated along with "classes.pkl" and "words.pkl" files

    """
    # return if the post request has no file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # return if file name is empty
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    #
    sheet_name = request.form['sheet_name']
    question_column = request.form['question_column']
    response_column = request.form['response_column']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        json_path =  "intents.json"
        
        intent_generator_function(socketio, file_path, sheet_name, json_path, question_column, response_column)
        train(json_path)
        socketio.emit('message', 100)
        
        return "Task complted succesfully"
    return "File not supported"
    



if __name__ == "__main__":
    socketio.run(port=3000, debug=True, app=app)
