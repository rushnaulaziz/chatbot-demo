from app import app
from flask import json

def test_index():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello, World!'

def test_train_template():
    response = app.test_client().get('/train')

    assert response.status_code == 200
    # assert response.data == b'Hello, World!'


def test_Bot_response():
    url = '/Bot_response'
    data = {
        'user_uery': "what"
    }
    content_type='application/json'
    headers =""
    response = app.test_client().post(url, data=json.dumps(data))

    # response = client.post(url, data=json.dumps(data))
        
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['response'] == "Sorry, I'm not able to understand your question. Can you please ask a different question?"

def test_Bot_response():
    url = '/Bot_response'
    data = {
        sheet_name = "Sheet2" 
        question_column = "Input"
        response_column = "Chatbot Response"
        training_type  = ""
    }
    content_type='application/json'
    headers = ""
    response = app.test_client().post(url, data=json.dumps(data))

    # response = client.post(url, data=json.dumps(data))
        
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['response'] == "Sorry, I'm not able to understand your question. Can you please ask a different question?"