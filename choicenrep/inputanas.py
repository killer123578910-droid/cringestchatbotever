import json
import re
import unicodedata
import random
data={}
with open("intents.json",encoding="utf-8") as f:
    data=json.load(f)

def randome(rep):
    return random.choice(rep)
#nomalize texts and remove sign by unicode
#working like a map, eX: 17 denominations of A will be translate into A, while Đ just need to turn into D, same will lowercase
BANG_XOA_DAU = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A"*17 + "D" + "E"*11 + "I"*5 + "O"*17 + "U"*11 + "Y"*5 + "a"*17 + "d" + "e"*11 + "i"*5 + "o"*17 + "u"*11 + "y"*5
)

def xoa_dau(txt: str) -> str:
    if not unicodedata.is_normalized("NFC", txt):
        txt = unicodedata.normalize("NFC", txt)
    return txt.translate(BANG_XOA_DAU)

#chunk comparing: compare word by word for each tag and calculate the intersection,the tag with the highest inter will be chosen
#when overlap,the first encounter(priortized by position in json) will be chosen
def takingtag(data,user):   
    tag_point={}
    for intent in data["intents"]:
        max_point=0
        for k in data["intents"][intent]["patterns"]:
            cur_point=len(set(k)&set(user))
            if max_point<cur_point:
                max_point=cur_point 
        tag_point[intent]=max_point
    tagvalue=max(tag_point.values())
    tag=max(tag_point,key=tag_point.get)
    return "fallback" if tagvalue==0 else tag

def response(data,user):
    userp=xoa_dau(user)

    #split by regex
    userp=re.split("\W+",userp)
    
    
    intents=data['intents']
    response=randome(intents[takingtag(data,userp)]["responses"])
    return response
if __name__=="__main__":
    #stripinput
    user_input=input().lower().strip()
    print(response(data,user_input))
    f.close()
            
        