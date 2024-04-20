# coding=utf-8
import json

import requests

debug = True
debugnum = 0

def print_debug(content, _:bool = debug):
    global debugnum
    debugnum = debugnum + 1
    if _:
        print(debugnum, content)

def update_config(uid:int, cookie:str):
    global debugnum
    debugnum = 0
    with open('config.json', 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
            print_debug(config)
            config[str(uid)] = cookie
            print_debug(config)
        except:
            config = dict()
            config[str(uid)] = cookie
    print_debug(config)
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print_debug(config)

update_config(1, "")
