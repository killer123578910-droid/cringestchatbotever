import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from underthesea import text_normalize,word_tokenize
from sklearn.metrics.pairwise import cosine_similarity


def randome(rep):
    return random.choice(rep)




#init data: take list of responses-take list of tags
def init_data(data):
    tags=[]
    patterns=[]
    intents=data["intents"]
    for tag,patt in intents.items():
        tags.append(tag)
        patterns.append(patt["patterns"])
        
    return tags,patterns

def custom_tokenized(text):
    return word_tokenize(text)


#tfidf fit_transform: vectorizing the response list(feature matrix) 
def formvectorized(tf,patt):
    #fit all text to make a general vocab for intents detect, req a [" "," ",...]
    alldoc=[doc for intent in patt for doc in intent]
    tf.fit(alldoc)
    res=[]
    for iten in patt:
        if len(iten)>0:
            matrix=tf.transform(iten)
            res.append(matrix)
        
    return res

def uservectorized(tf,inte):
    maxtrix=tf.transform(inte)
    return maxtrix
#predict respose: 
#-load user reply- underthesea-vectorized-calculate cosine similarity with each feature vector and take the highest
#check if max >=0.3? take tag,response base on json:tag==fallback,response. 
def response(tf,patt,user_int,tags,data):
    user_int=[text_normalize(user_int)]
    vectorized=uservectorized(tf,user_int)
    
    
    
    max_score=0
    maxidx=0
    for idx,value in enumerate(patt):
        cur_score=max(cosine_similarity(vectorized,value).flatten())
        if cur_score>max_score:
            max_score=cur_score
            maxidx=idx
    tag=""       
    if max_score>=0.3:
        tag=tags[maxidx]
    else:
        tag=tags[6]
    rep=randome(data["intents"][tag]["responses"])
    #print(f"{tag} \n {rep}")
    
    return rep
    
    
    
    


if __name__=="__main__":
    #for testing
    dataf={}
    with open("intents.json",encoding="utf-8") as f:
        dataf=json.load(f)
    
    tags,patt=init_data()
    tf=TfidfVectorizer(tokenizer=custom_tokenized,lowercase=True)
    fitted=formvectorized(tf,patt)
    usr="tôi muốn làm ca sĩ"
    response(tf,fitted,usr.strip(),tags)