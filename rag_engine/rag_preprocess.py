from langchain_openai import OpenAIEmbeddings 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_core.documents import Document
from dotenv import load_dotenv
from sqlalchemy import text
from extensions import db
import os,pathlib
from datetime import datetime

load_dotenv()
openrouter_api=os.getenv("op_api")

#folder traverse
curdir=pathlib.Path(__file__).parent.resolve()
basedir=curdir.parent
contextdir=basedir/"context"

def delete_vtdb():
    db.session.execute(text('truncate table chatbot_vector restart identity'))
def add_text_features(text,chat_id):
    docs=[Document(
                    page_content=text,
                    metadata={'source':'user_file','author':chat_id})]
    chunked=chunking(docs)
    embed_docs(chunked,chat_id)

#đọc file,đưa thành text -> update(user input name of files,loop over the list of name to open each file and store in a list of docs)
def init_data(contextdir,user_name):
    cupath=pathlib.Path(contextdir)
    docs=[]
    for i in cupath.glob("*.txt"):
        try:
            docs.append(
                Document(
                    page_content=i.read_text(encoding='utf8'),
                    metadata={'source':'user_file','author':user_name,'file_name':i.name}
                )
            )
        except Exception as e:
            print(f"error: cant not read upload file,detail:{e}")
    return docs

#chunking sử dụng textspliter
chunker=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=10)
def chunking(docs):
    return chunker.split_documents(docs)



#dùng embeds_documents để đẩy docs vào vector db(if not exist)
embedmodel=OpenAIEmbeddings(
    model="nvidia/nemotron-3-embed-1b:free",         # Specify the OpenRouter model slug
    openai_api_key=openrouter_api,  # Your OpenRouter API Key
    openai_api_base="https://openrouter.ai/api/v1", # OpenRouter base endpoint
    check_embedding_ctx_length=False ,
    encoding_format='float',
)

def embed_docs(docs,chat_id):
    
    doclist=[doc.page_content for doc in docs]
    data=embedmodel.embed_documents(doclist)
    sql_command=text("""insert into chatbot_vector (content,embedding,user_id,created_at) values(:content,:embedding,:user_id,:time) """)
    for i in range(len(data)):
        db.session.execute(sql_command,{'content':doclist[i],'embedding':str(data[i]),'user_id':chat_id,'time':datetime.now().isoformat()})

    db.session.commit()

#queries and response( embeds_query)-> select .. from table order by embedding <=>(cosine similarity)::%s limit k; 
#next task: import llm, config rag to llm and get response in text
#def responsefortesting(app,userquery,k):
 #   embedqur=embedmodel.embed_query(userquery)
  #  with app.app_context():
   #     sql_command=text("""select content,1-(embedding<=> cast(:vu as vector)) as cosine_diff from chatbot_vector order by embedding <=> cast(:vu as vector) limit :limit_k""")
    #    req=db.session.execute(sql_command,{"vu":str(embedqur),"limit_k":k})
     #   #print(req.fetchall())
    #return req.fetchall()

def response(userq,k,user_id):
    embedqur=embedmodel.embed_query(userq)
    sql_command=text("""select content,1-(embedding<=> cast(:vu as vector)) as cosine_diff from chatbot_vector where user_id = :user_id order by embedding <=> cast(:vu as vector) limit :limit_k""")
    req=db.session.execute(sql_command,{"vu":str(embedqur),'user_id':user_id,"limit_k":k})
    #print(req.fetchall())
    return req.fetchall()
if __name__=="__main__":
    #operator for push embedded vector into dbvector   
    #data=init_data()
    #processed=chunking(data)
    #embed_docs(processed)
    #from app import app

    #query parts
    userq='rag is a powerful tool'
    #print(responsefortesting(app,userq,5))


    #dbclose()
