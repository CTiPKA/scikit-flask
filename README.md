# scikit-flask

Docker container to work easily with SciKit-Learn framework as service. Flask using to access scikit as REST service.

Implemented API calls:

  /ndcg_score
  
  parameters:
  
   {
  
     "ground_truth":[1, 0, 2],
    
     "predictions":[[0.15, 0.55, 0.2], [0.7, 0.2, 0.1], [0.06, 0.04, 0.9]],
    
     "k":2
    
  }
  
