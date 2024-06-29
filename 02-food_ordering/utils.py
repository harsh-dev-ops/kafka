import json

def json_encoder(data:dict|list):
    return json.dumps(data).encode("utf-8")

def json_decoder(data:bytes|str):
    return json.loads(data)