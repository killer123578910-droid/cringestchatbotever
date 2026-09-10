#import llm;
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage
from dotenv import load_dotenv
import os
from rag_engine.rag_preprocess import response
load_dotenv()

api=os.getenv("op_api")
llm = ChatOpenAI(
    model="google/gemma-4-31b-it",
    api_key=api,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7
)


#take top k similarity, form its content to a context text;
def form_prompt(userq,k,user_id):
    listofrelevent=list(response(userq,k,user_id))
    context_text=' '.join(row[0] for row in listofrelevent)
    listofchosenid=[row[3] for row in listofrelevent]

    sysprompt=f'You are a knowledgeable virtual assistant. Based on the following information: {context_text}, answer the users question. If the information is not available in the context, say that you do not know. Do not make up or fabricate any information.'
    messages=[
        SystemMessage(content=sysprompt),
        HumanMessage(content=userq)
    ]
    return messages,listofchosenid

#put prompt for llm do generate answer. response answer.
def take_rep(sysprompt):
    return(llm.invoke(sysprompt).content)


if __name__=="__main__":
    #testkey()
    promt,embedchunked=form_prompt("what is rag",5)
    print("top 5 most relevant text: \n")
    for i in range(len(embedchunked)):
        print(f'tier:{i} : {embedchunked[i]} \n')
    print('answer'+ ': ' +take_rep(promt))
        