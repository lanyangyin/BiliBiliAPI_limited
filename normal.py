# coding=utf-8
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
        <td>live_status</td>
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
    """
    api = "https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld"
    data = {
        "mid": mid,
    }
    RoomInfoOld = requests.get(api, headers=headers, params=data).json()
    return RoomInfoOld["data"]


print(getRoomInfoOld(67141))


def v1_Room_get_info():
    api = "https://api.live.bilibili.com/room/v1/Room/get_info"



















