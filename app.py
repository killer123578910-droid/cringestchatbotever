from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from choicenrep.inputanas import response,init_data,formvectorized,init_tf
import pathlib
import json
from dotenv import load_dotenv
import os
import telebot
#telebot
API_KEY=os.getenv("API")
bot=telebot.TeleBot(API_KEY)
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

#psql
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
    chat_id=db.Column(
        db.BigInteger,
        nullable=False,
        doc="chatid"
    )
    chat_name=db.Column(
            db.Text,
            nullable=False,
            doc="name_usr"
        )
    

    create_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        server_default=db.text("now()"),
        doc="Timestamp of message creation"
    )

    def __init__(self,user_ms,bot_rep,chat_id,chat_name):
        self.user_ms=user_ms
        self.bot_rep=bot_rep
        self.chat_id=chat_id
        self.chat_name=chat_name
    def to_dict(self):
        return {'id':self.id,'user_ms':self.user_ms,'bot_rep':self.bot_rep,'chat_id':self.chat_id,'chat_name':self.chat_name,'create_at':self.create_at.isoformat() if self.create_at else None}
    

with app.app_context():
    db.create_all()
    
    
#api route    
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
        
@app.route(f"/tele",methods=["POST"])
def getmessages():
    
    usr=request.get_json()
    if usr and 'message' in usr and 'text' in usr["message"]:
        chat_id= usr['message']['chat']['id']
        chat_name=usr['message']['chat']['first_name']+usr['message']['chat']['last_name']
        text=usr['message']['text']
    
        reply_text=response(tf,fitted,text,tags,data)
        chat=chathis(text,reply_text,chat_id,chat_name)
                
        db.session.add(chat)
        db.session.commit()
        bot.send_message(chat_id=chat_id,text=reply_text)
        return jsonify({"message":reply_text}),200
    else:
        return jsonify({
                    "message":"failed to fetch client input"
                    }),400
        
    
if __name__=="__main__":
    app.run(port=5000,debug=True)
    