import json

tags=["greetings","g_info","services_prices","utils","terms_cond","goodbye"]
data={"ts":[]}
for t in tags:
    data["ts"].append({"tag":t})
with open("intents.json","w") as f:
    f.write(json.dumps(data))
