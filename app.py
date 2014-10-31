import json

from flask import Flask, jsonify, request

from src import ConversionEngine, RulesEngine
from utility import data

app = Flask(__name__)

converted_data = ConversionEngine.convert(data.test_data)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/raw', methods=['GET'])
def get_raw_data():
    return jsonify(data.test_data)

@app.route('/converted', methods=['GET'])
def get_converted_data():
    return jsonify(converted_data)

@app.route('/events', methods=['GET'])
def get_events():
    percentile = request.args.get('percentile', 'median')
    return jsonify(RulesEngine.run_rules(converted_data, percentile))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)