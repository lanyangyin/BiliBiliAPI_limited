# coding=utf-8
import sys
import time
from io import StringIO

import qrcode

debug = True
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


def qr_encode(str: str, border: int = 1, invert: bool = False) -> str:
    # 创建一个空的StringIO对象
    output = StringIO()
    qr = qrcode.QRCode()
    qr.border = border
    qr.add_data(str)
    qr.make()
    qr.print_ascii(out=None, tty=False, invert=invert)
    # 将标准输出重定向到StringIO对象
    sys.stdout = output
    result = output.getvalue()
    return result


print_debug(qr_encode('https://txz.qq.com/p?k=EDDit-xHaBeBrZmB0ZSiWYvp1OgI2loq&f=1600001602'))

