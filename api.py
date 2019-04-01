"""Question Answering API Service """

import argparse

from flask import Flask, request, jsonify
from waitress import serve

from model import init_qa

parser = argparse.ArgumentParser('Menu Tagger API service')

parser.add_argument('--host', default='0.0.0.0', type=str, help="server host")
parser.add_argument('--port', default='5000', help="server port")
parser.add_argument('--query_key', default='questions', help="key to pass questions list in request body")
parser.add_argument('--data_path', default='data/sample_qa_data.csv', help="path to the qa data")
parser.add_argument('--debug', action='store_true', help='enable debugging')

app = Flask(__name__)


@app.route('/', methods=['POST'])
def api_qa():
    data = request.get_json()
    questions = data[args.query_key]
    max_distance = data["max_distance"]

    results = []
    for question in questions:
        id = question.get('id', None)
        question_text = question.get('question', '')
        answer = qa_model.query(question_text, max_distance)

        results.append(dict(id=id, question=question_text, answer=answer))

    return jsonify(results)


global qa_model
if __name__ == '__main__':
    args = parser.parse_args()
    qa_model = init_qa(args.data_path)

    if args.debug:
        # this will be used for development purposes instead of serve
        app.run(host=args.host, port=args.port, debug=True)
    else:
        serve(app.wsgi_app, host=args.host, port=args.port, threads=True)
