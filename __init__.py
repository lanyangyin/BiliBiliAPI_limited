# coding=utf-8
from tool import config_B, qr_encode, dict2cookieformat
from login import generate, poll
from special import master
import asyncio


async def start_login(uid: int = 0, dirname: str = "Biliconfig"):
    """
    扫码登陆获得cookies
    :param uid: 登陆的账号的uid，为0时使用记录中默认的，会使用上一次正常登陆的账号作为默认
    :param dirname: 文件保存目录
    :return: dict
    """
    # 获取uid对应的cookies
    configb = config_B(uid=uid, dirname=dirname)
    cookies = configb.check()
    # 尝试使用存录的cookies登录
    islogin = master(dict2cookieformat(cookies)).interface_nav()["isLogin"]
    if islogin:
        # 记录到默认登录字段
        configb = config_B(uid=0, dirname=dirname)
        configb.update(cookies)
        return {'uid': int(cookies['DedeUserID']), 'cookies': cookies, 'cookie': dict2cookieformat(cookies)}
    else:  # cookies无法登录或者没有记录所填的uid
        # 申请登录二维码
        url8qrcode_key = generate()
        url = url8qrcode_key['url']
        # 获取二维码
        qr = qr_encode(url)
        # 输出二维码图形字符串
        print(qr["str"])
        # 获取二维码key
        qrcode_key = url8qrcode_key['qrcode_key']
        # 获取二维码扫描登陆状态
        code = poll(qrcode_key)['code']
        print(code)

        # 轮询二维码扫描登录状态
        async def check_poll(code):
            """
            二维码扫描登录状态检测
            @param code: 一个初始的状态，用于启动轮询
            @return: cookies，超时为{}
            """
            while True:
                code_ = code
                poll_ = poll(qrcode_key)
                code = poll_['code']
                if code_ != code:
                    # 二维码扫描登陆状态改变时，输出改变后状态
                    print(code)
                    pass
                if code == 0 or code == 86038:
                    # 二维码扫描登陆状态为成功或者超时时获取cookies结束[轮询二维码扫描登陆状态]
                    cookies = poll_['cookies']
                    break
            return cookies

        cookies = await check_poll(code)

    if cookies:
        # 获取登陆账号cookies中携带的uid
        uid = int(cookies['DedeUserID'])
        # 记录
        configb = config_B(uid=uid, dirname=dirname)
        configb.update(cookies)
        # 记录到默认登录字段
        configb = config_B(uid=0, dirname=dirname)
        configb.update(cookies)
    return {'uid': int(cookies['DedeUserID']), 'cookies': cookies, 'cookie': dict2cookieformat(cookies)}


login_info = asyncio.run(start_login(143474500))
# print(cookies)
