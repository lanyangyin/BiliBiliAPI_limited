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


# pprint.pprint(getFansMembersRank(1703797642))


def dynamic_v1_feed_space(host_mid, all: bool = False) -> list:
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
