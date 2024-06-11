# class tool:
# coding=utf-8
import asyncio
import base64
import html
import io
import json
import os
import sys
from io import StringIO
from urllib.parse import quote, unquote
from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests
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
            os.makedirs(dirname, exist_ok=True)

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
        @return: uid 对应的 cookies ，uid 不存在会返回{}
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
# print(time_format(1714660247))


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
    img.save(buf)  # , format='PNG'
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


def dict2url(dictV: dict):
    # 将字典形式的参数转换为URL编码的字符串
    return urllib.parse.urlencode(dictV)


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


def creatfile(filepath: str, data: str = "file"):
    """
    文件不存在时创建
    @param filepath: 文件路径
    @param data: 是 "config" 时生成空json内容
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
    except:
        if data == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('')


def wbi(data: dict):
    """
    WBI 签名
    @param data: 需要 wbi签名 的 params 参数
    @return: requests的 params 参数
    @rtype: dict
    """
    mixinKeyEncTab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]

    def getMixinKey(orig: str):
        """对 imgKey 和 subKey 进行字符顺序打乱编码"""
        return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

    def encWbi(params: dict, img_key: str, sub_key: str):
        """为请求参数进行 wbi 签名"""
        mixin_key = getMixinKey(img_key + sub_key)
        curr_time = round(time.time())
        params['wts'] = curr_time  # 添加 wts 字段
        params = dict(sorted(params.items()))  # 按照 key 重排参数
        # 过滤 value 中的 "!'()*" 字符
        params = {
            k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
            for k, v
            in params.items()
        }
        query = urllib.parse.urlencode(params)  # 序列化参数
        wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
        params['w_rid'] = wbi_sign
        return params

    def getWbiKeys() -> tuple[str, str]:
        """获取最新的 img_key 和 sub_key"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        }
        resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
        resp.raise_for_status()
        json_content = resp.json()
        img_url: str = json_content['data']['wbi_img']['img_url']
        sub_url: str = json_content['data']['wbi_img']['sub_url']
        img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        return img_key, sub_key

    img_key, sub_key = getWbiKeys()

    signed_params = encWbi(
        params=data,
        img_key=img_key,
        sub_key=sub_key
    )
    return signed_params


def b64_file(base64_string: str, file_path: str):
    """
    将Base64编码的字符串转换回文件
    @param base64_string:Base64编码的字符串
    @param file_path:目标文件路径
    """
    # 解码Base64字符串
    decoded_data = base64.b64decode(base64_string)
    # 将解码后的数据写入文件
    with open(file_path, "wb") as f:
        f.write(decoded_data)


# 定义一个异步函数，用来等待文件出现
async def wait_for_file(path, timeout=60):
    start_time = time.time()  # 记录等待开始的时间
    while not os.path.exists(path):  # 循环检查文件是否存在
        if time.time() - start_time > timeout:  # 如果等待时间超过指定的超时时间
            raise TimeoutError("Timeout while waiting for file")  # 抛出超时异常
        await asyncio.sleep(1)  # 等待1秒钟再次检查文件是否存在
    return path  # 当文件出现后，返回文件路径


# login
# coding=utf-8
# 只能二维码登录
import json
import re

import requests

debug = False
debug_num = 0
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
}


def generate() -> dict:
    """
    申请登录二维码
    @return: {'url': 二维码文本, 'qrcode_key': 扫描秘钥}
    """
    api = 'https://passport.bilibili.com/x/passport-login/web/qrcode/generate'
    url8qrcode_key = requests.get(api, headers=headers).json()
    # print(url8qrcode_key)
    data = url8qrcode_key['data']
    url = data['url']
    qrcode_key = data['qrcode_key']
    return {'url': url, 'qrcode_key': qrcode_key}


# print(generate())


def poll(qrcode_key: str) -> dict[str, dict[str, str] | int]:
    """
    获取登陆状态，登陆成功获取 基础的 cookies
    @param qrcode_key: 扫描秘钥
    @return: {'code', 'cookies'}
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>code</td>
            <td>num</td>
            <td>0：扫码登录成功<br>86038：二维码已失效<br>86090：二维码已扫码未确认<br>86101：未扫码</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    @rtype: dict
    """
    global data
    api = f'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}'
    DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct = requests.get(api, data=qrcode_key, headers=headers).json()
    data = DedeUserID8DedeUserID__ckMd58SESSDATA8bili_jct['data']
    # print(data)
    cookies = {}
    code = data['code']
    if code == 0:
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

        data_dict = urldata_dict(data['url'])
        cookies["DedeUserID"] = data_dict['DedeUserID']
        cookies["DedeUserID__ckMd5"] = data_dict['DedeUserID__ckMd5']
        cookies["SESSDATA"] = data_dict['SESSDATA']
        cookies["bili_jct"] = data_dict['bili_jct']
        # 补充 cookie
        buvid3 = requests.get(f'https://www.bilibili.com/video/', headers=headers)
        cookies.update(buvid3.cookies.get_dict())
    return {'code': code, 'cookies': cookies}


# print(poll(""))


def get_buvid3(bvid: str = 'BV16F411c7CR') -> dict:
    """
    通过视频BV号获取cookie部分参数
    :param bvid: BV号
    :return:  {'cookies': cookies, 'data_dict': data_dict, 'session': sessionId}
    """
    response = requests.get(f'https://www.bilibili.com/video/{bvid}/', headers=headers)
    cookies = response.cookies.get_dict()
    data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', response.text)  # .表示除换行符所有字符，+ 表示一个或者多个
    try:
        data_dict = json.loads(data_list[0])  # 结果长得像字典， 就用python中反序列化转成json格式
        sessionId = re.findall(r'session":"(.+)"}</script', response.text)[0]
    except:
        data_dict = ''
        sessionId = ''
    return {'cookies': cookies, 'data_dict': data_dict, 'session': sessionId}


# print_debug(get_buvid3())


# normal
# coding=utf-8
import pprint

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
}


def getRoomInfoOld(mid: int) -> dict:
    """
    直接用Bid查询到的直播间基础信息<br>
    @param mid: B站UID
    @type mid: int
    @return:
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>roomStatus</td>
            <td>num</td>
            <td>直播间状态</td>
            <td>0：无房间<br>1：有房间</td>
        </tr>
        <tr>
            <td>roundStatus</td>
            <td>num</td>
            <td>轮播状态</td>
            <td>0：未轮播<br>1：轮播</td>
        </tr>
        <tr>
            <td>liveStatus</td>
            <td>num</td>
            <td>直播状态</td>
            <td>0：未开播<br>1：直播中</td>
        </tr>
        <tr>
            <td>url</td>
            <td>str</td>
            <td>直播间网页url</td>
            <td></td>
        </tr>
        <tr>
            <td>title</td>
            <td>str</td>
            <td>直播间标题</td>
            <td></td>
        </tr>
        <tr>
            <td>cover</td>
            <td>str</td>
            <td>直播间封面url</td>
            <td></td>
        </tr>
        <tr>
            <td>online</td>
            <td>num</td>
            <td>直播间人气</td>
            <td>值为上次直播时刷新</td>
        </tr>
        <tr>
            <td>roomid</td>
            <td>num</td>
            <td>直播间id（短号）</td>
            <td></td>
        </tr>
        <tr>
            <td>broadcast_type</td>
            <td>num</td>
            <td>0</td>
            <td></td>
        </tr>
        <tr>
            <td>online_hidden</td>
            <td>num</td>
            <td>0</td>
            <td></td>
        </tr>
        </tbody>
    </table>
    @rtype: dict
    """
    api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
    data = {
        "mid": mid,
    }
    RoomInfoOld = requests.get(api, headers=headers, params=data).json()
    return RoomInfoOld["data"]


# pprint.pprint(getRoomInfoOld(67141))


def v1_Room_get_info(room_id: int) -> dict:
    """
    用直播间号查询到的直播间基础信息<br>
    @param room_id:直播间号
    @type room_id: int
    @return:
    <table>
        <thead>
        <tr>
            <th>字段</th>
            <th>类型</th>
            <th>内容</th>
            <th>备注</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>uid</td>
            <td>num</td>
            <td>主播mid</td>
            <td></td>
        </tr>
        <tr>
            <td>room_id</td>
            <td>num</td>
            <td>直播间长号</td>
            <td></td>
        </tr>
        <tr>
            <td>short_id</td>
            <td>num</td>
            <td>直播间短号</td>
            <td>为0是无短号</td>
        </tr>
        <tr>
            <td>attention</td>
            <td>num</td>
            <td>关注数量</td>
            <td></td>
        </tr>
        <tr>
            <td>online</td>
            <td>num</td>
            <td>观看人数</td>
            <td></td>
        </tr>
        <tr>
            <td>is_portrait</td>
            <td>bool</td>
            <td>是否竖屏</td>
            <td></td>
        </tr>
        <tr>
            <td>description</td>
            <td>str</td>
            <td>描述</td>
            <td></td>
        </tr>
        <tr>
            <td>live_status</td>
            <td>num</td>
            <td>直播状态</td>
            <td>0：未开播<br>1：直播中<br>2：轮播中</td>
        </tr>
        <tr>
            <td>area_id</td>
            <td>num</td>
            <td>分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>parent_area_id</td>
            <td>num</td>
            <td>父分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>parent_area_name</td>
            <td>str</td>
            <td>父分区名称</td>
            <td></td>
        </tr>
        <tr>
            <td>old_area_id</td>
            <td>num</td>
            <td>旧版分区id</td>
            <td></td>
        </tr>
        <tr>
            <td>background</td>
            <td>str</td>
            <td>背景图片链接</td>
            <td></td>
        </tr>
        <tr>
            <td>title</td>
            <td>str</td>
            <td>标题</td>
            <td></td>
        </tr>
        <tr>
            <td>user_cover</td>
            <td>str</td>
            <td>封面</td>
            <td></td>
        </tr>
        <tr>
            <td>keyframe</td>
            <td>str</td>
            <td>关键帧</td>
            <td>用于网页端悬浮展示</td>
        </tr>
        <tr>
            <td>is_strict_room</td>
            <td>bool</td>
            <td>未知</td>
            <td>未知</td>
        </tr>
        <tr>
            <td>live_time</td>
            <td>str</td>
            <td>直播开始时间</td>
            <td>YYYY-MM-DD HH:mm:ss</td>
        </tr>
        <tr>
            <td>tags</td>
            <td>str</td>
            <td>标签</td>
            <td>','分隔</td>
        </tr>
        <tr>
            <td>is_anchor</td>
            <td>num</td>
            <td>未知</td>
            <td>未知</td>
        </tr>
        <tr>
            <td>room_silent_type</td>
            <td>str</td>
            <td>禁言状态</td>
            <td></td>
        </tr>
        <tr>
            <td>room_silent_level</td>
            <td>num</td>
            <td>禁言等级</td>
            <td></td>
        </tr>
        <tr>
            <td>room_silent_second</td>
            <td>num</td>
            <td>禁言时间</td>
            <td>单位是秒</td>
        </tr>
        <tr>
            <td>area_name</td>
            <td>str</td>
            <td>分区名称</td>
            <td></td>
        </tr>
        <tr>
            <td>pardants</td>
            <td>str</td>
            <td>未知</td>
            <td>未知</td>
        </tr>
        <tr>
            <td>area_pardants</td>
            <td>str</td>
            <td>未知</td>
            <td>未知</td>
        </tr>
        <tr>
            <td>hot_words</td>
            <td>list(str)</td>
            <td>热词</td>
            <td></td>
        </tr>
        <tr>
            <td>hot_words_status</td>
            <td>num</td>
            <td>热词状态</td>
            <td></td>
        </tr>
        <tr>
            <td>verify</td>
            <td>str</td>
            <td>未知</td>
            <td>未知</td>
        </tr>
        <tr>
            <td>new_pendants</td>
            <td>obj</td>
            <td>头像框\大v</td>
            <td></td>
        </tr>
        <tr>
            <td>up_session</td>
            <td>str</td>
            <td>未知</td>
            <td></td>
        </tr>
        <tr>
            <td>pk_status</td>
            <td>num</td>
            <td>pk状态</td>
            <td></td>
        </tr>
        <tr>
            <td>pk_id</td>
            <td>num</td>
            <td>pk id</td>
            <td></td>
        </tr>
        <tr>
            <td>battle_id</td>
            <td>num</td>
            <td>未知</td>
            <td></td>
        </tr>
        <tr>
            <td>allow_change_area_time</td>
            <td>num</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>allow_upload_cover_time</td>
            <td>num</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>studio_info</td>
            <td>obj</td>
            <td></td>
            <td></td>
        </tr>
        </tbody>
    </table>
    @rtype:dict
    """
    api = "https://api.live.bilibili.com/room/v1/Room/get_info"
    data = {
        "room_id": room_id,
    }
    v1_Room_info = requests.get(api, headers=headers, params=data).json()
    return v1_Room_info["data"]


# pprint.pprint(v1_Room_get_info(213))

def v2_index_getRoomPlayInfo(room_id: int):
    """
    直播间获取到的，不知道是啥
    @param room_id:
    @return:
    "data": {
        "room_id": 22966160,
        "short_id": 0,
        "uid": 1703797642,
        "is_hidden": false,
        "is_locked": false,
        "is_portrait": false,
        "live_status": 0,
        "hidden_till": 0,
        "lock_till": 0,
        "encrypted": false,
        "pwd_verified": true,
        "live_time": 0,
        "room_shield": 0,
        "all_special_types": [],
        "playurl_info": null,
        "official_type": 0,
        "official_room_id": 0,
        "risk_with_delay": 0
    }
    @rtype: dict
    """
    api = "https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo"
    data = {
        "room_id": room_id,
    }
    RoomPlayInfo = requests.get(api, headers=headers, params=data).json()
    return RoomPlayInfo["data"]


# pprint.pprint(v2_index_getRoomPlayInfo(room_id=213))

def getRoomBaseInfo(room_id: int):
    """
    直播间的
    @param room_id:
    @return:
    "data": {
    "by_uids": {

    },
    "by_room_ids": {
        "25322725": {
            "room_id": 25322725,
            "uid": 143474500,
            "area_id": 192,
            "live_status": 0,
            "live_url": "https://live.bilibili.com/25322725",
            "parent_area_id": 5,
            "title": "obsのlua插件2测试",
            "parent_area_name": "电台",
            "area_name": "聊天电台",
            "live_time": "0000-00-00 00:00:00",
            "description": "个人简介测试",
            "tags": "我的个人标签测试",
            "attention": 35,
            "online": 0,
            "short_id": 0,
            "uname": "兰阳音",
            "cover": "http://i0.hdslb.com/bfs/live/new_room_cover/c17af2dbbbdfce33888e834bdb720edbf9515f95.jpg",
            "background": "",
            "join_slide": 1,
            "live_id": 0,
            "live_id_str": "0"
        }
    }
  }
    """
    api = "https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo"
    data = {
        'room_ids': room_id,
        'req_biz': "link-center"
    }
    RoomBaseInfo = requests.get(api, headers=headers, params=data).json()
    return RoomBaseInfo["data"]


# pprint.pprint(getRoomBaseInfo(room_id=213))


def finger_spi():
    """
    不知道是啥，有点像 buvid3
    @return:
    "data": {
    'b_3': '6B3DAAB1-0715-00DE-EFD0-528483AA2A0E08946infoc',
    'b_4': 'FD202488-5C2B-0BC8-6BF9-6023C4B59C5708946-024050510-sdKnSN59x4BTPH9pWZcWMg=='
    }

    @rtype: dict
    """
    api = "https://api.bilibili.com/x/frontend/finger/spi"
    RoomPlayInfo = requests.get(api, headers=headers).json()
    return RoomPlayInfo["data"]


# pprint.pprint(finger_spi())


def Area_getList():
    """
    获取直播分区
    @return:
    <table>
    <thead>
    <tr>
        <th>字段</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>code</td>
        <td>num</td>
        <td>返回值</td>
        <td>0：成功</td>
    </tr>
    <tr>
        <td>msg</td>
        <td>str</td>
        <td>错误信息</td>
        <td>默认为success</td>
    </tr>
    <tr>
        <td>message</td>
        <td>str</td>
        <td>错误信息</td>
        <td>默认为success</td>
    </tr>
    <tr>
        <td>data</td>
        <td>array</td>
        <td>父分区列表</td>
        <td></td>
    </tr>
    </tbody>
</table>
<p><code>data</code>数组：</p>
<table>
    <thead>
    <tr>
        <th>项</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>0</td>
        <td>obj</td>
        <td>父分区1</td>
        <td></td>
    </tr>
    <tr>
        <td>n</td>
        <td>obj</td>
        <td>父分区(n+1)</td>
        <td></td>
    </tr>
    <tr>
        <td>……</td>
        <td>obj</td>
        <td>……</td>
        <td>……</td>
    </tr>
    </tbody>
</table>
<p><code>data</code>数组中的对象：</p>
<table>
    <thead>
    <tr>
        <th>字段</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>num</td>
        <td>父分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>name</td>
        <td>name</td>
        <td>父分区名</td>
        <td></td>
    </tr>
    <tr>
        <td>list</td>
        <td>list</td>
        <td>子分区列表</td>
        <td></td>
    </tr>
    </tbody>
</table>
<p><code>data</code>数组中的对象中的<code>list</code>数组：</p>
<table>
    <thead>
    <tr>
        <th>项</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>0</td>
        <td>obj</td>
        <td>子分区1</td>
        <td></td>
    </tr>
    <tr>
        <td>n</td>
        <td>obj</td>
        <td>子分区(n+1)</td>
        <td></td>
    </tr>
    <tr>
        <td>……</td>
        <td>obj</td>
        <td>……</td>
        <td>……</td>
    </tr>
    </tbody>
</table>
<p><code>list</code>数组中的对象：</p>
<table>
    <thead>
    <tr>
        <th>字段</th>
        <th>类型</th>
        <th>内容</th>
        <th>备注</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>id</td>
        <td>str</td>
        <td>子分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>parent_id</td>
        <td>str</td>
        <td>父分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>old_area_id</td>
        <td>str</td>
        <td>旧分区id</td>
        <td></td>
    </tr>
    <tr>
        <td>name</td>
        <td>str</td>
        <td>子分区名</td>
        <td></td>
    </tr>
    <tr>
        <td>act_id</td>
        <td>str</td>
        <td>0</td>
        <td><strong>作用尚不明确</strong></td>
    </tr>
    <tr>
        <td>pk_status</td>
        <td>str</td>
        <td>？？？</td>
        <td><strong>作用尚不明确</strong></td>
    </tr>
    <tr>
        <td>hot_status</td>
        <td>num</td>
        <td>是否为热门分区</td>
        <td>0：否<br>1：是</td>
    </tr>
    <tr>
        <td>lock_status</td>
        <td>str</td>
        <td>0</td>
        <td><strong>作用尚不明确</strong></td>
    </tr>
    <tr>
        <td>pic</td>
        <td>str</td>
        <td>子分区标志图片url</td>
        <td></td>
    </tr>
    <tr>
        <td>parent_name</td>
        <td>str</td>
        <td>父分区名</td>
        <td></td>
    </tr>
    <tr>
        <td>area_type</td>
        <td>num</td>
        <td></td>
        <td></td>
    </tr>
    </tbody>
</table>

    """
    api = "https://api.live.bilibili.com/room/v1/Area/getList"
    AreaList = requests.get(api, headers=headers).json()
    return AreaList["data"]


# pprint.pprint(Area_getList())


# special
# coding=utf-8
import math
import pprint
import time

import requests


class master:
    def __init__(self, cookie: str,
                 UA: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"):
        """
        完善 浏览器headers
        @param cookies: B站cookie 的 cookies
        @param UA: 浏览器User-Agent
        """
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
        }

    def getFansMembersRank(self, uid: int) -> list:
        """
        通过用户的B站uid查看他的粉丝团成员列表
        :param uid:B站uid
        :return: list元素：[{face：头像url，guard_icon：舰队职位图标url，guard_level：舰队职位 1|2|3->总督|提督|舰长，honor_icon：""，level：粉丝牌等级，medal_color_border：粉丝牌描边颜色数值为 10 进制的 16 进制值，medal_color_start：勋章起始颜色，medal_color_end：勋章结束颜色，medal_name：勋章名，name：用户昵称，score：勋章经验值，special：""，target_id：up主mid，uid：用户mid，user_rank：在粉丝团的排名}]
        """
        api = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank"
        headers = self.headers
        page = 0
        # maxpage = 1
        RankFans = []
        FansMember = True
        while FansMember:
            # while page <= maxpage:
            page += 1
            data = {
                "ruid": uid,
                "page": page,
                "page_size": 30,
            }
            try:
                FansMembersRank = requests.get(api, headers=headers, params=data).json()
            except:
                time.sleep(5)
                FansMembersRank = requests.get(api, headers=headers, params=data).json()
            # num_FansMembersRank = FansMembersRank["data"]["num"]
            # print(FansMembersRank)
            FansMember = FansMembersRank["data"]["item"]
            RankFans += FansMember
            # maxpage = math.ceil(num_FansMembersRank / 30) + 1
        return RankFans

    def dynamic_v1_feed_space(self, host_mid, all: bool = False) -> list:
        """

        @param host_mid:
        @param all:
        @return:
        <div><h1 id="获取动态列表" tabindex="-1"><a class="header-anchor" href="#获取动态列表" aria-hidden="true">#</a> 获取动态列表
        </h1>
            <blockquote><p>https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all</p></blockquote>
            <p>请求方式：<code>GET</code></p>
            <p>是否需要登录：<code>是</code></p>
            <h2 id="json回复" tabindex="-1"><a class="header-anchor" href="#json回复" aria-hidden="true">#</a> Json回复</h2>
            <h3 id="根对象" tabindex="-1"><a class="header-anchor" href="#根对象" aria-hidden="true">#</a> 根对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>code</td>
                    <td>num</td>
                    <td>响应码</td>
                    <td>0：成功<br>-101：账号未登录</td>
                </tr>
                <tr>
                    <td>message</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>ttl</td>
                    <td>num</td>
                    <td>1</td>
                    <td></td>
                </tr>
                <tr>
                    <td>data</td>
                    <td>obj</td>
                    <td>信息本体</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象" tabindex="-1"><a class="header-anchor" href="#data对象" aria-hidden="true">#</a> <code>data</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>has_more</td>
                    <td>bool</td>
                    <td>是否有更多数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>数据数组</td>
                    <td></td>
                </tr>
                <tr>
                    <td>offset</td>
                    <td>str</td>
                    <td>偏移量</td>
                    <td>等于<code>items</code>中最后一条记录的id<br>获取下一页时使用</td>
                </tr>
                <tr>
                    <td>update_baseline</td>
                    <td>str</td>
                    <td>更新基线</td>
                    <td>等于<code>items</code>中第一条记录的id</td>
                </tr>
                <tr>
                    <td>update_num</td>
                    <td>num</td>
                    <td>本次获取获取到了多少条新动态</td>
                    <td>在更新基线以上的动态条数</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象" tabindex="-1"><a class="header-anchor" href="#data对象-items数组中的对象"
                                                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>basic</td>
                    <td>obj</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>动态id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>modules</td>
                    <td>obj</td>
                    <td>动态信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>动态类型</td>
                    <td><a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%8A%A8%E6%80%81%E7%B1%BB%E5%9E%8B"
                           class="">动态类型</a></td>
                </tr>
                <tr>
                    <td>visible</td>
                    <td>bool</td>
                    <td>是否显示</td>
                    <td><code>true</code>：正常显示<br><code>false</code>：折叠动态</td>
                </tr>
                <tr>
                    <td>orig</td>
                    <td>obj</td>
                    <td>原动态信息</td>
                    <td>仅动态类型为<code>DYNAMIC_TYPE_FORWARD</code>的情况下存在</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-basic对象" tabindex="-1"><a class="header-anchor"
                                                                           href="#data对象-items数组中的对象-basic对象"
                                                                           aria-hidden="true">#</a> <code>data</code>对象 -&gt;
                <code>items</code>数组中的对象 -&gt; <code>basic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>comment_id_str</td>
                    <td>str</td>
                    <td></td>
                    <td><code>DYNAMIC_TYPE_AV</code>：视频AV号<br><code>DYNAMIC_TYPE_UGC_SEASON</code>：视频AV号<br><code>DYNAMIC_TYPE_PGC</code>：剧集分集AV号<br><code>DYNAMIC_TYPE_LIVE_RCMD</code>：动态本身id<br><code>DYNAMIC_TYPE_DRAW</code>：相簿id<br><code>DYNAMIC_TYPE_ARTICLE</code>：专栏cv号<br><code>DYNAMIC_TYPE_FORWARD</code>：动态本身id<br><code>DYNAMIC_TYPE_WORD</code>：动态本身id<br><code>DYNAMIC_TYPE_LIVE</code>:动态本身id<br><code>DYNAMIC_TYPE_MEDIALIST</code>:收藏夹ml号
                    </td>
                </tr>
                <tr>
                    <td>comment_type</td>
                    <td>num</td>
                    <td></td>
                    <td>1：<code>DYNAMIC_TYPE_AV</code> <code>DYNAMIC_TYPE_PGC</code> <code>DYNAMIC_TYPE_UGC_SEASON</code><br>11：<code>DYNAMIC_TYPE_DRAW</code><br>12：<code>DYNAMIC_TYPE_ARTICLE</code><br>17：<code>DYNAMIC_TYPE_LIVE_RCMD</code>
                        <code>DYNAMIC_TYPE_FORWARD</code> <code>DYNAMIC_TYPE_WORD</code> <code>DYNAMIC_TYPE_COMMON_SQUARE</code><br>19：<code>DYNAMIC_TYPE_MEDIALIST</code>
                    </td>
                </tr>
                <tr>
                    <td>like_icon</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>空串</code></td>
                </tr>
                <tr>
                    <td>rid_str</td>
                    <td>str</td>
                    <td></td>
                    <td><code>DYNAMIC_TYPE_AV</code>：视频AV号<br><code>DYNAMIC_TYPE_UGC_SEASON</code>：视频AV号 <code>DYNAMIC_TYPE_PGC</code>：剧集分集EP号<br><code>DYNAMIC_TYPE_DRAW</code>：相簿id<br><code>DYNAMIC_TYPE_ARTICLE</code>：专栏cv号<br><code>DYNAMIC_TYPE_LIVE_RCMD</code>：live_id<br><code>DYNAMIC_TYPE_FORWARD</code>：未知<br><code>DYNAMIC_TYPE_WORD</code>：未知<br><code>DYNAMIC_TYPE_COMMON_SQUARE</code>：未知<br><code>DYNAMIC_TYPE_LIVE</code>：直播间id<br><code>DYNAMIC_TYPE_MEDIALIST</code>：收藏夹ml号
                    </td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-basic对象-like-icon对象" tabindex="-1"><a class="header-anchor"
                                                                                         href="#data对象-items数组中的对象-basic对象-like-icon对象"
                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>basic</code>对象 -&gt;
                <code>like_icon</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>action_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>end_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>start_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象" tabindex="-1"><a class="header-anchor"
                                                                             href="#data对象-items数组中的对象-modules对象"
                                                                             aria-hidden="true">#</a> <code>data</code>对象 -&gt;
                <code>items</code>数组中的对象 -&gt; <code>modules</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>module_author</td>
                    <td>obj</td>
                    <td>UP主信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_dynamic</td>
                    <td>obj</td>
                    <td>动态内容信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_more</td>
                    <td>obj</td>
                    <td>动态右上角三点菜单</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_stat</td>
                    <td>obj</td>
                    <td>动态统计数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_interaction</td>
                    <td>obj</td>
                    <td>热度评论</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_fold</td>
                    <td>obj</td>
                    <td>动态折叠信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_dispute</td>
                    <td>obj</td>
                    <td>争议小黄条</td>
                    <td></td>
                </tr>
                <tr>
                    <td>module_tag</td>
                    <td>obj</td>
                    <td>置顶信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象" tabindex="-1"><a class="header-anchor"
                                                                                               href="#data对象-items数组中的对象-modules对象-module-author对象"
                                                                                               aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>face</td>
                    <td>str</td>
                    <td>头像</td>
                    <td></td>
                </tr>
                <tr>
                    <td>face_nft</td>
                    <td>bool</td>
                    <td>是否为NFT头像</td>
                    <td></td>
                </tr>
                <tr>
                    <td>following</td>
                    <td>bool</td>
                    <td>是否关注此UP主</td>
                    <td>自己的动态为<code>null</code></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转链接</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>名称前标签</td>
                    <td><code>合集</code><br><code>电视剧</code><br><code>番剧</code></td>
                </tr>
                <tr>
                    <td>mid</td>
                    <td>num</td>
                    <td>UP主UID<br>剧集SeasonId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>UP主名称<br>剧集名称<br>合集名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>official_verify</td>
                    <td>obj</td>
                    <td>UP主认证信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pendant</td>
                    <td>obj</td>
                    <td>UP主头像框</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pub_action</td>
                    <td>str</td>
                    <td>更新动作描述</td>
                    <td><code>投稿了视频</code><br><code>直播了</code><br><code>投稿了文章</code><br><code>更新了合集</code><br><code>与他人联合创作</code><br><code>发布了动态视频</code><br><code>投稿了直播回放</code>
                    </td>
                </tr>
                <tr>
                    <td>pub_location_text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>pub_time</td>
                    <td>str</td>
                    <td>更新时间</td>
                    <td><code>x分钟前</code><br><code>x小时前</code><br><code>昨天</code></td>
                </tr>
                <tr>
                    <td>pub_ts</td>
                    <td>num</td>
                    <td>更新时间戳</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>作者类型</td>
                    <td><a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E4%BD%9C%E8%80%85%E7%B1%BB%E5%9E%8B"
                           class="">作者类型</a></td>
                </tr>
                <tr>
                    <td>vip</td>
                    <td>obj</td>
                    <td>UP主大会员信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>decorate</td>
                    <td>obj</td>
                    <td>装扮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>nft_info</td>
                    <td>obj</td>
                    <td>NFT头像信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-official-verify对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-official-verify对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>official_verify</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>认证说明</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>认证类型</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-pendant对象" tabindex="-1"><a class="header-anchor"
                                                                                                           href="#data对象-items数组中的对象-modules对象-module-author对象-pendant对象"
                                                                                                           aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象
                -&gt; <code>pendant</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>expire</td>
                    <td>num</td>
                    <td>过期时间</td>
                    <td>此接口返回恒为<code>0</code></td>
                </tr>
                <tr>
                    <td>image</td>
                    <td>str</td>
                    <td>头像框图片url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>image_enhance</td>
                    <td>str</td>
                    <td>头像框图片url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>image_enhance_frame</td>
                    <td>str</td>
                    <td>头像框图片逐帧序列url</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>头像框名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pid</td>
                    <td>num</td>
                    <td>头像框id</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-vip对象" tabindex="-1"><a class="header-anchor"
                                                                                                       href="#data对象-items数组中的对象-modules对象-module-author对象-vip对象"
                                                                                                       aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_author</code>对象
                -&gt; <code>vip</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>avatar_subscript</td>
                    <td>num</td>
                    <td>是否显示角标</td>
                    <td>0：不显示<br>1：显示</td>
                </tr>
                <tr>
                    <td>avatar_subscript_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>due_date</td>
                    <td>num</td>
                    <td>大会员过期时间戳</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>obj</td>
                    <td>大会员标签</td>
                    <td></td>
                </tr>
                <tr>
                    <td>nickname_color</td>
                    <td>str</td>
                    <td>名字显示颜色</td>
                    <td>大会员：<code>#FB7299</code></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td>大会员状态</td>
                    <td>0：无<br>1：有<br>2：？</td>
                </tr>
                <tr>
                    <td>theme_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>大会员类型</td>
                    <td>0：无<br>1：月大会员<br>2：年度及以上大会员</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-vip对象-label对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-vip对象-label对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>vip</code>对象 -&gt;
                <code>label</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>会员标签背景颜色</td>
                    <td><code>#FB7299</code></td>
                </tr>
                <tr>
                    <td>bg_style</td>
                    <td>num</td>
                    <td><code>0</code> <code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>border_color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>img_label_uri_hans</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>动态版 简体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hans_static</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>静态版 简体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hant</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>动态版 繁体版</td>
                </tr>
                <tr>
                    <td>img_label_uri_hant_static</td>
                    <td>str</td>
                    <td>大会员牌子图片</td>
                    <td>静态版 繁体版</td>
                </tr>
                <tr>
                    <td>label_theme</td>
                    <td>str</td>
                    <td>会员标签</td>
                    <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员<br>fools_day_hundred_annual_vip：最强绿鲤鱼
                    </td>
                </tr>
                <tr>
                    <td>path</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>会员类型文案</td>
                    <td><code>大会员</code> <code>年度大会员</code> <code>十年大会员</code> <code>百年大会员</code>
                        <code>最强绿鲤鱼</code></td>
                </tr>
                <tr>
                    <td>text_color</td>
                    <td>str</td>
                    <td>用户名文字颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>use_img_label</td>
                    <td>bool</td>
                    <td><code>true</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-decorate对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-decorate对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>decorate</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>card_url</td>
                    <td>str</td>
                    <td>动态卡片小图标图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>fan</td>
                    <td>obj</td>
                    <td>粉丝装扮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>装扮ID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>装扮名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-decorate对象-fan对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-decorate对象-fan对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>decorate</code>对象 -&gt;
                <code>fan</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>编号颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>is_fan</td>
                    <td>bool</td>
                    <td>是否是粉丝装扮</td>
                    <td></td>
                </tr>
                <tr>
                    <td>num_str</td>
                    <td>str</td>
                    <td>装扮编号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>number</td>
                    <td>num</td>
                    <td>装扮编号</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-author对象-nft-info对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-author对象-nft-info对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_author</code>对象 -&gt; <code>nft_info</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>region_icon</td>
                    <td>str</td>
                    <td>NFT头像角标URL</td>
                    <td>
                        类型1：https://i0.hdslb.com/bfs/activity-plat/static/20220506/334553dd7c506a92b88eaf4d59ac8b4d/j8AeXAkEul.gif
                        <br>类型2：https://i0.hdslb.com/bfs/activity-plat/static/20220506/334553dd7c506a92b88eaf4d59ac8b4d/IOHoVs1ebP.gif
                    </td>
                </tr>
                <tr>
                    <td>region_type</td>
                    <td>num</td>
                    <td>NFT头像角标类型</td>
                    <td>1,2</td>
                </tr>
                <tr>
                    <td>show_status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象" tabindex="-1"><a class="header-anchor"
                                                                                                href="#data对象-items数组中的对象-modules对象-module-dynamic对象"
                                                                                                aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>additional</td>
                    <td>obj</td>
                    <td>相关内容卡片信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>obj</td>
                    <td>动态文字内容</td>
                    <td>其他动态时为null</td>
                </tr>
                <tr>
                    <td>major</td>
                    <td>obj</td>
                    <td>动态主体对象</td>
                    <td>转发动态时为null</td>
                </tr>
                <tr>
                    <td>topic</td>
                    <td>obj</td>
                    <td>话题信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>common</td>
                    <td>obj</td>
                    <td>一般类型</td>
                    <td><code>ADDITIONAL_TYPE_COMMON</code>类型独有</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>卡片类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E7%9B%B8%E5%85%B3%E5%86%85%E5%AE%B9%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B"
                           class="">相关内容卡片类型</a></td>
                </tr>
                <tr>
                    <td>reserve</td>
                    <td>obj</td>
                    <td>预约信息</td>
                    <td><code>ADDITIONAL_TYPE_RESERVE</code>类型独有</td>
                </tr>
                <tr>
                    <td>goods</td>
                    <td>obj</td>
                    <td>商品内容</td>
                    <td><code>ADDITIONAL_TYPE_GOODS</code>类型独有</td>
                </tr>
                <tr>
                    <td>vote</td>
                    <td>obj</td>
                    <td>投票信息</td>
                    <td><code>ADDITIONAL_TYPE_VOTE</code>类型独有</td>
                </tr>
                <tr>
                    <td>ugc</td>
                    <td>obj</td>
                    <td>视频信息</td>
                    <td><code>ADDITIONAL_TYPE_UGC</code>类型独有</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>button</td>
                    <td>obj</td>
                    <td>按钮内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>左侧封面图</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc1</td>
                    <td>str</td>
                    <td>描述1</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc2</td>
                    <td>str</td>
                    <td>描述2</td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td>卡片头文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>相关id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_type</td>
                    <td>str</td>
                    <td>子类型</td>
                    <td><code>game</code><br><code>decoration</code><br><code>ogv</code></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>卡片标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_style</td>
                    <td>obj</td>
                    <td>跳转类型</td>
                    <td><code>game</code>和<code>decoration</code>类型特有</td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td></td>
                    <td>1：<code>game</code>和<code>decoration</code>类型<br>2：<code>ogv</code>类型</td>
                </tr>
                <tr>
                    <td>check</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>ogv</code>类型特有</td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>uncheck</td>
                    <td>obj</td>
                    <td></td>
                    <td><code>ogv</code>类型特有</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-jump-style对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-jump-style对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>jump_style</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td>game：<code>进入</code><br>decoration：<code>去看看</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-check对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-check对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>check</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>按钮图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>ogv</code>：已追剧</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-uncheck对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-common对象-button对象-uncheck对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>common</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>uncheck</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>按钮图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>ogv</code>：追剧</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>button</td>
                    <td>obj</td>
                    <td>按钮信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc1</td>
                    <td>obj</td>
                    <td>预约时间</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc2</td>
                    <td>obj</td>
                    <td>预约观看量</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>reserve_total</td>
                    <td>num</td>
                    <td>预约人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>num</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>state</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>stype</td>
                    <td>num</td>
                    <td><code>1</code> <code>2</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>预约标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>up_mid</td>
                    <td>num</td>
                    <td>预约发起人UID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc3</td>
                    <td>obj</td>
                    <td>预约有奖信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>check</td>
                    <td>obj</td>
                    <td>已预约状态显示内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td>预约状态</td>
                    <td>1：未预约，使用<code>uncheck</code><br>2：已预约，使用<code>check</code></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>1：视频预约，使用<code>jump_style</code><br>2：直播预约，使用<code>check</code>和<code>uncheck</code></td>
                </tr>
                <tr>
                    <td>uncheck</td>
                    <td>obj</td>
                    <td>未预约状态显示内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_style</td>
                    <td>obj</td>
                    <td>跳转按钮</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-check对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-check对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>check</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>已预约</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-uncheck对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-uncheck对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>uncheck</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>显示图标URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>toast</td>
                    <td>str</td>
                    <td>预约成功显示提示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable</td>
                    <td>num</td>
                    <td>是否不可预约</td>
                    <td>1：是</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-jump-style对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-button对象-jump-style对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>button</code>对象 -&gt; <code>jump_style</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>按钮显示文案</td>
                    <td><code>去观看</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc1对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc1对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc1</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>0：<code>视频预约</code> <code>11-05 20:00 直播</code> <code>预计今天
                        17:05发布</code><br>1：<code>直播中</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc2对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc2对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc2</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td><code>2人预约</code><br><code>743观看</code><br><code>1.0万人看过</code><br><code>2151人气</code></td>
                </tr>
                <tr>
                    <td>visible</td>
                    <td>bool</td>
                    <td>是否显示</td>
                    <td>true：显示文案<br>false：显示已结束</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc3对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-reserve对象-desc3对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>reserve</code>对象
                -&gt; <code>desc3</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>开奖信息跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>奖品信息显示文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>goods</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>head_icon</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td>卡片头显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>商品信息列表</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象-items数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-goods对象-items数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>goods</code>对象
                -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>brief</td>
                    <td>str</td>
                    <td>商品副标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>商品封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>str</td>
                    <td>商品ID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_desc</td>
                    <td>str</td>
                    <td>跳转按钮显示文案</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>商品名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>price</td>
                    <td>str</td>
                    <td>商品价格</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-vote对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-vote对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>additional</code>对象 -&gt; <code>vote</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>choice_cnt</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>default_share</td>
                    <td>num</td>
                    <td>是否默认勾选<code>同时分享至动态</code></td>
                    <td>1：勾选</td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>投票标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>end_time</td>
                    <td>num</td>
                    <td>剩余时间</td>
                    <td>单位：秒</td>
                </tr>
                <tr>
                    <td>join_num</td>
                    <td>num</td>
                    <td>已参与人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>null</td>
                    <td><code>null</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>uid</td>
                    <td>num</td>
                    <td>发起人UID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>vote_id</td>
                    <td>num</td>
                    <td>投票ID</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-ugc对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-additional对象-ugc对象" aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>additional</code>对象 -&gt; <code>ugc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_second</td>
                    <td>str</td>
                    <td>播放量与弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration</td>
                    <td>str</td>
                    <td>视频长度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>head_text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>id_str</td>
                    <td>str</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>视频跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>multi_line</td>
                    <td>bool</td>
                    <td><code>true</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>desc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>动态的文字内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>orig_text</td>
                    <td>str</td>
                    <td>原始文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>替换后的文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>节点类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>emoji</td>
                    <td>obj</td>
                    <td>表情信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>str</td>
                    <td>关联id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>goods</td>
                    <td>obj</td>
                    <td>商品信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>icon_name</td>
                    <td>str</td>
                    <td>图标名称</td>
                    <td><code>taobao</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
                -&gt; <code>emoji</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>表情图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>表情尺寸</td>
                    <td><code>1</code> <code>2</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>表情的文字代码</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>表情类型</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-goods对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-desc对象-rich-text-nodes数组中的对象-goods对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象
                -&gt; <code>goods</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象" tabindex="-1"><a class="header-anchor"
                                                                                                          href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象"
                                                                                                          aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>major</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>动态主体类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%8A%A8%E6%80%81%E4%B8%BB%E4%BD%93%E7%B1%BB%E5%9E%8B"
                           class="">动态主体类型</a></td>
                </tr>
                <tr>
                    <td>ugc_season</td>
                    <td>obj</td>
                    <td>合集信息</td>
                    <td><code>MAJOR_TYPE_UGC_SEASON</code></td>
                </tr>
                <tr>
                    <td>article</td>
                    <td>obj</td>
                    <td>专栏类型</td>
                    <td><code>MAJOR_TYPE_ARTICLE</code></td>
                </tr>
                <tr>
                    <td>draw</td>
                    <td>obj</td>
                    <td>带图动态</td>
                    <td><code>MAJOR_TYPE_DRAW</code></td>
                </tr>
                <tr>
                    <td>archive</td>
                    <td>obj</td>
                    <td>视频信息</td>
                    <td><code>MAJOR_TYPE_ARCHIVE</code></td>
                </tr>
                <tr>
                    <td>live_rcmd</td>
                    <td>obj</td>
                    <td>直播状态</td>
                    <td><code>MAJOR_TYPE_LIVE_RCMD</code></td>
                </tr>
                <tr>
                    <td>common</td>
                    <td>obj</td>
                    <td>一般类型</td>
                    <td><code>MAJOR_TYPE_COMMON</code></td>
                </tr>
                <tr>
                    <td>pgc</td>
                    <td>obj</td>
                    <td>剧集信息</td>
                    <td><code>MAJOR_TYPE_PGC</code></td>
                </tr>
                <tr>
                    <td>courses</td>
                    <td>obj</td>
                    <td>课程信息</td>
                    <td><code>MAJOR_TYPE_COURSES</code></td>
                </tr>
                <tr>
                    <td>music</td>
                    <td>obj</td>
                    <td>音频信息</td>
                    <td><code>MAJOR_TYPE_MUSIC</code></td>
                </tr>
                <tr>
                    <td>opus</td>
                    <td>obj</td>
                    <td>图文动态</td>
                    <td><code>MAJOR_TYPE_OPUS</code></td>
                </tr>
                <tr>
                    <td>live</td>
                    <td>obj</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>none</td>
                    <td>obj</td>
                    <td>动态失效</td>
                    <td><code>MAJOR_TYPE_NONE</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>aid</td>
                    <td>num</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>视频简介</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable_preview</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration_text</td>
                    <td>str</td>
                    <td>时长</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-badge对象" tabindex="-1">
                <a class="header-anchor"
                   href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-badge对象"
                   aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
                -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-stat对象" tabindex="-1">
                <a class="header-anchor"
                   href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-ugc-season对象-stat对象"
                   aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>ugc_season</code>对象
                -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-article对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-article对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>article</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>covers</td>
                    <td>array</td>
                    <td>封面图数组</td>
                    <td>最多三张</td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>文章摘要</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>文章CV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>文章跳转地址</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>文章阅读量</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>文章标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>draw</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>对应相簿id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>图片信息列表</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象-items数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-draw对象-items数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>draw</code>对象 -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>height</td>
                    <td>num</td>
                    <td>图片高度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>图片大小</td>
                    <td>单位KB</td>
                </tr>
                <tr>
                    <td>src</td>
                    <td>str</td>
                    <td>图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>tags</td>
                    <td>array</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>width</td>
                    <td>num</td>
                    <td>图片宽度</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>aid</td>
                    <td>str</td>
                    <td>视频AV号</td>
                    <td></td>
                </tr>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>bvid</td>
                    <td>str</td>
                    <td>视频BVID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>视频简介</td>
                    <td></td>
                </tr>
                <tr>
                    <td>disable_preview</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>duration_text</td>
                    <td>str</td>
                    <td>视频长度</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-stat对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-archive对象-stat对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>archive</code>对象 -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live-rcmd对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live-rcmd对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt; <code>live_rcmd</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>content</td>
                    <td>str</td>
                    <td>直播间内容JSON</td>
                    <td></td>
                </tr>
                <tr>
                    <td>reserve_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>common</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>biz_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>左侧图片封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>右侧描述信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转地址</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>sketch_id</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>style</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>右侧标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-common对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>common</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td><code>空串</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>视频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>epid</td>
                    <td>num</td>
                    <td>分集EpId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>season_id</td>
                    <td>num</td>
                    <td>剧集SeasonId</td>
                    <td></td>
                </tr>
                <tr>
                    <td>stat</td>
                    <td>obj</td>
                    <td>统计信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_type</td>
                    <td>num</td>
                    <td>剧集类型</td>
                    <td>1：番剧<br>2：电影<br>3：纪录片<br>4：国创<br>5：电视剧<br>6：漫画<br>7：综艺</td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>视频标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>2</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-stat对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-pgc对象-stat对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>pgc</code>对象 -&gt; <code>stat</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>danmaku</td>
                    <td>str</td>
                    <td>弹幕数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>play</td>
                    <td>str</td>
                    <td>播放数</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>courses</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>封面图URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td>更新状态描述</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>课程id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>sub_title</td>
                    <td>str</td>
                    <td>课程副标题</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>课程标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-courses对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>courses</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-music对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-music对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>music</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>音频封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>音频AUID</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>音频分类</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>音频标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>opus</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>fold_action</td>
                    <td>array</td>
                    <td>展开收起</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>pics</td>
                    <td>array</td>
                    <td>图片信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>summary</td>
                    <td>obj</td>
                    <td>动态内容</td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>动态标题</td>
                    <td>没有标题时为null</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象-summary对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-opus对象-summary对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>opus</code>对象 -&gt; <code>summary</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>和<code>desc</code>对象中的<code>rich_text_nodes</code>数组结构一样</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>评论内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>live</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>badge</td>
                    <td>obj</td>
                    <td>角标信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>cover</td>
                    <td>str</td>
                    <td>直播封面</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_first</td>
                    <td>str</td>
                    <td>直播主分区名称</td>
                    <td></td>
                </tr>
                <tr>
                    <td>desc_second</td>
                    <td>str</td>
                    <td>观看人数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>直播间id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>直播间跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>live_state</td>
                    <td>num</td>
                    <td>直播状态</td>
                    <td>0：直播结束<br>1：正在直播</td>
                </tr>
                <tr>
                    <td>reserve_type</td>
                    <td>num</td>
                    <td><code>0</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>直播间标题</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象-badge对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-live对象-badge对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>live</code>对象 -&gt; <code>badge</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>bg_color</td>
                    <td>str</td>
                    <td>背景颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>color</td>
                    <td>str</td>
                    <td>字体颜色</td>
                    <td></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>角标文案</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-none对象" tabindex="-1"><a
                    class="header-anchor" href="#data对象-items数组中的对象-modules对象-module-dynamic对象-major对象-none对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象 -&gt; <code>major</code>对象 -&gt;
                <code>none</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>tips</td>
                    <td>str</td>
                    <td>动态失效显示文案</td>
                    <td>deprecated?</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dynamic对象-topic对象" tabindex="-1"><a class="header-anchor"
                                                                                                          href="#data对象-items数组中的对象-modules对象-module-dynamic对象-topic对象"
                                                                                                          aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dynamic</code>对象
                -&gt; <code>topic</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>id</td>
                    <td>num</td>
                    <td>话题id</td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td>跳转URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>str</td>
                    <td>话题名称</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-more对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_more</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>three_point_items</td>
                    <td>array</td>
                    <td>右上角三点菜单</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>label</td>
                    <td>str</td>
                    <td>显示文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>类型</td>
                    <td></td>
                </tr>
                <tr>
                    <td>modal</td>
                    <td>obj</td>
                    <td>弹出框信息</td>
                    <td>删除动态时弹出</td>
                </tr>
                <tr>
                    <td>params</td>
                    <td>obj</td>
                    <td>参数</td>
                    <td>置顶/取消置顶时使用</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-modal对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-modal对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象 -&gt;
                <code>modal</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>cancel</td>
                    <td>str</td>
                    <td>取消按钮</td>
                    <td><code>我点错了</code></td>
                </tr>
                <tr>
                    <td>confirm</td>
                    <td>str</td>
                    <td>确认按钮</td>
                    <td><code>删除</code></td>
                </tr>
                <tr>
                    <td>content</td>
                    <td>str</td>
                    <td>提示内容</td>
                    <td><code>确定要删除此条动态吗？</code></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>标题</td>
                    <td><code>删除动态</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-params对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-more对象-three-point-items数组中的对象-params对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_more</code>对象 -&gt; <code>three_point_items</code>数组中的对象 -&gt;
                <code>params</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>dynamic_id</td>
                    <td>str</td>
                    <td>当前动态ID</td>
                    <td>deprecated?</td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>bool</td>
                    <td>当前动态是否处于置顶状态</td>
                    <td>deprecated?</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-stat对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>comment</td>
                    <td>obj</td>
                    <td>评论数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forward</td>
                    <td>obj</td>
                    <td>转发数据</td>
                    <td></td>
                </tr>
                <tr>
                    <td>like</td>
                    <td>obj</td>
                    <td>点赞数据</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-comment对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-stat对象-comment对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>comment</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>评论数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>hidden</td>
                    <td>bool</td>
                    <td>是否隐藏</td>
                    <td>直播类型动态会隐藏回复功能</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-forward对象" tabindex="-1"><a class="header-anchor"
                                                                                                         href="#data对象-items数组中的对象-modules对象-module-stat对象-forward对象"
                                                                                                         aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>forward</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>转发数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-stat对象-like对象" tabindex="-1"><a class="header-anchor"
                                                                                                      href="#data对象-items数组中的对象-modules对象-module-stat对象-like对象"
                                                                                                      aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_stat</code>对象
                -&gt; <code>like</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>count</td>
                    <td>num</td>
                    <td>点赞数</td>
                    <td></td>
                </tr>
                <tr>
                    <td>forbidden</td>
                    <td>bool</td>
                    <td><code>false</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>status</td>
                    <td>bool</td>
                    <td>当前用户是否点赞</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象" tabindex="-1"><a class="header-anchor"
                                                                                                    href="#data对象-items数组中的对象-modules对象-module-interaction对象"
                                                                                                    aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_interaction</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>items</td>
                    <td>array</td>
                    <td>信息列表</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>obj</td>
                    <td>点赞/评论信息</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>类型</td>
                    <td>0：点赞信息<br>1：评论信息</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象" tabindex="-1"><a
                    class="header-anchor"
                    href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象"
                    aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>rich_text_nodes</td>
                    <td>array</td>
                    <td>富文本节点列表</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>评论内容</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>orig_text</td>
                    <td>str</td>
                    <td>原始文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>rid</td>
                    <td>str</td>
                    <td>关联ID</td>
                    <td>用户UID</td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>替换后文本</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>str</td>
                    <td>富文本节点类型</td>
                    <td>
                        <a href="/bilibili-API-collect/docs/dynamic/dynamic_enum.html#%E5%AF%8C%E6%96%87%E6%9C%AC%E8%8A%82%E7%82%B9%E7%B1%BB%E5%9E%8B"
                           class="">富文本节点类型</a></td>
                </tr>
                <tr>
                    <td>emoji</td>
                    <td>obj</td>
                    <td>表情信息</td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                tabindex="-1"><a class="header-anchor"
                                 href="#data对象-items数组中的对象-modules对象-module-interaction对象-items数组中的对象-desc对象-rich-text-nodes数组中的对象-emoji对象"
                                 aria-hidden="true">#</a> <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>modules</code>对象 -&gt; <code>module_interaction</code>对象 -&gt; <code>items</code>数组中的对象 -&gt;
                <code>desc</code>对象 -&gt; <code>rich_text_nodes</code>数组中的对象 -&gt; <code>emoji</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>icon_url</td>
                    <td>str</td>
                    <td>表情图片URL</td>
                    <td></td>
                </tr>
                <tr>
                    <td>size</td>
                    <td>num</td>
                    <td>表情尺寸</td>
                    <td><code>1</code> <code>2</code></td>
                </tr>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>表情的文字代码</td>
                    <td></td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td>表情类型</td>
                    <td><code>1</code> <code>2</code> <code>3</code></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-fold对象" tabindex="-1"><a class="header-anchor"
                                                                                             href="#data对象-items数组中的对象-modules对象-module-fold对象"
                                                                                             aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_fold</code>对象
            </h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>ids</td>
                    <td>array</td>
                    <td>被折叠的动态id列表</td>
                    <td></td>
                </tr>
                <tr>
                    <td>statement</td>
                    <td>str</td>
                    <td>显示文案</td>
                    <td>例：展开x条相关动态</td>
                </tr>
                <tr>
                    <td>type</td>
                    <td>num</td>
                    <td><code>1</code></td>
                    <td></td>
                </tr>
                <tr>
                    <td>users</td>
                    <td>array</td>
                    <td><code>空数组</code></td>
                    <td></td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-dispute对象" tabindex="-1"><a class="header-anchor"
                                                                                                href="#data对象-items数组中的对象-modules对象-module-dispute对象"
                                                                                                aria-hidden="true">#</a> <code>data</code>对象
                -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt; <code>module_dispute</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>desc</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>jump_url</td>
                    <td>str</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>title</td>
                    <td>str</td>
                    <td>提醒文案</td>
                    <td>例：视频内含有危险行为，请勿模仿</td>
                </tr>
                </tbody>
            </table>
            <h3 id="data对象-items数组中的对象-modules对象-module-tag对象" tabindex="-1"><a class="header-anchor"
                                                                                            href="#data对象-items数组中的对象-modules对象-module-tag对象"
                                                                                            aria-hidden="true">#</a>
                <code>data</code>对象 -&gt; <code>items</code>数组中的对象 -&gt; <code>modules</code>对象 -&gt;
                <code>module_tag</code>对象</h3>
            <table>
                <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>内容</th>
                    <th>备注</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>text</td>
                    <td>str</td>
                    <td>'置顶'</td>
                    <td>置顶动态出现这个对象，否则没有</td>
                </tr>
                </tbody>
            </table>
        </div>

        """
        api = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
        headers = self.headers
        data = {
            "offset": "",
            "host_mid": host_mid
        }
        dynamic = requests.get(api, headers=headers, params=data).json()
        if not all:
            dynamics = dynamic["data"]["items"]
        else:
            dynamics = dynamic["data"]["items"]
            while dynamic["data"]["has_more"]:
                data["offset"] = dynamic["data"]["offset"]
                dynamic = requests.get(api, headers=headers, params=data).json()
                for i in dynamic["data"]["items"]:
                    if i not in dynamics:
                        dynamics.append(i)
        dynamic = dynamics
        return dynamic

    def interface_nav(self):
        """
        获取登录后导航栏用户信息
        @return:
        <p><code>data</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>isLogin</td>
                <td>bool</td>
                <td>是否已登录</td>
                <td>false：未登录<br>true：已登录</td>
            </tr>
            <tr>
                <td>email_verified</td>
                <td>num</td>
                <td>是否验证邮箱地址</td>
                <td>0：未验证<br>1：已验证</td>
            </tr>
            <tr>
                <td>face</td>
                <td>str</td>
                <td>用户头像 url</td>
                <td></td>
            </tr>
            <tr>
                <td>level_info</td>
                <td>obj</td>
                <td>等级信息</td>
                <td></td>
            </tr>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>用户 mid</td>
                <td></td>
            </tr>
            <tr>
                <td>mobile_verified</td>
                <td>num</td>
                <td>是否验证手机号</td>
                <td>0：未验证<br>1：已验证</td>
            </tr>
            <tr>
                <td>money</td>
                <td>num</td>
                <td>拥有硬币数</td>
                <td></td>
            </tr>
            <tr>
                <td>moral</td>
                <td>num</td>
                <td>当前节操值</td>
                <td>上限为70</td>
            </tr>
            <tr>
                <td>official</td>
                <td>obj</td>
                <td>认证信息</td>
                <td></td>
            </tr>
            <tr>
                <td>officialVerify</td>
                <td>obj</td>
                <td>认证信息 2</td>
                <td></td>
            </tr>
            <tr>
                <td>pendant</td>
                <td>obj</td>
                <td>头像框信息</td>
                <td></td>
            </tr>
            <tr>
                <td>scores</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>uname</td>
                <td>str</td>
                <td>用户昵称</td>
                <td></td>
            </tr>
            <tr>
                <td>vipDueDate</td>
                <td>num</td>
                <td>会员到期时间</td>
                <td>毫秒 时间戳</td>
            </tr>
            <tr>
                <td>vipStatus</td>
                <td>num</td>
                <td>会员开通状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>vipType</td>
                <td>num</td>
                <td>会员类型</td>
                <td>0：无<br>1：月度大会员<br>2：年度及以上大会员</td>
            </tr>
            <tr>
                <td>vip_pay_type</td>
                <td>num</td>
                <td>会员开通状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>vip_theme_type</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>vip_label</td>
                <td>obj</td>
                <td>会员标签</td>
                <td></td>
            </tr>
            <tr>
                <td>vip_avatar_subscript</td>
                <td>num</td>
                <td>是否显示会员图标</td>
                <td>0：不显示<br>1：显示</td>
            </tr>
            <tr>
                <td>vip_nickname_color</td>
                <td>str</td>
                <td>会员昵称颜色</td>
                <td>颜色码</td>
            </tr>
            <tr>
                <td>wallet</td>
                <td>obj</td>
                <td>B币钱包信息</td>
                <td></td>
            </tr>
            <tr>
                <td>has_shop</td>
                <td>bool</td>
                <td>是否拥有推广商品</td>
                <td>false：无<br>true：有</td>
            </tr>
            <tr>
                <td>shop_url</td>
                <td>str</td>
                <td>商品推广页面 url</td>
                <td></td>
            </tr>
            <tr>
                <td>allowance_count</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>answer_status</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>is_senior_member</td>
                <td>num</td>
                <td>是否硬核会员</td>
                <td>0：非硬核会员<br>1：硬核会员</td>
            </tr>
            <tr>
                <td>wbi_img</td>
                <td>obj</td>
                <td>Wbi 签名实时口令</td>
                <td>该字段即使用户未登录也存在</td>
            </tr>
            <tr>
                <td>is_jury</td>
                <td>bool</td>
                <td>是否风纪委员</td>
                <td>true：风纪委员<br>false：非风纪委员</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>level_info</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>current_level</td>
                <td>num</td>
                <td>当前等级</td>
                <td></td>
            </tr>
            <tr>
                <td>current_min</td>
                <td>num</td>
                <td>当前等级经验最低值</td>
                <td></td>
            </tr>
            <tr>
                <td>current_exp</td>
                <td>num</td>
                <td>当前经验</td>
                <td></td>
            </tr>
            <tr>
                <td>next_exp</td>
                <td>小于6级时：num<br>6级时：str</td>
                <td>升级下一等级需达到的经验</td>
                <td>当用户等级为Lv6时，值为<code>--</code>，代表无穷大</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>role</td>
                <td>num</td>
                <td>认证类型</td>
                <td>见<a href="/bilibili-API-collect/docs/user/official_role.html" class="">用户认证类型一览</a></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证备注</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：认证</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official_verify</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：认证</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>pendant</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>pid</td>
                <td>num</td>
                <td>挂件id</td>
                <td></td>
            </tr>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>挂件名称</td>
                <td></td>
            </tr>
            <tr>
                <td>image</td>
                <td>str</td>
                <td>挂件图片url</td>
                <td></td>
            </tr>
            <tr>
                <td>expire</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>vip_label</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>path</td>
                <td>str</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>text</td>
                <td>str</td>
                <td>会员名称</td>
                <td></td>
            </tr>
            <tr>
                <td>label_theme</td>
                <td>str</td>
                <td>会员标签</td>
                <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>wallet</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>登录用户mid</td>
                <td></td>
            </tr>
            <tr>
                <td>bcoin_balance</td>
                <td>num</td>
                <td>拥有B币数</td>
                <td></td>
            </tr>
            <tr>
                <td>coupon_balance</td>
                <td>num</td>
                <td>每月奖励B币数</td>
                <td></td>
            </tr>
            <tr>
                <td>coupon_due_time</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>wbi_img</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>img_url</td>
                <td>str</td>
                <td>Wbi 签名参数 <code>imgKey</code>的伪装 url</td>
                <td>详见文档 <a href="/bilibili-API-collect/docs/misc/sign/wbi.html" class="">Wbi 签名</a></td>
            </tr>
            <tr>
                <td>sub_url</td>
                <td>str</td>
                <td>Wbi 签名参数 <code>subKey</code>的伪装 url</td>
                <td>详见文档 <a href="/bilibili-API-collect/docs/misc/sign/wbi.html" class="">Wbi 签名</a></td>
            </tr>
            </tbody>
        </table>

        """
        api = "https://api.bilibili.com/x/web-interface/nav"
        headers = self.headers
        nav = requests.get(api, headers=headers).json()
        return nav["data"]


class CsrfAuthenticationL:
    def __init__(self, cookie: str, cookies: dict,
                 UA: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"):
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
        }
        self.csrf = cookies["bili_jct"]

    def AnchorChangeRoomArea(self, area_id):
        api = "https://api.live.bilibili.com/xlive/app-blink/v2/room/AnchorChangeRoomArea"
        data = {
            "platform": "pc",
            "room_id": 25322725,
            "area_id": area_id,
            "csrf_token": self.csrf,
            "csrf": self.csrf
        }


from tool import wbi


class WbiSigna:
    def __init__(self, cookie: str,
                 UA: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"):
        """
        完善 浏览器headers
        @param cookies: B站cookie 的 cookies
        @param UA: 浏览器User-Agent
        """
        self.headers = {
            "User-Agent": UA,
            "cookie": cookie,
        }

    def acc_info(self, mid: int):
        """
        用户空间详细信息
        @param mid:目标用户mid
        @return:
        <p><code>data</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>mid</td>
                <td></td>
            </tr>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>昵称</td>
                <td></td>
            </tr>
            <tr>
                <td>sex</td>
                <td>str</td>
                <td>性别</td>
                <td>男/女/保密</td>
            </tr>
            <tr>
                <td>face</td>
                <td>str</td>
                <td>头像链接</td>
                <td></td>
            </tr>
            <tr>
                <td>face_nft</td>
                <td>num</td>
                <td>是否为 NFT 头像</td>
                <td>0：不是 NFT 头像<br>1：是 NFT 头像</td>
            </tr>
            <tr>
                <td>face_nft_type</td>
                <td>num</td>
                <td>NFT 头像类型？</td>
                <td></td>
            </tr>
            <tr>
                <td>sign</td>
                <td>str</td>
                <td>签名</td>
                <td></td>
            </tr>
            <tr>
                <td>rank</td>
                <td>num</td>
                <td>用户权限等级</td>
                <td>目前应该无任何作用<br>5000：0级未答题<br>10000：普通会员<br>20000：字幕君<br>25000：VIP<br>30000：真·职人<br>32000：管理员
                </td>
            </tr>
            <tr>
                <td>level</td>
                <td>num</td>
                <td>当前等级</td>
                <td>0-6 级</td>
            </tr>
            <tr>
                <td>jointime</td>
                <td>num</td>
                <td>注册时间</td>
                <td>此接口返回恒为<code>0</code></td>
            </tr>
            <tr>
                <td>moral</td>
                <td>num</td>
                <td>节操值</td>
                <td>此接口返回恒为<code>0</code></td>
            </tr>
            <tr>
                <td>silence</td>
                <td>num</td>
                <td>封禁状态</td>
                <td>0：正常<br>1：被封</td>
            </tr>
            <tr>
                <td>coins</td>
                <td>num</td>
                <td>硬币数</td>
                <td>需要登录（Cookie） <br>只能查看自己的<br>默认为<code>0</code></td>
            </tr>
            <tr>
                <td>fans_badge</td>
                <td>bool</td>
                <td>是否具有粉丝勋章</td>
                <td>false：无<br>true：有</td>
            </tr>
            <tr>
                <td>fans_medal</td>
                <td>obj</td>
                <td>粉丝勋章信息</td>
                <td></td>
            </tr>
            <tr>
                <td>official</td>
                <td>obj</td>
                <td>认证信息</td>
                <td></td>
            </tr>
            <tr>
                <td>vip</td>
                <td>obj</td>
                <td>会员信息</td>
                <td></td>
            </tr>
            <tr>
                <td>pendant</td>
                <td>obj</td>
                <td>头像框信息</td>
                <td></td>
            </tr>
            <tr>
                <td>nameplate</td>
                <td>obj</td>
                <td>勋章信息</td>
                <td></td>
            </tr>
            <tr>
                <td>user_honour_info</td>
                <td>obj</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>is_followed</td>
                <td>bool</td>
                <td>是否关注此用户</td>
                <td>true：已关注<br>false：未关注<br>需要登录（Cookie） <br>未登录恒为<code>false</code></td>
            </tr>
            <tr>
                <td>top_photo</td>
                <td>str</td>
                <td>主页头图链接</td>
                <td></td>
            </tr>
            <tr>
                <td>theme</td>
                <td>obj</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>sys_notice</td>
                <td>obj</td>
                <td>系统通知</td>
                <td>无内容则为空对象<br>主要用于展示如用户争议、纪念账号等等的小黄条</td>
            </tr>
            <tr>
                <td>live_room</td>
                <td>obj</td>
                <td>直播间信息</td>
                <td></td>
            </tr>
            <tr>
                <td>birthday</td>
                <td>str</td>
                <td>生日</td>
                <td>MM-DD<br>如设置隐私为空</td>
            </tr>
            <tr>
                <td>school</td>
                <td>obj</td>
                <td>学校</td>
                <td></td>
            </tr>
            <tr>
                <td>profession</td>
                <td>obj</td>
                <td>专业资质信息</td>
                <td></td>
            </tr>
            <tr>
                <td>tags</td>
                <td>null</td>
                <td>个人标签</td>
                <td></td>
            </tr>
            <tr>
                <td>series</td>
                <td>obj</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>is_senior_member</td>
                <td>num</td>
                <td>是否为硬核会员</td>
                <td>0：否<br>1：是</td>
            </tr>
            <tr>
                <td>mcn_info</td>
                <td>null</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>gaia_res_type</td>
                <td>num</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>gaia_data</td>
                <td>null</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>is_risk</td>
                <td>bool</td>
                <td>（？）</td>
                <td></td>
            </tr>
            <tr>
                <td>elec</td>
                <td>obj</td>
                <td>充电信息</td>
                <td></td>
            </tr>
            <tr>
                <td>contract</td>
                <td>obj</td>
                <td>是否显示老粉计划</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>rank</code>示例</p>
        <table>
            <thead>
            <tr>
                <th>UID</th>
                <th>rank</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>2</td>
                <td>20000</td>
            </tr>
            <tr>
                <td>16765</td>
                <td>20000</td>
            </tr>
            <tr>
                <td>15773384</td>
                <td>20000</td>
            </tr>
            <tr>
                <td>124416</td>
                <td>20000</td>
            </tr>
            <tr>
                <td>429736362</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>424261768</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>41273726</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>15080107</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>9847497</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>4856007</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>928123</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>132704</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>70093</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>47291</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>27380</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>22445</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>3351</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>1101</td>
                <td>25000</td>
            </tr>
            <tr>
                <td>93066</td>
                <td>30000</td>
            </tr>
            <tr>
                <td>2443068</td>
                <td>30000</td>
            </tr>
            <tr>
                <td>46368</td>
                <td>30000</td>
            </tr>
            <tr>
                <td>11167</td>
                <td>30000</td>
            </tr>
            </tbody>
        </table>
        <p><code>profession</code>示例</p>
        <table>
            <thead>
            <tr>
                <th>UID</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>654391</td>
            </tr>
            <tr>
                <td>1440295</td>
            </tr>
            <tr>
                <td>1785155</td>
            </tr>
            <tr>
                <td>2990100</td>
            </tr>
            <tr>
                <td>3875803</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>official</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>role</td>
                <td>num</td>
                <td>认证类型</td>
                <td>见 <a href="/bilibili-API-collect/docs/user/official_role.html" class="">用户认证类型一览</a></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>认证信息</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>desc</td>
                <td>str</td>
                <td>认证备注</td>
                <td>无为空</td>
            </tr>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>是否认证</td>
                <td>-1：无<br>0：个人认证<br>1：机构认证</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>vip</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>type</td>
                <td>num</td>
                <td>会员类型</td>
                <td>0：无<br>1：月大会员<br>2：年度及以上大会员</td>
            </tr>
            <tr>
                <td>status</td>
                <td>num</td>
                <td>会员状态</td>
                <td>0：无<br>1：有</td>
            </tr>
            <tr>
                <td>due_date</td>
                <td>num</td>
                <td>会员过期时间</td>
                <td>毫秒时间戳</td>
            </tr>
            <tr>
                <td>vip_pay_type</td>
                <td>num</td>
                <td>支付类型</td>
                <td>0：未支付（常见于官方账号）<br>1：已支付（以正常渠道获取的大会员均为此值）</td>
            </tr>
            <tr>
                <td>theme_type</td>
                <td>num</td>
                <td>0</td>
                <td>作用尚不明确</td>
            </tr>
            <tr>
                <td>label</td>
                <td>obj</td>
                <td>会员标签</td>
                <td></td>
            </tr>
            <tr>
                <td>avatar_subscript</td>
                <td>num</td>
                <td>是否显示会员图标</td>
                <td>0：不显示<br>1：显示</td>
            </tr>
            <tr>
                <td>nickname_color</td>
                <td>str</td>
                <td>会员昵称颜色</td>
                <td>颜色码，一般为<code>#FB7299</code>，曾用于愚人节改变大会员配色</td>
            </tr>
            <tr>
                <td>role</td>
                <td>num</td>
                <td>大角色类型</td>
                <td>1：月度大会员<br>3：年度大会员<br>7：十年大会员<br>15：百年大会员</td>
            </tr>
            <tr>
                <td>avatar_subscript_url</td>
                <td>str</td>
                <td>大会员角标地址</td>
                <td></td>
            </tr>
            <tr>
                <td>tv_vip_status</td>
                <td>num</td>
                <td>电视大会员状态</td>
                <td>0：未开通</td>
            </tr>
            <tr>
                <td>tv_vip_pay_type</td>
                <td>num</td>
                <td>电视大会员支付类型</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>vip</code>中的<code>label</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>path</td>
                <td>str</td>
                <td>空</td>
                <td>作用尚不明确</td>
            </tr>
            <tr>
                <td>text</td>
                <td>str</td>
                <td>会员类型文案</td>
                <td><code>大会员</code> <code>年度大会员</code> <code>十年大会员</code> <code>百年大会员</code>
                    <code>最强绿鲤鱼</code></td>
            </tr>
            <tr>
                <td>label_theme</td>
                <td>str</td>
                <td>会员标签</td>
                <td>vip：大会员<br>annual_vip：年度大会员<br>ten_annual_vip：十年大会员<br>hundred_annual_vip：百年大会员<br>fools_day_hundred_annual_vip：最强绿鲤鱼
                </td>
            </tr>
            <tr>
                <td>text_color</td>
                <td>str</td>
                <td>会员标签</td>
                <td></td>
            </tr>
            <tr>
                <td>bg_style</td>
                <td>num</td>
                <td>1</td>
                <td></td>
            </tr>
            <tr>
                <td>bg_color</td>
                <td>str</td>
                <td>会员标签背景颜色</td>
                <td>颜色码，一般为<code>#FB7299</code>，曾用于愚人节改变大会员配色</td>
            </tr>
            <tr>
                <td>border_color</td>
                <td>str</td>
                <td>会员标签边框颜色</td>
                <td>未使用</td>
            </tr>
            <tr>
                <td>use_img_label</td>
                <td>bool</td>
                <td><code>true</code></td>
                <td></td>
            </tr>
            <tr>
                <td>img_label_uri_hans</td>
                <td>str</td>
                <td><code>空串</code></td>
                <td></td>
            </tr>
            <tr>
                <td>img_label_uri_hant</td>
                <td>str</td>
                <td><code>空串</code></td>
                <td></td>
            </tr>
            <tr>
                <td>img_label_uri_hans_static</td>
                <td>str</td>
                <td>大会员牌子图片</td>
                <td>简体版</td>
            </tr>
            <tr>
                <td>img_label_uri_hant_static</td>
                <td>str</td>
                <td>大会员牌子图片</td>
                <td>繁体版</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>pendant</code>对象：</p>
        <p><strong>普通头像框的<code>image</code>与<code>image_enhance</code>内容相同</strong></p>
        <p><strong>动态头像框的<code>image</code>为png静态图片，<code>image_enhance</code>为webp动态图片，<code>image_enhance_frame</code>为png逐帧序列</strong>
        </p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>pid</td>
                <td>num</td>
                <td>头像框id</td>
                <td></td>
            </tr>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>头像框名称</td>
                <td></td>
            </tr>
            <tr>
                <td>image</td>
                <td>str</td>
                <td>头像框图片url</td>
                <td></td>
            </tr>
            <tr>
                <td>expire</td>
                <td>num</td>
                <td>过期时间</td>
                <td>此接口返回恒为<code>0</code></td>
            </tr>
            <tr>
                <td>image_enhance</td>
                <td>str</td>
                <td>头像框图片url</td>
                <td></td>
            </tr>
            <tr>
                <td>image_enhance_frame</td>
                <td>str</td>
                <td>头像框图片逐帧序列url</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>nameplate</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>nid</td>
                <td>num</td>
                <td>勋章id</td>
                <td></td>
            </tr>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>勋章名称</td>
                <td></td>
            </tr>
            <tr>
                <td>image</td>
                <td>str</td>
                <td>勋章图标</td>
                <td></td>
            </tr>
            <tr>
                <td>image_small</td>
                <td>str</td>
                <td>勋章图标（小）</td>
                <td></td>
            </tr>
            <tr>
                <td>level</td>
                <td>str</td>
                <td>勋章等级</td>
                <td></td>
            </tr>
            <tr>
                <td>condition</td>
                <td>str</td>
                <td>获取条件</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>fans_medal</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>show</td>
                <td>bool</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>wear</td>
                <td>bool</td>
                <td>是否佩戴了粉丝勋章</td>
                <td></td>
            </tr>
            <tr>
                <td>medal</td>
                <td>obj</td>
                <td>粉丝勋章信息</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>fans_medal</code>中的<code>medal</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>uid</td>
                <td>num</td>
                <td>此用户mid</td>
                <td></td>
            </tr>
            <tr>
                <td>target_id</td>
                <td>num</td>
                <td>粉丝勋章所属UP的mid</td>
                <td></td>
            </tr>
            <tr>
                <td>medal_id</td>
                <td>num</td>
                <td>粉丝勋章id</td>
                <td></td>
            </tr>
            <tr>
                <td>level</td>
                <td>num</td>
                <td>粉丝勋章等级</td>
                <td></td>
            </tr>
            <tr>
                <td>medal_name</td>
                <td>str</td>
                <td>粉丝勋章名称</td>
                <td></td>
            </tr>
            <tr>
                <td>medal_color</td>
                <td>num</td>
                <td>颜色</td>
                <td></td>
            </tr>
            <tr>
                <td>intimacy</td>
                <td>num</td>
                <td>当前亲密度</td>
                <td></td>
            </tr>
            <tr>
                <td>next_intimacy</td>
                <td>num</td>
                <td>下一等级所需亲密度</td>
                <td></td>
            </tr>
            <tr>
                <td>day_limit</td>
                <td>num</td>
                <td>每日亲密度获取上限</td>
                <td></td>
            </tr>
            <tr>
                <td>today_feed</td>
                <td>num</td>
                <td>今日已获得亲密度</td>
                <td></td>
            </tr>
            <tr>
                <td>medal_color_start</td>
                <td>num</td>
                <td>粉丝勋章颜色</td>
                <td>十进制数，可转为十六进制颜色代码</td>
            </tr>
            <tr>
                <td>medal_color_end</td>
                <td>num</td>
                <td>粉丝勋章颜色</td>
                <td>十进制数，可转为十六进制颜色代码</td>
            </tr>
            <tr>
                <td>medal_color_border</td>
                <td>num</td>
                <td>粉丝勋章边框颜色</td>
                <td>十进制数，可转为十六进制颜色代码</td>
            </tr>
            <tr>
                <td>is_lighted</td>
                <td>num</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>light_status</td>
                <td>num</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>wearing_status</td>
                <td>num</td>
                <td>当前是否佩戴</td>
                <td>0：未佩戴<br>1：已佩戴</td>
            </tr>
            <tr>
                <td>score</td>
                <td>num</td>
                <td></td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>sys_notice</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>id</td>
                <td>num</td>
                <td>id</td>
                <td></td>
            </tr>
            <tr>
                <td>content</td>
                <td>str</td>
                <td>显示文案</td>
                <td></td>
            </tr>
            <tr>
                <td>url</td>
                <td>str</td>
                <td>跳转地址</td>
                <td></td>
            </tr>
            <tr>
                <td>notice_type</td>
                <td>num</td>
                <td>提示类型</td>
                <td>1,2</td>
            </tr>
            <tr>
                <td>icon</td>
                <td>str</td>
                <td>前缀图标</td>
                <td></td>
            </tr>
            <tr>
                <td>text_color</td>
                <td>str</td>
                <td>文字颜色</td>
                <td></td>
            </tr>
            <tr>
                <td>bg_color</td>
                <td>str</td>
                <td>背景颜色</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>sys_notice</code>示例</p>
        <table>
            <thead>
            <tr>
                <th>id</th>
                <th>content</th>
                <th>notice_type</th>
                <th>示例用户</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>5</td>
                <td>该用户存在争议行为，已冻结其帐号功能的使用</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/82385070" target="_blank" rel="noopener noreferrer">82385070<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>8</td>
                <td>该用户存在较大争议，请谨慎甄别其内容</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/28062215" target="_blank" rel="noopener noreferrer">28062215<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>11</td>
                <td>该账号涉及合约争议，暂冻结其账号功能使用。详见公告-&gt;</td>
                <td>1</td>
                <td></td>
            </tr>
            <tr>
                <td>16</td>
                <td>该UP主内容存在争议，请注意甄别视频内信息</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/382534165" target="_blank" rel="noopener noreferrer">382534165<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>20</td>
                <td>请允许我们在此献上最后的告别，以此纪念其在哔哩哔哩留下的回忆与足迹。请点此查看纪念账号相关说明</td>
                <td>2</td>
                <td><a href="https://space.bilibili.com/212535360" target="_blank" rel="noopener noreferrer">212535360<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>22</td>
                <td>该账号涉及合约诉讼，封禁其账号使用</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>24</td>
                <td>该账号涉及合约争议，暂冻结其账号功能使用</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/291229008" target="_blank" rel="noopener noreferrer">291229008<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>25</td>
                <td>该用户涉及严重指控，暂冻结其账号功能使用</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/81447581" target="_blank" rel="noopener noreferrer">81447581<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>31</td>
                <td>该用户涉及严重指控，暂冻结其账号功能使用</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/22439273" target="_blank" rel="noopener noreferrer">22439273<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>34</td>
                <td>该用户涉及严重指控，暂冻结其账号功能使用</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/1640486775" target="_blank"
                       rel="noopener noreferrer">1640486775<span><svg class="external-link-icon"
                                                                      xmlns="http://www.w3.org/2000/svg" aria-hidden="true"
                                                                      focusable="false" x="0px" y="0px"
                                                                      viewBox="0 0 100 100" width="15" height="15"><path
                        fill="currentColor"
                        d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            <tr>
                <td>36</td>
                <td>该账户存在争议，请谨慎甄别</td>
                <td>1</td>
                <td><a href="https://space.bilibili.com/198297" target="_blank" rel="noopener noreferrer">198297<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a><br><a
                        href="https://space.bilibili.com/18149131" target="_blank" rel="noopener noreferrer">18149131<span><svg
                        class="external-link-icon" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
                        x="0px" y="0px" viewBox="0 0 100 100" width="15" height="15"><path fill="currentColor"
                                                                                           d="M18.8,85.1h56l0,0c2.2,0,4-1.8,4-4v-32h-8v28h-48v-48h28v-8h-32l0,0c-2.2,0-4,1.8-4,4v56C14.8,83.3,16.6,85.1,18.8,85.1z"></path><polygon
                        fill="currentColor"
                        points="45.7,48.7 51.3,54.3 77.2,28.5 77.2,37.2 85.2,37.2 85.2,14.9 62.8,14.9 62.8,22.9 71.5,22.9"></polygon></svg><span
                        class="external-link-icon-sr-only">open in new window</span></span></a></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>live_room</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>roomStatus</td>
                <td>num</td>
                <td>直播间状态</td>
                <td>0：无房间<br>1：有房间</td>
            </tr>
            <tr>
                <td>liveStatus</td>
                <td>num</td>
                <td>直播状态</td>
                <td>0：未开播<br>1：直播中</td>
            </tr>
            <tr>
                <td>url</td>
                <td>str</td>
                <td>直播间网页 url</td>
                <td></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>直播间标题</td>
                <td></td>
            </tr>
            <tr>
                <td>cover</td>
                <td>str</td>
                <td>直播间封面 url</td>
                <td></td>
            </tr>
            <tr>
                <td>watched_show</td>
                <td>obj</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>roomid</td>
                <td>num</td>
                <td>直播间 id(短号)</td>
                <td></td>
            </tr>
            <tr>
                <td>roundStatus</td>
                <td>num</td>
                <td>轮播状态</td>
                <td>0：未轮播<br>1：轮播</td>
            </tr>
            <tr>
                <td>broadcast_type</td>
                <td>num</td>
                <td>0</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>live_room</code>中的<code>watched_show</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>switch</td>
                <td>bool</td>
                <td>?</td>
                <td></td>
            </tr>
            <tr>
                <td>num</td>
                <td>num</td>
                <td>total watched users</td>
                <td></td>
            </tr>
            <tr>
                <td>text_small</td>
                <td>str</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>text_large</td>
                <td>str</td>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td>icon</td>
                <td>str</td>
                <td>watched icon url</td>
                <td></td>
            </tr>
            <tr>
                <td>icon_location</td>
                <td>str</td>
                <td>?</td>
                <td></td>
            </tr>
            <tr>
                <td>icon_web</td>
                <td>str</td>
                <td>watched icon url</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>school</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>就读大学名称</td>
                <td>没有则为空</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>profession</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>name</td>
                <td>str</td>
                <td>资质名称</td>
                <td></td>
            </tr>
            <tr>
                <td>department</td>
                <td>str</td>
                <td>职位</td>
                <td></td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td>所属机构</td>
                <td></td>
            </tr>
            <tr>
                <td>is_show</td>
                <td>num</td>
                <td>是否显示</td>
                <td>0：不显示<br>1：显示</td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>user_honour_info</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>mid</td>
                <td>num</td>
                <td>0</td>
                <td></td>
            </tr>
            <tr>
                <td>colour</td>
                <td>str</td>
                <td>null</td>
                <td></td>
            </tr>
            <tr>
                <td>tags</td>
                <td>array</td>
                <td>null</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>series</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>user_upgrade_status</td>
                <td>num</td>
                <td>(?)</td>
                <td></td>
            </tr>
            <tr>
                <td>show_upgrade_window</td>
                <td>bool</td>
                <td>(?)</td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>elec</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>show_info</td>
                <td>obj</td>
                <td></td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>elec</code>中的<code>show_info</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>show</td>
                <td>bool</td>
                <td>是否开通了充电</td>
                <td></td>
            </tr>
            <tr>
                <td>state</td>
                <td>num</td>
                <td>状态</td>
                <td>-1：未开通<br>1：已开通</td>
            </tr>
            <tr>
                <td>title</td>
                <td>str</td>
                <td><code>空串</code></td>
                <td></td>
            </tr>
            <tr>
                <td>icon</td>
                <td>str</td>
                <td><code>空串</code></td>
                <td></td>
            </tr>
            <tr>
                <td>jump_url</td>
                <td>str</td>
                <td><code>空串</code></td>
                <td></td>
            </tr>
            </tbody>
        </table>
        <p><code>data</code>中的<code>contract</code>对象：</p>
        <table>
            <thead>
            <tr>
                <th>字段名</th>
                <th>类型</th>
                <th>内容</th>
                <th>备注</th>
            </tr>
            </thead>
            <tbody>
            <tr>
                <td>is_display</td>
                <td>bool</td>
                <td></td>
                <td>true/false<br>在页面中未使用此字段</td>
            </tr>
            <tr>
                <td>is_follow_display</td>
                <td>bool</td>
                <td>是否在显示老粉计划</td>
                <td>true：显示<br>false：不显示</td>
            </tr>
            </tbody>
        </table>

        """
        api = "https://api.bilibili.com/x/space/wbi/acc/info"
        headers = self.headers
        data = {
            "mid": mid,
        }
        accinfo = requests.get(api, headers=headers, params=wbi(data)).json()
        return accinfo["data"]


# 整合
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

# login_info = asyncio.run(start_login(143474500))
# print(cookies)
