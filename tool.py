# coding=utf-8
import base64
import html
import io
import json
import os
import sys
import time
from io import StringIO
from typing import Dict, Any
from urllib.parse import quote, unquote

import qrcode
from qrcode.image.pil import PilImage


class config_B:
    """
    配置文件 config.json 的 查找 和 更新
    """

    def __init__(self, uid: int, dirname: str = "Bili_config"):
        """
        @param uid: 用户id
        @param dirname: 配置文件 config.json 所在文件夹名
        """
        # 字符串化UID
        self.uid = str(uid)
        # 配置文件 config.json 路径
        self.configpath = f'.\\{dirname}\\config.json'
        if not os.path.exists(".\\" + dirname):
            os.makedirs(dirname)

    def update(self, cookies: dict):
        """
        记录uid和cookie到配置文件 config.json 中
        @param cookies: 登录获取的 cookies，字段来自 cookie
        """
        uid = self.uid
        # 配置文件 config.json 路径
        configpath = self.configpath
        # 判断配置文件 config.json 是否存在，不存在则创建一个初始配置文件
        try:
            with open(configpath, 'r', encoding='utf-8') as f:
                f.read()
        except:
            with open(configpath, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        # 判断配置文件 config.json 是否符合json格式，符合则更新 uid 对应的 cookie，不符合则备份违规文件并覆写 uid 对应的 cookie
        try:
            with open(configpath, 'r', encoding='utf-8') as f:
                config = json.load(f)
                config[uid] = cookies
                outputconfig = config
        except:
            with open(configpath, 'r', encoding='utf-8') as f:
                inputconfig = f.read()
                outputconfig = {uid: cookies}
            # 备份违规文件
            with open(str(time.strftime("%Y%m%d%H%M%S")) + '_config.json', 'w', encoding='utf-8') as f:
                f.write(inputconfig)
        # 更新uid和cookie到配置文件 config.json 中
        with open(configpath, 'w', encoding='utf-8') as f:
            json.dump(outputconfig, f, ensure_ascii=False, indent=4)

    def check(self) -> dict:
        """
        查询配置文件中保存的 uid 对应的 cookies，没有则为空字符
        @return: uid 对应的 cookies
        """
        cookies = {}
        try:
            with open(self.configpath, 'r', encoding='utf-8') as f:
                cookies = json.load(f)[self.uid]
        except:
            pass
        return cookies


def time_encode(dt) -> float:
    """
    将 "%Y-%m-%d %H:%M:%S" 格式的时间字符串转换成unix时间戳
    @param dt: "%Y-%m-%d %H:%M:%S"格式的时间
    @return: unix时间戳
    """
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp


def time_format(t: float) -> str:
    """
    将 unix时间戳 格式化为 "%Y-%m-%d %H:%M:%S"
    @param t: unix时间戳
    @return: "%Y-%m-%d %H:%M:%S"
    """
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return time_string


# print(time_encode("2024-03-21 17:53:24"))
# print(time_format(1714072323))


def qr_encode(qr_str: str, border: int = 2, invert: bool = False):
    """
    字符串转二维码
    @param qr_str: 二维码文本
    @param border: 边框大小
    @param invert: 黑白底转换
    @return: {"str": output_str, "base64": b64, "img": img}
    @rtype: dict[str, str, PilImage]
    """
    # 保存了当前的标准输出（stdout）
    savestdout = sys.stdout
    # 创建一个 StringIO 对象来捕获 print 输出
    output = StringIO()
    # 将系统的标准输出重定向到 output
    sys.stdout = output
    # 创建了一个 QRCode 对象 qr
    qr = qrcode.QRCode(
        version=1,  # 版本
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 纠错级别
        box_size=10,  # 方块大小
        border=border,  # 边框大小
    )
    # 将要转换的文本 qr_str 添加到二维码中
    qr.make(fit=True)
    qr.add_data(qr_str)
    # 生成二维码图像对象 img
    img = qr.make_image()
    # 将 Pillow 图像对象保存到一个内存中的字节流 buf 中
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    image_stream = buf.getvalue()
    # 将其转换为 PNG 格式的二进制流
    heximage = base64.b64encode(image_stream)
    # 使用 base64 编码转换成字符串 b64
    b64 = heximage.decode()
    # 使用 qr 对象的 print_ascii 方法将二维码以 ASCII 字符串的形式打印出来，并根据 invert 参数的值决定是否反转黑白颜色
    qr.print_ascii(out=None, tty=False, invert=invert)
    # 重定向输出到变量中
    output_str = output.getvalue()
    # 恢复 sys.stdout
    sys.stdout = savestdout
    out = {"str": output_str, "base64": b64, "img": img}
    return out


# qr = {}
# qr = qr_encode('你好')
# print(qr["str"], qr["base64"], type(qr["img"]))


def urldata_dict(url: str):
    """
    将 url参数 转换成 dict
    @param url: 带有参数的url
    @return: 转换成的dict
    @rtype: dict
    """
    urldata = url.split('?', 1)[1]
    data_list = urldata.split('&')
    data_dict = {}
    for data in data_list:
        data = data.split('=')
        data_dict[data[0]] = data[1]
    return data_dict


# print(urldata_dict('https://passport.biligame.com/x/passport-login/web/crossDomain?DedeUserID=143474500&DedeUserID__ckMd5=7d59d5cc4d178400&Expires=1729193932&SESSDATA=3d5dd2c2,1729193932,b1217*41CjArtWqP5q3E5GigFZnLjLkswOq3mkL9C1pRtD_p_eBBRb_7oC0t-46HstTY3SfRlhQSVnNHQWFpWDFQZ0F3OHpWWE5XZmg2MXhSZXBvZng1UlFIX3lFQ28yRW4wbkotbGo2OFZPVHdsSWsxNVpUakJPUzR6OGNPMnotT0dpRDg5bDdPb3FzNkR3IIEC&bili_jct=2a9a95c3a7b2d39230b783a7c5e7eb49&gourl=https%3A%2F%2Fwww.bilibili.com&first_domain=.bilibili.com'))


def url_decoded(url_string: str) -> str:
    """
    将 UTF-8 解码成 URL编码
    @param url_string: 要解码的 UTF-8 编码字符串
    @return: URL编码
    """
    # 使用quote()函数将URL编码转换为UTF-8
    utf8_encoded = quote(url_string, encoding='utf-8')
    return utf8_encoded


def url_encoded(encoded_string: str) -> str:
    """
    将 URL编码 转换为 UTF-8 编码字符串
    @param encoded_string: 要编码的字符串
    @return: UTF-8 编码字符串
    """
    # 使用 unquote() 函数解码为原始字符串
    decoded_string = unquote(encoded_string, encoding='utf-8')
    return decoded_string


# print(url_encoded("DedeUserID=143474500&DedeUserID__ckMd5=7d59d5cc4d178400&Expires=1729193932&SESSDATA=3d5dd2c2,1729193932,b1217*41CjArtWqP5q3E5GigFZnLjLkswOq3mkL9C1pRtD_p_eBBRb_7oC0t-46HstTY3SfRlhQSVnNHQWFpWDFQZ0F3OHpWWE5XZmg2MXhSZXBvZng1UlFIX3lFQ28yRW4wbkotbGo2OFZPVHdsSWsxNVpUakJPUzR6OGNPMnotT0dpRDg5bDdPb3FzNkR3IIEC&bili_jct=2a9a95c3a7b2d39230b783a7c5e7eb49&gourl=https%3A%2F%2Fwww.bilibili.com&first_domain=.bilibili.com',"))


def dict2cookieformat(jsondict: dict) -> str:
    """
    将 dict 转换为 cookie格式
    @param jsondict: 字典
    @return: cookie格式的字典
    """
    cookie = ''
    for json_dictK in jsondict:
        json_dictki = json_dictK
        json_dictVi = jsondict[json_dictki]
        cookie += url_decoded(str(json_dictki)) + '=' + url_decoded(str(json_dictVi)) + '; '
    cookie = cookie.strip()
    if cookie.endswith(";"):
        cookie = cookie[:-1]
    return cookie


# print(dict2cookieformat({'0': '9&0', "8": 8}))


def html_decoded(htmlstr: str) -> str:
    """
    将 UTF-8字符串 转义为 HTML实体字符
    @param htmlstr: 要转义的字符串
    @return: 转义为的 HTML实体字符
    """
    # 将UTF-8字符串转义为HTML实体字符
    escaped_string = html.escape(htmlstr, quote=True)
    return escaped_string


def html_encoded(encoded_string: str) -> str:
    """
    将 HTML实体字符 解码为 UTF-8字符串
    @param encoded_string: 包含HTML实体字符的字符串
    @return: UTF-8字符串
    """
    # 将HTML实体字符解码为UTF-8字符串
    decoded_string = html.unescape(encoded_string)
    return decoded_string


def file2b64(filepath: str):
    """
    文件 转 base64
    @param filepath: 文件路径
    @return: base64 编码
    @rtype: str
    """
    with open(filepath, 'rb') as f1:
        # base64类型
        base64_str = base64.b64encode(f1.read())
        # str
        src = base64_str.decode('utf-8')
        # print(src)
        return src
