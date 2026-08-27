from flask import Flask,request,jsonify
from choicenrep.inputanas import response
import pathlib
import json
data={}
basedir=pathlib.Path(__file__).parent.resolve()
intenpath=basedir/"choicenrep"/"intents.json"
with open(intenpath,"r",encoding="utf-8") as f:
    data=json.load(f)
#the json loaded
app=Flask(__name__)

@app.route("/api/chat",methods=["POST"])    
def chat():
    usr=request.get_json()
    if  not usr or "message" not in usr:
        return jsonify({
            "message":"failed to fetch cilent input"
            }),400
    else:
        rep=response(data,usr["message"])
        return jsonify({
            "message":rep}),200
if __name__=="__main__":
    app.run()