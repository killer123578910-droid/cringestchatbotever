import json

with open("intents.json", encoding="utf-8") as f:
    data = json.load(f)
    for intents in data["intents"]:
        print(intents["patterns"])
