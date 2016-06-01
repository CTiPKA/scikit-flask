import numpy as np
from flask import Flask, request, jsonify
from sklearn.preprocessing import LabelBinarizer
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

@app.route('/post_test', methods=['POST'])
def post_test():
    """POST data test"""
    
    request_json = request.get_json(force=True)
    
    ground_truth = request_json['ground_truth']
    predictions = request_json['predictions']
    k = request_json['k']
    
    response_dict = {"ground_truth":ground_truth,"predictions":predictions,"k":k}
    
    return jsonify(**response_dict)

def dcg_score(y_true, y_score, k=5):
    """Discounted cumulative gain (DCG) at rank K.
        
        Parameters
        ----------
        y_true : array, shape = [n_samples]
        Ground truth (true relevance labels).
        y_score : array, shape = [n_samples, n_classes]
        Predicted scores.
        k : int
        Rank.
        
        Returns
        -------
        score : float
        """
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])
    
    gain = 2 ** y_true - 1
    
    discounts = np.log2(np.arange(len(y_true)) + 2)
    return np.sum(gain / discounts)


def ndcg_score(ground_truth, predictions, k=5):
    """Normalized discounted cumulative gain (NDCG) at rank K.
        
        Normalized Discounted Cumulative Gain (NDCG) measures the performance of a
        recommendation system based on the graded relevance of the recommended
        entities. It varies from 0.0 to 1.0, with 1.0 representing the ideal
        ranking of the entities.
        
        Parameters
        ----------
        ground_truth : array, shape = [n_samples]
        Ground truth (true labels represended as integers).
        predictions : array, shape = [n_samples, n_classes]
        Predicted probabilities.
        k : int
        Rank.
        
        Returns
        -------
        score : float
        
        Example
        -------
        >>> ground_truth = [1, 0, 2]
        >>> predictions = [[0.15, 0.55, 0.2], [0.7, 0.2, 0.1], [0.06, 0.04, 0.9]]
        >>> score = ndcg_score(ground_truth, predictions, k=2)
        1.0
        >>> predictions = [[0.9, 0.5, 0.8], [0.7, 0.2, 0.1], [0.06, 0.04, 0.9]]
        >>> score = ndcg_score(ground_truth, predictions, k=2)
        0.6666666666
        """
    lb = LabelBinarizer()
    lb.fit(range(len(predictions) + 1))
    T = lb.transform(ground_truth)
    
    scores = []
    
    # Iterate over each y_true and compute the DCG score
    for y_true, y_score in zip(T, predictions):
        actual = dcg_score(y_true, y_score, k)
        best = dcg_score(y_true, y_true, k)
        score = float(actual) / float(best)
        scores.append(score)
    
    return np.mean(scores)

@app.route('/ndcg_score_example', methods=['GET'])
def metric2_example():
    """NDCG test call for hardcoded data"""
    ground_truth = [1, 0, 2]
    predictions = [[0.15, 0.55, 0.2], [0.7, 0.2, 0.1], [0.06, 0.04, 0.9]]
    score1 = ndcg_score(ground_truth, predictions, k=2)

    predictions = [[0.9, 0.5, 0.8], [0.7, 0.2, 0.1], [0.06, 0.04, 0.9]]
    score2 = ndcg_score(ground_truth, predictions, k=2)

    response_dict = {"ndcg_score1" : score1, "ndcg_score2":score2}

    return jsonify(**response_dict)

@app.route('/ndcg_score', methods=['POST'])
def metric2():
    """NDCG calculation on received data"""
        
    request_json = request.get_json(force=True)
    
    ground_truth = request_json['ground_truth']
    predictions = request_json['predictions']
    k = request_json['k']
    score = ndcg_score(ground_truth, predictions, k)
    
    return jsonify(ndcg_score=score)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')