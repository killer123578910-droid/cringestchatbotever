import telebot
import os
from dotenv import load_dotenv
import requests
load_dotenv()
API_KEY=os.getenv("API")
bot=telebot.TeleBot(API_KEY)


@bot.message_handler(func= lambda message:True,content_types=["text"])
def readmess(message):

    user_text=message.text
    chat_id=message.chat.id
    usrn=message.from_user.username
    try:
        #for localhost:(replace https://cringest.....com to http://127.0.0.1:5000)
        response=requests.post("https://cringestchatbotever.onrender.com/api/chat",json={"message":user_text})
        text=response.json()["message"]
        bot.send_message(text=text,chat_id=chat_id)
    except Exception as e:
        print(f"error: {e}")    
if __name__=="__main__":
    bot.polling()