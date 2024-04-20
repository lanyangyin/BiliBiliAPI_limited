# coding=utf-8
# 只能二维码
import json
import sys
import time

import requests
from tool import qr_encode, urldata_dict

debug = False
debug_num = 0
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
}


def print_debug(content, _: bool = debug):
    global debug_num
    debug_num = debug_num + 1
    if _:
        print(debug_num, content)


def update_config(uid: int, cookie: str):
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


print_debug(update_config(1, ""))


def generate():
    """
    申请二维码
    https://passport.bilibili.com/x/passport-login/web/qrcode/generate
    :return:{'url': 二维码文本, 'qrcode_key': 扫描秘钥}
    """
    api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
    try:
        url8qrcode_key = requests.get(api, headers=headers).json()
        print_debug(url8qrcode_key)
        data = url8qrcode_key['data']
        url = data['url']
        qrcode_key = data['qrcode_key']
    except:
        url = ""
        qrcode_key = ""
    return {'url': url, 'qrcode_key': qrcode_key}


print_debug(generate())


def poll(qrcode_key: str):
    """
    登陆状态
    https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}
    :param qrcode_key:扫描秘钥
    :return: {'code': code, 'cookies': {'DedeUserID': DedeUserID, 'DedeUserID__ckMd5': DedeUserID__ckMd5, 'SESSDATA': SESSDATA, 'csrf': bili_jct}}
    """
    global data
    api = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}'
    try:
        DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct = requests.get(api, data=qrcode_key, headers=headers).json()
        data = DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct['data']
        print_debug(data)
        code = data['code']
        data_dict = urldata_dict(data['url'])
        DedeUserID = data_dict['DedeUserID']
        DedeUserID__ckMd5 = data_dict['DedeUserID__ckMd5']
        SESSDATA = data_dict['SESSDATA']
        bili_jct = data_dict['bili_jct']
    except:
        try:
            code = data['code']
        except:
            code = ''
        DedeUserID = ''
        DedeUserID__ckMd5 = ''
        SESSDATA = ''
        bili_jct = ''
    return {'code': code, 'cookies': {'DedeUserID': DedeUserID, 'DedeUserID__ckMd5': DedeUserID__ckMd5, 'SESSDATA': SESSDATA, 'csrf': bili_jct}}


print_debug(poll(generate()['qrcode_key']))

