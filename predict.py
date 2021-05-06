import pandas as pd
import pickle
from data_prep import DataPrep
from model import Model
from statistics import mean

#                   Explaination of Above modules
#
#  from model import Model:
#  calls the "model.py" file
#
#   Rest of the above modules are explained and mentioned in 
#                   "AccuaracyTest.py"
#                     Please Read it 

class Predictor():
    def __init__(self):
        from model import Model
        self.traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
        self.models = {}

    # This function loads the pickle model to predict scores on test data.
    def load_models(self):
        for trait in self.traits:
            with open('staticLGB/' + trait + '_model.pkl', 'rb') as f:
                self.models[trait] = pickle.load(f)

    # This uses the loaded pickle data to perform the prediction
    def predict(self, X, traits='All', predictions='All'):
        predictions = {}
        self.load_models()
        if traits == 'All':
            for trait in self.traits:
                pkl_model = self.models[trait]

                trait_categories = pkl_model.predict(X)
                predictions['pred_c'+trait] = str(trait_categories[0])

                trait_categories_probs = pkl_model.predict_proba(X)
                predictions['pred_prob_c'+trait] = mean(trait_categories_probs[:, 1])
        

        return predictions


