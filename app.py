from flask import Flask
from sklearn.metrics import recall_score
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/recall_score', methods=['GET'])
def metric1():
    y_true = [0, 1, 2, 0, 1, 2]
    y_pred = [0, 2, 1, 0, 0, 1]
    result = recall_score(y_true, y_pred, average='macro')
    return 'recall_score: ' + str(result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')