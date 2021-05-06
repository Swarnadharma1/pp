import pickle
from xgboost import XGBClassifier
from data_prep import DataPrep
from sklearn.feature_extraction.text import TfidfVectorizer
from time import time
from lightgbm import LGBMClassifier
#                   Explaination of Above modules

#   All of the above modules are explained and mentioned in 
#                   "AccuaracyTest.py"
#                     Please Read it 


class Model:

    def __init__(self):

        
        self.xgb = XGBClassifier(
            learning_rate=0.03,
            max_depth=4,
            min_child_weight=0.5,
            n_estimators=50,
            num_leaves=2,#scale_pos_weight=0.58,
            colsample_bytree=0.3,subsample=0.6,
            silent=False,
        )
        self.tfidf = TfidfVectorizer(
                max_df=0.01,max_features=5000,ngram_range=(1,1),norm='l1',use_idf=True,strip_accents='ascii',binary=True
 
        )
        self.lgb = LGBMClassifier(
            learning_rate=0.03,
            max_depth=4,
            min_child_weight=0.5,
            n_estimators=50,#scale_pos_weight=0.58,
            num_leaves=2,
            colsample_bytree=0.3,subsample=0.6,
            silent=True,
        )

    # Fit a model for the Training Dataset
    def fit(self, X, y):

        X = self.tfidf.fit_transform(X)

        self.lgb = self.lgb.fit(X,y)

    # Predict Results for Data based on the fitted model.
    def predict(self, X):

        X = self.tfidf.transform(X)
        
        return self.lgb.predict(X)

    # Find and return the probability scores for the Categorical Data obtained
    def predict_proba(self, X):

        X = self.tfidf.transform(X)
        return self.lgb.predict_proba(X)

# Below code runs, if the "model.py" is run in python
if __name__ == "__main__":
    from model import Model
    traits = ["OPN", "CON", "EXT", "AGR", "NEU"]
    model = Model()
    t0 = time()
    timer={}

            # Preparing ByteStream Data for the Proposed Model (LightGBM)
    for trait in traits:
        dp = DataPrep()
        X_categorical, y_categorical = dp.prep_data(trait)


        print("LightGBM Fitting trait of" + trait + " categorical model...")
        model.fit(X_categorical, y_categorical)
        print("Done!")


        with open("staticLGB/" + trait + "_model.pkl", "wb") as f:
            # Write the model to a file.
            pickle.dump(model, f)


    t2 = int(time() - t0)
    print("total time occured for working on LightGBM done in %fs" % t2)
