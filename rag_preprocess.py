from langchain_openai import OpenAIEmbeddings 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from dotenv import load_dotenv
import psycopg2
import os

openrouter_api=os.getenv("op_api")
connectid=os.getenv("DB_URL")

#đọc file,đưa thành text(join lại thành các docs)

#chunking sử dụng textspliter


#dùng embeds_documents để đẩy docs vào vector db(if not exist)


#queries and response( embeds_query)-> select .. from table order by embedding <=>(cosine similarity)::%s limit k; 