# coding=utf-8
import sys
import time
from io import StringIO
from urllib.parse import quote, unquote

import qrcode

debug = False
debug_num = 0


def print_debug(content, _: bool = debug):
    global debug_num
    debug_num = debug_num + 1
    if _:
        print(debug_num, content)


def time_encode(dt) -> float:
    """
    将 "%Y-%m-%d %H:%M:%S" 格式的时间字符串转换成时间戳
    :param dt: "%Y-%m-%d %H:%M:%S"
    :return: 时间戳
    """
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp


def time_format(t: float) -> str:
    """
    将 时间戳 格式化为 "%Y-%m-%d %H:%M:%S"
    :param t: 时间戳
    :return: "%Y-%m-%d %H:%M:%S"
    """
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return time_string


print_debug(time_encode("2024-03-21 17:53:24"))
print_debug(time_format(time_encode("2024-03-21 17:53:24")))


def qr_encode(qr_str: str, border: int = 2, invert: bool = False) -> str:
    # 创建一个 StringIO 对象来捕获 print 输出
    output = StringIO()
    sys.stdout = output
    qr = qrcode.QRCode()
    qr.border = border
    qr.add_data(qr_str)
    qr.make()
    qr.print_ascii(out=None, tty=False, invert=invert)
    # 重定向输出到变量中
    output_str = output.getvalue()
    # 恢复 sys.stdout
    sys.stdout = sys.__stdout__
    return output_str


print_debug(qr_encode('https://txz.qq.com/p?k=EDDit-xHaBeBrZmB0ZSiWYvp1OgI2loq&f=1600001602'))


def urldata_dict(url: str) -> dict:
    """
    将url参数转换成dict
    :param url: 带有参数的url
    :return: 转换成的dict
    """
    urldata = url.split('?',1)[1]
    data_list = urldata.split('&')
    data_dict = {}
    for data in data_list:
        data = data.split('=')
        data_dict[data[0]] = data[1]
    return data_dict



print_debug(urldata_dict('https://passport.biligame.com/x/passport-login/web/crossDomain?DedeUserID=143474500&DedeUserID__ckMd5=7d59d5cc4d178400&Expires=1729193932&SESSDATA=3d5dd2c2,1729193932,b1217*41CjArtWqP5q3E5GigFZnLjLkswOq3mkL9C1pRtD_p_eBBRb_7oC0t-46HstTY3SfRlhQSVnNHQWFpWDFQZ0F3OHpWWE5XZmg2MXhSZXBvZng1UlFIX3lFQ28yRW4wbkotbGo2OFZPVHdsSWsxNVpUakJPUzR6OGNPMnotT0dpRDg5bDdPb3FzNkR3IIEC&bili_jct=2a9a95c3a7b2d39230b783a7c5e7eb49&gourl=https%3A%2F%2Fwww.bilibili.com&first_domain=.bilibili.com'))


def url_decoded(url_string):
    """
    将 UTF-8 解码成 URL编码
    :param url_string: 要解码的 UTF-8 编码字符串
    :return: URL编码
    """
    # 使用quote()函数将URL编码转换为UTF-8
    utf8_encoded = quote(url_string, encoding='utf-8')
    return utf8_encoded


def url_encoded(encoded_string):
    """
    将URL编码转换为 UTF-8 编码字符串
    :param encoded_string: 要编码的字符串
    :return: UTF-8 编码字符串
    """
    # 使用 unquote() 函数解码为原始字符串
    decoded_string = unquote(encoded_string, encoding='utf-8')
    return decoded_string


print_debug(url_encoded("DedeUserID=143474500&DedeUserID__ckMd5=7d59d5cc4d178400&Expires=1729193932&SESSDATA=3d5dd2c2,1729193932,b1217*41CjArtWqP5q3E5GigFZnLjLkswOq3mkL9C1pRtD_p_eBBRb_7oC0t-46HstTY3SfRlhQSVnNHQWFpWDFQZ0F3OHpWWE5XZmg2MXhSZXBvZng1UlFIX3lFQ28yRW4wbkotbGo2OFZPVHdsSWsxNVpUakJPUzR6OGNPMnotT0dpRDg5bDdPb3FzNkR3IIEC&bili_jct=2a9a95c3a7b2d39230b783a7c5e7eb49&gourl=https%3A%2F%2Fwww.bilibili.com&first_domain=.bilibili.com',"))


