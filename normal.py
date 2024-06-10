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

def getRoomBaseInfo(room_id:int):
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

pprint.pprint(Area_getList())
