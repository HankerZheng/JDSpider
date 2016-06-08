import json

def load_config():
    with open('config.txt') as f:
        configs = json.loads(f.read())
    return configs

configs = load_config()