from flask import Flask,request,jsonify
from choicenrep.inputanas import response,init_data,formvectorized
import pathlib
from underthesea import word_tokenize
import json
from sklearn.feature_extraction.text import TfidfVectorizer

#the json loader
data={}
basedir=pathlib.Path(__file__).parent.resolve()
intenpath=basedir/"choicenrep"/"intents.json"
with open(intenpath,"r",encoding="utf-8") as f:
    data=json.load(f)

def custom_tokenized(text):
    return word_tokenize(text)
#preparing for TF-IDF
tags,patt=init_data(data)
tf=TfidfVectorizer(tokenizer=custom_tokenized,lowercase=True)
fitted=formvectorized(tf,patt)


#Flask
app=Flask(__name__)

@app.route("/api/chat",methods=["POST"])    
def chat():
    usr=request.get_json()
    if  not usr or "message" not in usr:
        return jsonify({
            "message":"failed to fetch cilent input"
            }),400
    else:
        rep=response(tf,fitted,usr["message"],tags,data)
        return jsonify({
            "message":rep}),200
if __name__=="__main__":
    app.run()