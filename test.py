import json

with open("intents.json", encoding="utf-8") as f:
    data = json.load(f)

for intent in data["intents"]:
    intent["patterns"] = [
        pattern.split()
        for pattern in intent["patterns"]
    ]

with open("intents.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
