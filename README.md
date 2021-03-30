# chatbot-demo
A chatbot utility using NLTK and Tensorflow

## File structure and the type of files: 
•	`train_chatbot.py`  In this Python file, we wrote a script to build the model and train our chatbot (the deep learning model that can classify and identify what the user is asking from the chatbot).
•	`Intents.json` — The intents file has all the data that we will use to train the model. It stores a collection of tags with their corresponding patterns and responses 
•	`Chatbot_model.h5` – This is a hierarchical data format file in which we have stored the weights of the neurons and the architecture of our trained model.
•	`Classes.pkl` — The pickle file can be used to store all the tag names (list of categories) to classify when we are predicting the message.
•	`Words.pkl` — This is a pickle file, which store all the unique words that are the vocabulary of our model. 
•	`app.py` — This file is where we built an API that can be connected to graphical user interface for easy interaction (chat) with our trained chatbot and also an interface (API) for uploading (replacing/appending) the training data.

##Pipeline:
Here are the 5 steps that we followed to create a chatbot:
1.	Import and load the data file
2.	Preprocess data
3.	Create training and testing data
4.	Build the model
5.	Predict the response

1. Import libraries & Load the data
First, create a new python file and name it as train_chatbot.py and then we are going to import all the required modules the necessary packages for our chatbot and initialize the variables we will use in our Python project. The data file is in JSON format so we used the json package to parse the JSON file into Python.
2. Preprocess data
The model cannot take the raw data. It has to go through a lot of pre-processing for the machine to easily understand. For textual data, there are many preprocessing techniques available.  
Tokenizing is the most basic and first thing you can do on text data. Tokenizing is the process of breaking the whole text into small parts like words.  By observing the intents file, we can see that each tag contains a list of patterns and responses. Here we iterate through the patterns and tokenize the sentence using nltk.word_tokenize() function and append each word in the words list. Also, we create a list of classes and documents to add all the intents associated with patterns.
Another technique is Lemmatization. We can convert words into the lemma form so that we can reduce all the canonical words. For example, the words play, playing, plays, played, etc. will all be replaced with play. This way, we can reduce the number of total words in our vocabulary. So now we lemmatize each word and remove the duplicates.
In the end, the words contain the vocabulary of our project and classes contain the total entities to classify. To save the python object in a file, we used the pickle.dump() method. These files will be helpful after the training is done and we predict the chats.
3. Create training and testing data
For creating the training data our input will be the pattern and output will be the class our input pattern belongs to. But the computer doesn’t understand text so, to train the model, we will convert each input pattern (text) into numbers. 
First, we will lemmatize each word of the pattern and create a list of zeroes of the same length as the total number of words. We will set value 1 to only those indexes that contain the word in the patterns. 
In the same way, we will create the output by setting 1 to the class input the pattern belongs to.
4. Build & Train the model
We have our training data ready, now we will build a deep neural network that has 3 layers. We use the Keras sequential API for this. The first layer has 128 neurons, the second one has 64 and the last layer will have the same neurons as the number of classes. The dropout layers are introduced to reduce overfitting of the model. We have used the SGD optimizer and fit the data to start the training of the model. After the training the model for 200 epochs, we then save the trained model using the Keras model.save(“chatbot_model.h5”) function.
5. Predict the response (API & UI) 
To predict the sentences and get a response from the user we create a new file named as ‘app.py’.
Again we import the necessary packages and load the ‘words.pkl’ and ‘classes.pkl’ pickle files which we have created when we trained our model and also load the trained model and then use an API through which the user can ask a query, and now to predict the class, we will need to provide input in the same way as we did while training. So we will create some functions that will perform text preprocessing and then predict the class. The model will only tell us the class it belongs to, so we will implement some functions which will identify the class and then retrieve us a random response from the list of responses.





6. Run the chatbot
To run the chatbot, we run the app.py file. 
First, we train the model by uploading the data to API with route “/train”, (endpoint: train), we upload the training data in excel sheet format having Q&As columns, If we don’t see any error during file uploading and training, we have successfully created the model. 
Then to interact with chatbot navigate to the index route “/”, where you can find a chat window, this is where the chatbot interact with the user (bot captures the user message and again perform some preprocessing before we input the message into our trained model The model will then predict the tag of the user’s message, and we will randomly select the response from the list of responses in our intents file).

