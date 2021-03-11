from flask import Flask, session, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask import send_from_directory

from chatbotkeras import *
from werkzeug.utils import secure_filename
import os
UPLOAD_FOLDER = './uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

# Setting the secret key to some random bytes
app.secret_key = "any random string"
# command for generating random secrete key : python -c 'import os; print(os.urandom(16))'
# session['username'] can be set using with username entered while logging in 
# session.pop('username', None) can remove the username from the session if it's there

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/chatbot2_demo')
# def chatbot2_function():
#     return render_template("chatbot2.html")

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

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File Uploaded succesfully"
            # return "redirect(url_for('uploaded_file', filename=filename))"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
if __name__ == "__main__":
    app.run(port=3000, debug = True)