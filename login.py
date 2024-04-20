# coding=utf-8
import json
import sys
import time

import requests

debug = True
debug_num = 0


def print_debug(content, _:bool = debug):
    global debug_num
    debug_num = debug_num + 1
    if _:
        print(debug_num, content)


def update_config(uid:int, cookie:str):
    global debug_num
    debug_num = 0
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            inputconfig = config
            print_debug(inputconfig)
            config[str(uid)] = cookie
            outputconfig = config
            print_debug(outputconfig)
            inconfig_isjson = True
    except:
        with open('config.json', 'r', encoding='utf-8') as f:
            inputconfig = f.read()
            outputconfig = dict()
            outputconfig[str(uid)] = cookie
            inconfig_isjson = False
            print_debug(inputconfig)
    if not inconfig_isjson:
        with open(str(time.strftime("%Y%m%d%H%M%S")) + '_config.json', 'w', encoding='utf-8') as f:
            f.write(inputconfig)
            print_debug(inputconfig)
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(outputconfig, f, ensure_ascii=False, indent=4)
    print_debug(outputconfig)


update_config(1, "")
