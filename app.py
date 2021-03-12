from flask import Flask, session, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask import send_from_directory
from intent_generator import intent_generator_function, parse_file
from chatbotkeras import *
from werkzeug.utils import secure_filename
import os
from flask_socketio import SocketIO
from train_chatbot import train
import time
import threading

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app,cors_allowed_origins="*", logger=True)

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
    ''' It will fetch the user  '''
    user_query = request.form['user_query']
    # Converting the entire text into lowercase, so that the algorithm does not treat the same words in different cases as different
    user_query = user_query.lower()
    
    bot_response  = chatbot_response(user_query)
        # , 200 , {'ContentType':'application/json'} 
    return jsonify({'response' : bot_response})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def intent_progress_estimate(file_path, sheet_name, stop):
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
            time.sleep(2)
            time_spent_till_now = time.time() - start_time1
            progress = int((time_spent_till_now/total_etsimated_time)*100) 
            socketio.emit('message', progress)
            print(f"--- progress : {progress} % ---")

            if stop():
                progress = 100
                socketio.emit('message', progress)
                print(f"--- progress : {progress} % ---")
                break
    else:
        print('File {fp} not found'.format(fp=file_path)) 
   
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # os.system("") 
            sheet_name = "Sheet2"
            json_path =  "./uploads/intents.json"
            start_time = time.time()
            stop_thread = False
            thread1 = threading.Thread(target=intent_progress_estimate, args=(file_path, sheet_name, lambda : stop_thread))
            thread1.start()

            intent_generator_function(file_path, sheet_name, json_path)
            train(json_path)
            print(f"--- {time.time() - start_time} seconds ---")
            stop_thread = True
            
            return "Task complted succesfully"
            # return "redirect(url_for('uploaded_file', filename=filename))"

    return render_template("socket_com.html")

if __name__ == "__main__":
    socketio.run(port=3000, debug=True, app=app)
