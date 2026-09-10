from flask import Flask,request,jsonify
import requests
from extensions import db
from sqlalchemy import text
from datetime import datetime
import pathlib
from rag_engine.get_rep import take_rep,form_prompt
from rag_engine.rag_preprocess import delete_vtdb,add_text_features
import json
from dotenv import load_dotenv
import os
import telebot
from zoneinfo import ZoneInfo
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


load_dotenv()
#Flask
app=Flask(__name__)

#psql
pw=os.getenv("DB_URL")
app.config['SQLALCHEMY_DATABASE_URI']=pw
db.init_app(app)

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
        default=datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")),
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
@app.route(f"/tele",methods=["POST"])
def getmessages():

    usr=request.get_json()
    
    if usr and 'message' in usr:
        chat_id= usr['message']['chat']['id']
        chat_name=usr['message']['chat'].get('first_name', '') + " " + usr['message']['chat'].get('last_name', '')

        if('caption' in usr['message']):
            
            if 'document' in usr['message'] and usr['message']['document']['mime_type']=='text/plain' and usr['message']['caption']=='/input':
                file_id=usr['message']['document']['file_id']
                
                
                file_path=requests.get(f"https://api.telegram.org/bot{API_KEY}/getFile?file_id={file_id}")
                file_content=requests.get(f"https://api.telegram.org/file/bot{API_KEY}/{file_path.json()['result']['file_path']}")
                add_text_features(file_content.text,chat_id)
                return jsonify({
                    'method':'sendMessage',
                    'chat_id':chat_id,
                    'text':'data digested' 
                }),200
            else:
                return jsonify({
                                    'method':'sendMessage',
                                    'chat_id':chat_id,
                                    'text':'wrong input syntax or no file included, please do /input and include your file' 
                                }),404
                
                
            
        elif 'text' in usr["message"]:         

            if usr['message']['text'].startswith('/input'):
                txt=usr['message']['text'].replace('/input','')
                

                add_text_features(txt,chat_id)
                return jsonify({
                    'method':'sendMessage',
                    'chat_id':chat_id,
                    'text':'data digested'
                }),200
            elif usr['message']['text'].startswith('/delete'):
                delete_vtdb()
                return jsonify({
                                    'method':'sendMessage',
                                    'chat_id':chat_id,
                                    'text':'context cleared'
                                }),200
            
            else:
                txt=usr['message']['text']

                processed,listofrag=form_prompt(userq=txt,k=7,user_id=chat_id)
                reply_text=take_rep(processed) 

        
                

                update_sql_cm=f"""update chatbot_vector set created_at = :current_timestamp where id in ({','.join(str(r) for r in listofrag)});"""
                db.session.execute(text(update_sql_cm),{'current_timestamp':datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()})        

                chat=chathis(txt,reply_text,chat_id,chat_name)
                db.session.add(chat)
                db.session.commit()
                return jsonify({
                    "method":"sendMessage",
                    "chat_id":chat_id,
                    "text":reply_text}),200
    else:
        return jsonify({
                    "message":"failed to fetch client input"
                    }),400

    
if __name__=="__main__":
    app.run(port=5000,debug=True)
    