from flask import Flask
import requests
from flask import request, jsonify
import time

app=Flask(__name__)

THIRD_PARTY_API_URL = 'https://jsonplaceholder.typicode.com'
retries=5

@app.route('/')
def hello():
    return 'Default route'
   
@app.route('/data', methods=['GET'])
def get_data():
    url = THIRD_PARTY_API_URL + '/posts'
    response = call_api(url, None, 'GET')
    if response.status_code == 200:
        data = response.json()[:10]
        return data
    else:
        return {'error': 'Failed to fetch data'}

   
@app.route('/data', methods=['POST'])
def create_data():
    data = request.json
    url=THIRD_PARTY_API_URL + '/posts'
    response = call_api(url, data, 'POST')
    if response.status_code == 201:
        return response.json()
    else:
        return {'error': 'Failed to create data'}

@app.route('/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    updated_data = request.json
    url = THIRD_PARTY_API_URL + '/posts/' + str(data_id)
    response = call_api(url, updated_data, 'PUT')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to update data'}

@app.route('/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    url=THIRD_PARTY_API_URL + '/posts/' + str(data_id)
    response = call_api(url, None, 'DELETE')
    if response.status_code == 200:
        return {'message': 'Data successfully deleted'}
    else:
        return {'error': 'Failed to delete data'}


def call_api(url,body,method):

    for i in range(retries):
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=body)
            elif method == 'PUT':
                response = requests.put(url, json=body)
            elif method == 'DELETE':
                response = requests.delete(url)
            else:
                raise Exception('Failed to send request')
            return response
           
        except Exception as e:
            error_message = str(e)
            if i < retries - 1:
                time.sleep(2 ** i)
            else:
                return {'error': error_message}
    