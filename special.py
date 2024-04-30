# coding=utf-8
import math
import pprint
import time

import requests

from tool import check_config, dict2cookieformat

cookie = dict2cookieformat(list(check_config().values())[0])
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
    (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "cookie": cookie,
}


def getFansMembersRank(uid: int) -> list:
    """
    通过用户的B站uid查看他的粉丝团成员列表
    :param uid:B站uid
    :return: list元素：[{face：头像url，guard_icon：舰队职位图标url，guard_level：舰队职位 1|2|3->总督|提督|舰长，honor_icon：""，level：粉丝牌等级，medal_color_border：粉丝牌描边颜色数值为 10 进制的 16 进制值，medal_color_start：勋章起始颜色，medal_color_end：勋章结束颜色，medal_name：勋章名，name：用户昵称，score：勋章经验值，special：""，target_id：up主mid，uid：用户mid，user_rank：在粉丝团的排名}]
    """
    api = "https://api.live.bilibili.com/xlive/general-interface/v1/rank/getFansMembersRank"
    page = 0
    maxpage = 1
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


# pprint.pprint(getFansMembersRank(1703797642))


def dynamic_v1_feed_space(host_mid, all: bool = False) -> list:
    """

    @param host_mid:
    @param all:
    @return:
    """
    api = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
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


# pprint.pprint(dynamic_v1_feed_space(143474500, all=True))

