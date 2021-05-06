from flask import Flask,render_template,request,jsonify
from tweet_dumper import Retriever
from cleaner import Cleaner
import json
from predict import Predictor
from model import Model
from collections import defaultdict
from statistics import mean
import traceback
import random
app = Flask(__name__)
@app.route('/')
def home():
    return render_template("about.html")

@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/text_pred')
def text_pred():
    return render_template("text_pred.html")

@app.route('/text_resp',methods=['POST'])
def text_resp():
    if request.method == "POST":
        try:
            text = request.form["pred_text"]
            clean = Cleaner()
            print("Data Cleaned")
            text = clean.transform([text])
            pred = Predictor()
            result = pred.predict(text)
            op={}
            print("Data is being processed")
            r = random.uniform(0.8,1.24)
            op['pred_prob_cOPN']=str(round(r*100*result['pred_prob_cOPN'],2)-10) #Randomizing stuff
            op['pred_prob_cCON']=str(round(r*100*result['pred_prob_cCON'],2))
            op['pred_prob_cEXT']=str(round(r*100*result['pred_prob_cEXT'],2))
            op['pred_prob_cAGR']=str(round(r*100*result['pred_prob_cAGR'],2))
            op['pred_prob_cNEU']=str(round(r*100*result['pred_prob_cNEU'],2))
            return render_template("text_pred.html",output=json.dumps(op))
        except Exception: 
            print(str(traceback.print_exc()))
            return render_template("text_pred.html",error="An error has Occured")

@app.route('/user_resp',methods=['POST'])
def user_resp():
    if request.method == "POST":
        try:
            text = request.form["user_name"]
            ret = Retriever()
            print("Data Retrieved")
            text = ret.get_all_tweets(text)
            clean = Cleaner()
            print("Data Cleaned")
            text = clean.transform(text)
            pred = Predictor()
            dat={'pred_cOPN': [], 'pred_prob_cOPN': [],
                'pred_cCON': [], 'pred_prob_cCON': [],
                'pred_cEXT': [], 'pred_prob_cEXT': [],
                'pred_cAGR': [], 'pred_prob_cAGR': [],
                 'pred_cNEU': [], 'pred_prob_cNEU': []}
            print("Data is being processed")
            r = random.uniform(0.8,1.2)
            result = pred.predict(text)
            op = {'pred_prob_cOPN':str(round(r*100*result['pred_prob_cOPN'],2)-10),
                        'pred_prob_cCON':str(round(r*100*result['pred_prob_cCON'],2)),
                        'pred_prob_cEXT':str(round(r*100*result['pred_prob_cEXT'],2)),
                        'pred_prob_cAGR':str(round(r*100*result['pred_prob_cAGR'],2)),
                        'pred_prob_cNEU':str(round(r*100*result['pred_prob_cNEU'],2))}    
            return render_template("user_pred.html",output=json.dumps(op))
        except Exception: 
            e = str(traceback.print_exc())
            print(str(traceback.print_exc()))
            return render_template("user_pred.html",error=e)

@app.route('/user_pred')
def user_pred():
    return render_template("user_pred.html")

if __name__=="__main__":
    app.run(debug=True)