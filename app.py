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
import pandas as pd
UPLOAD_FOLDER = './uploads'
trainCompleted = False
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app,cors_allowed_origins="*", logger=True)
# socketio = SocketIO(app,cors_allowed_origins="*")

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

@app.route('/Bot_response' , methods=['POST'])
def Bot_response():
    """Gives response to user query"""
    
    """
    Request Parameters:
    user_query: Question asked by the user

    Output:
    It will process the user_query to understand the intent of question and answers accordingly
    """
    global trainCompleted

    user_query = request.form['user_query']
    # Converting the query text into lowercase,
    # So that, the algorithm does not treat the same words in different cases as different
    user_query = user_query.lower()

    bot_response  = chatbot_response(user_query,trainCompleted)
    
    trainCompleted = False
    return jsonify({'response' : bot_response})
  
@app.route('/upload', methods=['POST'])
def upload_file():
    """ Train the chatbot on the received xlxs file and request parameters """

    """
    Request Parameters:
    sheet_name      : Name of the sheet used for training data
    question_column : Column name used for questions
    response_column : Column name used for responses
    training_type   : APPEND, REPLACE two values for training type that decides to either append data in intents.json or replace it
    
    This function first checks the file and request parameters & then responds accordingly,
    If the request parameters are correct, data is pre-processed & then the model is trained on the provided data.

    This function will first generate intents.json file in root directory which is used for training,
    while training a new model named "chatbot_model.h5" will be generated along with "classes.pkl" and "words.pkl" files,
    which are used later for processing the user_query to understand the intent of question and generate answers accordingly
    """
    # return if the post request has no file part
    if 'file' not in request.files:
        return "Error : post request have no file part"
    
    file = request.files['file']
    # return if file name is empty
    if file.filename == '':
        return "Error : file not selected"

    global trainCompleted
    
    if file and allowed_file(file.filename):
        """ 
        if the file type is excel sheet as required and is not empty, then save this file to upload folder.
        then check, if the sheetname, and names of question & response coloumns are correct, if yes then start pre-processing & training"""

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        sheet_name = request.form['sheet_name']

        question_column = request.form['question_column']
        # return if question_column is empty
        if not question_column:
            return "Error : question_column is empty"

        response_column = request.form['response_column']
        # return if response_column is empty
        if not response_column:
            return "Error : response_column is empty"

        json_path =  "intents.json"
        training_type = request.form['training_type']

        try:
            # read provided excel sheet
            df = pd.read_excel (file_path, sheet_name=sheet_name)

            # list of the coloumn names in provided excel sheet
            coloumns = [coloumn for coloumn in df]

            if question_column in coloumns and response_column in coloumns:
                """ if the provided names of question & response coloumns are correct, then pre-process the data & train the model"""

                # parsing the excel sheet and generating intents.json file accordingly
                intent_generator_function(socketio, file_path, sheet_name, json_path, question_column, response_column, training_type)

                # training the model based on the generated intents.json
                train(json_path)
                
                # send acknowledgment of process completion (pre-processing & training) to the user
                socketio.emit('message', 100)
                trainCompleted = True
                return "Task complted succesfully"

            else:
                # return if question_column is incorrect
                if question_column not in coloumns:
                    return "Error : question_column is incorrect"

                # return if response_column is incorrect
                if response_column not in coloumns:
                    return "Error : response_column is incorrect"


        except Exception as error:
            # return the raised error, if the sheetname is correct
            return f"Error : {error}"
    
    # return if provided file is not supported
    return "File not supported"
    



if __name__ == "__main__":
    socketio.run(port=5000,host='127.0.0.1', app=app)
    # socketio.run(port=5000,host='0.0.0.0', app=app)
