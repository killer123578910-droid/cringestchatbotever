from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from choicenrep.inputanas import response,init_data,formvectorized,init_tf
import pathlib
from urllib.parse import quote_plus
import json
from dotenv import load_dotenv
import os

#the json loader
data={}
basedir=pathlib.Path(__file__).parent.resolve()
intenpath=basedir/"choicenrep"/"intents.json"


with open(intenpath,"r",encoding="utf-8") as f:
    data=json.load(f)

#preparing for TF-IDF
tags,patt=init_data(data)
tf=init_tf()
fitted=formvectorized(tf,patt)

load_dotenv()
#Flask
app=Flask(__name__)
pw=os.getenv("DB_URL")
app.config['SQLALCHEMY_DATABASE_URI']=pw
db=SQLAlchemy(app)

class chathis(db.Model):
    __tablename__='chat_his'
    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True,
        server_default=db.text("nextval('chat_his_id_seq'::regclass)")
    )
    
    user_ms = db.Column(
        db.Text,
        nullable=False,
        doc="User message"
    )
    
    bot_rep = db.Column(
        db.Text,
        nullable=False,
        doc="Bot reply/response"
    )
    
    create_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        server_default=db.text("now()"),
        doc="Timestamp of message creation"
    )
    
    def __init__(self,user_ms,bot_rep):
        self.user_ms=user_ms
        self.bot_rep=bot_rep
    def to_dict(self):
        return {'id':self.id,'user_ms':self.user_ms,'bot_rep':self.bot_rep,'create_at':self.create_at.isoformat() if self.create_at else None}
    
    
@app.route("/api/chat",methods=["POST"])    
def chat():
    usr=request.get_json()
    if  not usr or "message" not in usr:
        return jsonify({
            "message":"failed to fetch client input"
            }),400
    else:
        rep=response(tf,fitted,usr["message"],tags,data)
        chat=chathis(usr["message"],rep)
        
        db.session.add(chat)
        db.session.commit()
        
        
        return jsonify({
            "message":rep}),200
if __name__=="__main__":
    app.run()
    