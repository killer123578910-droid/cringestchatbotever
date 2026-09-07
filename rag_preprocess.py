from langchain_openai import OpenAIEmbeddings 
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_core.documents import Document
from dotenv import load_dotenv
import psycopg2
import os,json,pathlib

load_dotenv()
openrouter_api=os.getenv("op_api")
connectid=os.getenv("DB_URL")
db=psycopg2.connect(connectid)
cur=db.cursor()


def closedb(db,cur):
    cur.close()
    db.close()
#đọc file,đưa thành text -> update(user input name of files,loop over the list of name to open each file and store in a list of docs)


def init_data():
    docs=[]
    with open("context.txt",'r',encoding='UTF8') as f:
        docs.append(Document(page_content=f.read(),metadata={'source':"userfile",'author':'kh'}))
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
    encoding_format='float'
)

def embed_docs(docs):
    
    doclist=[doc.page_content for doc in docs]
    data=embedmodel.embed_documents(doclist)
    for i in range(len(data)):
        cur.execute("""insert into chatbot_vector (content,embedding) values(%s,%s) """,(doclist[i],data[i]))

    db.commit()

#queries and response( embeds_query)-> select .. from table order by embedding <=>(cosine similarity)::%s limit k; 
def response(userquery,k):
    embedqur=embedmodel.embed_query(userquery)

    cur.execute("""select content,1-(embedding<=> %s::vector) as cosine_diff 
                    from chatbot_vector 
                    order by embedding <=> %s::vector 
                    limit %s""",
                    (embedqur,embedqur,k))
    print(cur.fetchall())


if __name__=="__main__":
    #operator for push embedded vector into dbvector   
    #data=init_data()
    #processed=chunking(data)
    #embed_docs(processed)



    #query parts
    userq='rag is a powerful tool'
    response(userquery=userq,k=5)

    #dbclose()
