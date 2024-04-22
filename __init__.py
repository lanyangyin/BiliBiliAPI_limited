# coding=utf-8
from .tool import check_config, qr_encode, update_config, dict2cookieformat
from .login import generate, poll, get_buvid3


def start_login(usernum: int = 0):
    """
    扫码登陆获得cookies
    :param usernum:
    :return:
    """
    uid = ''
    cookies = {}
    try:
        config = check_config()
        uid = list(config.keys())[usernum]
        cookies = list(config.values())[usernum]
    except:
        url8qrcode_key = generate()
        url = url8qrcode_key['url']
        print(qr_encode(url))
        qrcode_key = url8qrcode_key['qrcode_key']
        code = poll(qrcode_key)['code']
        print(code)
        while True:
            code_ = code
            poll_ = poll(qrcode_key)
            code = poll_['code']
            if code_ != code:
                print(code)
            if code == 0 or code == 86038:
                break
        try:
            cookies = poll_['cookies']
            uid = cookies['DedeUserID']
        except:
            pass
    cookies.update(get_buvid3()['cookies'])
    if uid != '':
        update_config(uid, cookies)
    return dict2cookieformat(cookies)



