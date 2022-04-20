#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
=================================================
@Project -> File   ：douban_data_crawler -> test
@IDE    ：PyCharm
@Author ：Young
@Date   ：2021/8/18 22:37
@Desc   ：
==================================================
"""
import random

if __name__ == '__main__':
    # count = 101
    # step = 20
    # _ = list(range(0, count))[0::step]
    # list_list = [[start, step] for start in _]
    # for start, step in list_list:
    #     print(start, step)
    print(random.randint(0,9))


    from lxml import etree
    from lxml.etree import HTMLParser
    text = """
    
<div class="grid-view">
        

        <div class="item" >
            <div class="pic">
                <a title="오징어 게임" href="https://movie.douban.com/subject/34812928/" class="nbg">
                    <img alt="오징어 게임" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2677934359.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/34812928/" class="">
                            <em>鱿鱼游戏 / 오징어 게임</em>
                             / 第六轮 / Squid Game
                        </a>
                    </li>
                        <li class="intro">2021-09-17(韩国) / 李政宰 / 朴海秀 / 魏化俊 / 孔刘 / 李秉宪 / 吴永洙 / 郑浩妍 / 许成泰 / 金周灵 / 李瑜美 / 阿努帕姆·特里帕蒂 / 金英玉 / 金范来 / 李书焕 / 金英善 / 朴惠珍 / 姜末琴 / 杰弗里·朱利亚诺 / 约翰 D.迈克斯 / 丹尼尔·C·肯尼迪 / 李政俊 / 许栋元 / 斯蒂芬妮·小村 / 林基雄 / 韩国 / 黄东赫 / 60分钟 / 鱿鱼游戏 / 悬疑 / 惊悚 / 黄东赫 Dong-hyuk Hwang / 韩语</li>
                    <li>
                                    <span class="rating4-t"></span>
                        <span class="date">2021-10-11</span>
                        
                    </li>
                    <li>
                        <span class="comment">8分，世人真是太喜欢大逃杀题材了，从戈尔丁的蝇王、深作欣二的大逃杀，到狩猎、黄渤的一出好戏，大家一遍又一遍的翻拍荒岛逃生题材，各种人性丑陋险恶暴露干净随便就可以拍几部，以至于2021年网飞拍出来，已经能够滴水不漏、层层剖开、又精确无误得满足观众对人性恶的需求了，是的，观众非常需要看到人性恶的一面，简直如一场饕餮盛宴，但依然有致命缺点，那就是男一的伪善，把男主的自私和软弱隐藏的极其深，从头到尾男一并无真正付出过，喂流浪猫照顾弱者不过是自己力所能及的玩乐，而从一开始没有自控力且自私，面对老人必须是不忍心但被迫接受20个弹珠，面对独木桥必须是为了满足别人被迫选的最后号牌，最后必须是女主生命垂危被迫进入决赛，从来没有真正面临死亡道德选择，才能如此从容的站在道德高点指责，这就是伪善和软弱，是创造者的傲慢！</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="闯入者" href="https://movie.douban.com/subject/20514902/" class="nbg">
                    <img alt="闯入者" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2242132737.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/20514902/" class="">
                            <em>闯入者</em>
                             / 闯入者* / Red Amnesia
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2014-09-04(威尼斯电影节) / 2015-04-30(中国大陆) / 吕中 / 冯远征 / 秦海璐 / 秦昊 / 石榴 / 黄素影 / 韩艺博 / 许守钦 / 李苒苒 / 张颂文 / 中国大陆 / 王小帅 / 106分钟(中国大陆) / 110分钟(多伦多电影节) / 剧情 / 犯罪 / 惊悚 / 王小帅 Xiaoshuai Wang / 方镭 Lei Fang / 李非 Fei Li / 汉语普通话</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-10-11</span>
                        
                            <span class="tags">标签: 2015 王小帅 文革</span>
                    </li>
                    <li>
                        <span class="comment">6.5分，有时候一直在想，北京大院走出来的这些导演是不是永远困在自己那个胡同里了？冯小刚的老炮、姜文的大院、王朔的胡同、王小帅的工厂故事，反反复复变换花样，旧时代工厂故事加青春怀旧是标配，再加点文艺范高级感，怕观众太疏离就再加点悬疑魔幻元素，但扒开一看，不还是原地打圈，怀念往事怀念自己的青春吗？</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="ร่างทรง" href="https://movie.douban.com/subject/35208823/" class="nbg">
                    <img alt="ร่างทรง" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2661923862.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/35208823/" class="">
                            <em>灵媒 / ร่างทรง</em>
                             / 萨满(台) / 凶灵祭(港)
                        </a>
                    </li>
                        <li class="intro">2021-07-14(韩国) / 纳瑞拉·库尔蒙科尔佩特 / 萨尼·乌托玛 / 邦松·纳卡普 / Sirani Yankittikan / 亚沙卡·柴松 / 泰国 / 韩国 / 班庄·比辛达拿刚 / 130分钟 / 灵媒 / 恐怖 / 罗泓轸 Hong-jin Na / 班庄·比辛达拿刚 Banjong Pisanthanakun / 泰语</li>
                    <li>
                                    <span class="rating2-t"></span>
                        <span class="date">2021-10-09</span>
                        
                            <span class="tags">标签: 2021</span>
                    </li>
                    <li>
                        <span class="comment">典型的装神弄鬼，犯了所以恐怖片都会犯的错误，为了把宗教故事讲到底，为了给人想象解读的空间而漏洞百出，另外伪纪录片形式用到这简直就是反面教材</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="Mulan" href="https://movie.douban.com/subject/26357307/" class="nbg">
                    <img alt="Mulan" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2590336843.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/26357307/" class="">
                            <em>花木兰 / Mulan</em>
                             / 木兰传说 / 花木兰真人版
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2020-09-04(美国网络) / 2020-09-11(中国大陆) / 刘亦菲 / 甄子丹 / 巩俐 / 李连杰 / 李截 / 安柚鑫 / 马泰 / 赵家玲 / 郑佩佩 / 温明娜 / 曾晓童 / 袁文忠 / 唐辰瀛 / 道阿·茂阿 / 黄谷悦 / 尼尔森·李 / 李勋 / 饶雪晶 / 袁之正 / 仁成外桥 / 加里·扬 / 邝泰恩 / 乌特卡什·安邦德卡尔 / 钱姆·艾希勒珀拉 / 大卫·T·林 / 詹森·郑 / Jun Yu / 美国 / 加拿大 / 中国香港 / 妮琪·卡罗 / 115分钟 / 花木兰 / 动作 / 冒险 / 古装 / 劳伦·希内克 Lauren Hynek / 里克·杰法 Rick Jaffa / 伊丽莎白·马丁 Elizabeth Martin / 阿曼达·斯尔沃 Amanda Silver / 英语 / 汉语普通话</li>
                    <li>
                                    <span class="rating1-t"></span>
                        <span class="date">2021-10-09</span>
                        
                    </li>
                    <li>
                        <span class="comment">确实是刘亦菲也挽救不回来的烂，逻辑没有高潮也没有，别说和中国文化一点也没有，就算有，女性觉醒和气有什么关系吗，怎么莫名其妙就觉醒了</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="Malignant" href="https://movie.douban.com/subject/25909236/" class="nbg">
                    <img alt="Malignant" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2672792129.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/25909236/" class="">
                            <em>致命感应 / Malignant</em>
                             / 恶煞(港) / 疾厄(台)
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2021-09-01(法国) / 2021-09-10(美国) / 安娜贝拉·沃丽丝 / 麦蒂·哈森 / 吴宇卫 / 米歇尔·沃特 / 麦肯娜·格瑞丝 / 珍·路易莎·凯利 / 苏珊娜·汤姆森 / 杰克·阿贝尔 / 杰奎琳·麦根斯 / 克里斯蒂安·克莱门松 / 梅塞德斯·科隆 / 英格丽·比苏 / 乔恩·李·布罗迪 / 保拉·马绍尔 / 佐伊·贝尔 / 娜塔莉·萨福兰 / 迈克·门德兹 / 雷·蔡斯 / 帕翠西娅·维拉奎兹 / 麦迪逊·沃尔夫 / 安迪·比恩 / 帕特里克·考克斯 / 蕾妮·戴蒙德 / 玛丽娜·马泽帕 / 基诺·蒙特斯诺斯 / 阿米尔·阿布莱拉 / 肖特·丽奈特·约翰逊 / 杰苏斯·特鲁希略 / 鲁本·普拉 / 丹·拉莫斯 / 丽莎·卡塔拉 / 美国 / 中国大陆 / 温子仁 / 112分钟 / 108分钟(中国网络) / 致命感应 / 悬疑 / 恐怖 / 阿克拉·库珀 Akela Cooper / 温子仁 James Wan / 英格丽·比苏 Ingrid Bisu / 英语</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-10-08</span>
                        
                    </li>
                    <li>
                        <span class="comment">没想到又玩出了新花样</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="Who Am I - Kein System ist sicher" href="https://movie.douban.com/subject/25932086/" class="nbg">
                    <img alt="Who Am I - Kein System ist sicher" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2201518484.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/25932086/" class="">
                            <em>我是谁：没有绝对安全的系统 / Who Am I - Kein System ist sicher</em>
                             / 黑客搏击会(港) / Who Am I - No System Is Safe
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2014-09-25(德国) / 汤姆·希林 / 埃利亚斯·穆巴里克 / 沃坦·维尔克·默林 / 汉娜·赫茨施普龙 / 崔娜·蒂虹 / 李奥那多·卡劳 / 小安托万·莫诺特 / 利奥波德·霍尔农 / 卡塔琳娜·马茨 / 阿尔恩特·施韦林·索瑞 / 德国 / www.whoami-film.de/site/ / 巴伦·博·欧达尔 / 102分钟 / 我是谁：没有绝对安全的系统 / 犯罪 / 悬疑 / 惊悚 / Baran bo Odar / Jantje Friese / 德语 / 英语</li>
                    <li>
                                    <span class="rating2-t"></span>
                        <span class="date">2021-10-07</span>
                        
                    </li>
                    <li>
                        <span class="comment">漏洞百出吧</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="双旗镇刀客" href="https://movie.douban.com/subject/1307812/" class="nbg">
                    <img alt="双旗镇刀客" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2553119558.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/1307812/" class="">
                            <em>双旗镇刀客</em>
                             / The Swordsman in Double Flag Town
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">1991-05-17(中国大陆) / 高一玮 / 赵玛娜 / 常江 / 孙海英 / 王刚 / 中国大陆 / 何平 / 91分钟 / 动作 / 冒险 / 武侠 / 何平 Ping He / 杨争光 Zhengguang Yang / 汉语普通话</li>
                    <li>
                                    <span class="rating5-t"></span>
                        <span class="date">2021-10-07</span>
                        
                            <span class="tags">标签: 1991</span>
                    </li>
                    <li>
                        <span class="comment">9分，极其精简的故事和动作，三刀撑起了整部电影：一刀劈羊，赢得了老丈和好妹的尊重，一刀劈霸凌者，赢回了正义，一刀劈一刀仙，平定了自己和双旗镇的危机。沙里飞这个角色简直神来之笔，正义不是靠别人帮来的，全靠自己争取来的</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="八佰" href="https://movie.douban.com/subject/26754233/" class="nbg">
                    <img alt="八佰" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2615992304.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/26754233/" class="">
                            <em>八佰</em>
                             / 八百启示录 / 战争启示录之八百壮士
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2020-08-14(大规模点映) / 2020-08-21(中国大陆) / 王千源 / 张译 / 姜武 / 黄志忠 / 张俊一 / 欧豪 / 杜淳 / 魏晨 / 张宥浩 / 唐艺昕 / 李九霄 / 李晨 / 梁静 / 侯勇 / 辛柏青 / 俞灏明 / 刘晓庆 / 姚晨 / 郑恺 / 余皑磊 / 黄晓明 / 徐嘉雯 / 张承 / 马精武 / 胡晓光 / 陆思宇 / 白恩 / 曹璐 / 刘云龙 / 杨嘉华 / 中泉英雄 / 高爽 / 郑伟 / 高冬平 / 黄米依 / 曹卫宇 / 宋洋 / 徐乐同 / 徐幸 / 阮经天 / 杜子蓝 / 陈果 / 秦越 / 邵老五 / 文森特·马蒂尔 / 塞缪尔D.T.麦基 / 常海军 / 李卓航 / 大卫·塞默里 / 丹尼尔·克劳泽 / 詹卢卡·佐帕 / 莱昂内尔·鲁道 / 杰古 / 奥梅尔·尤祖亚克 / 斯图尔特·D·拉瑟姆 / 特里·科米尔 / 布罗诺·巴塔拉 / 付紫铉 / 石佳禾 / 横井哲也 / 刘航宇 / 松田笃儿 / 李惊澜 / 乌雪晨 / 持田健人 / 庞国昌 / 韩帅 / 孔祥海 / 刘彦希 / 中国大陆 / 管虎 / 147分钟(公映版) / 160分钟(上海电影节) / 剧情 / 历史 / 战争 / 管虎 Hu Guan / 葛瑞 Rui Ge / 汉语普通话 / 日语 / 英语</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-10-07</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="寻枪" href="https://movie.douban.com/subject/1305224/" class="nbg">
                    <img alt="寻枪" src="https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2184558984.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/1305224/" class="">
                            <em>寻枪</em>
                             / The Missing Gun
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2002-05-09(中国大陆) / 姜文 / 宁静 / 伍宇娟 / 刘小宁 / 石凉 / 韩三平 / 中国大陆 / 陆川 / 90分钟 / 120分钟(美国) / 犯罪 / 剧情 / 悬疑 / 陆川 Chuan Lu / 贵州话</li>
                    <li>
                                    <span class="rating4-t"></span>
                        <span class="date">2021-10-06</span>
                        
                            <span class="tags">标签: 陆川</span>
                    </li>
                    <li>
                        <span class="comment">风格化明显，电影拍完以后陆川也很尴尬，成也姜文败也姜文</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="送你一朵小红花" href="https://movie.douban.com/subject/35096844/" class="nbg">
                    <img alt="送你一朵小红花" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2618247457.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/35096844/" class="">
                            <em>送你一朵小红花</em>
                             / A Little Red Flower
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2020-12-31(中国大陆) / 易烊千玺 / 刘浩存 / 朱媛媛 / 高亚麟 / 夏雨 / 岳云鹏 / 陈祉希 / 李晓川 / 孔琳 / 吴晓亮 / 张绍刚 / 孙强 / 安笑歌 / 李增辉 / 姚未平 / 张浩天 / 柴陆 / 中国大陆 / 韩延 / 128分钟 / 剧情 / 韩延 Yan Han / 韩今谅 Jinliang Han / 贾佳薇 Jiawei Jia / 于勇敢 Yonggan Yu / 李晗 Han Li / 汉语普通话</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-10-04</span>
                        
                    </li>
                    <li>
                        <span class="comment">7.5分，现在大数据商业片太精确了，癌症➕亲情➕爱情，每一步都要踩在泪点上，该轻松的时候轻松，该哭的时候哭，连起来又太刻意，电影的问题就是精确过头了</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="少年巴比伦" href="https://movie.douban.com/subject/25876760/" class="nbg">
                    <img alt="少年巴比伦" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2410887742.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/25876760/" class="">
                            <em>少年巴比伦</em>
                             / 路小路，你有种！ / Young Love Lost
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2015-06-18(上海电影节) / 2017-01-13(中国大陆) / 董子健 / 李梦 / 尚铁龙 / 李大光 / 唐小然 / 张陆 / 杨皓宇 / 刘惠 / 宫海滨 / 李洋 / 付强 / 刘忠哲 / 刘思博 / 田旭东 / 嘟嘟 / 李思宁 / 鲁野 / 高浩元 / 佟磊 / 巴特尔 / 黄小兰 / 中国大陆 / 相国强 / 96分钟 / 剧情 / 喜剧 / 爱情 / 陈健忠 Jianzhong Chen / 路内 Nei Lu / 汉语普通话</li>
                    <li>
                                    <span class="rating4-t"></span>
                        <span class="date">2021-10-03</span>
                        
                            <span class="tags">标签: 2017</span>
                    </li>
                    <li>
                        <span class="comment">7.9分，整体流畅亲切，观感舒适，李梦演的白蓝气质真好，少年的成熟就在一夜之间，已经远超很多青春片了</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="피에타" href="https://movie.douban.com/subject/10487226/" class="nbg">
                    <img alt="피에타" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p1699450600.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/10487226/" class="">
                            <em>圣殇 / 피에타</em>
                             / 圣母怜子图 / 母与子
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2012-09-04(威尼斯电影节) / 2012-09-06(韩国) / 李廷镇 / 赵敏修 / 伍基洪 / 姜恩珍 / 权律 / 许俊硕 / 孙钟学 / 陈庸旭 / 刘河福 / 赵载龙 / 金在祿 / 宋文洙 / 韩国 / pieta.kr / 金基德 / 103分钟 / 圣殇 / 剧情 / 金基德 Ki-duk Kim / 韩语</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-10-03</span>
                        
                    </li>
                    <li>
                        <span class="comment">6.5分，装的厉害，和莫比乌斯环一样，电影冷冰冰粗糙的像一块石头，输出全靠砸</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="The Shape of Water" href="https://movie.douban.com/subject/26752852/" class="nbg">
                    <img alt="The Shape of Water" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2506388632.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/26752852/" class="">
                            <em>水形物语 / The Shape of Water</em>
                             / 忘形水(港) / 水底情深(台)
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2017-08-31(威尼斯电影节) / 2017-12-01(美国) / 2018-03-16(中国大陆) / 莎莉·霍金斯 / 道格·琼斯 / 迈克尔·珊农 / 理查德·詹金斯 / 奥克塔维亚·斯宾瑟 / 迈克尔·斯图巴 / 大卫·休莱特 / 尼克·瑟西 / 斯图尔特·阿诺特 / 尼格尔·本内特 / 劳伦·李·史密斯 / 马丁·罗奇 / 阿莱格拉·富尔顿 / 约翰·卡普洛斯 / 摩根·凯利 / 马文·凯伊 / 德鲁·维尔戈维尔 / 凯伦·格莱夫 / 丹·莱特 / 辛迪·戴 / 吉尔莫·德尔·托罗 / 布兰登·麦克奈特 / 美国 / 加拿大 / 墨西哥 / 吉尔莫·德尔·托罗 / 123分钟 / 水形物语 / 剧情 / 爱情 / 奇幻 / 吉尔莫·德尔·托罗 Guillermo del Toro / 瓦内莎·泰勒 Vanessa Taylor / 英语 / 美国手语 / 俄语 / 法语</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-10-02</span>
                        
                    </li>
                    <li>
                        <span class="comment">7分，除了跨种族的爱情外没有任何亮点，不要再为了政治正确而正确了</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="东" href="https://movie.douban.com/subject/1870250/" class="nbg">
                    <img alt="东" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2551994632.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/1870250/" class="">
                            <em>东</em>
                             / Dong
                        </a>
                    </li>
                        <li class="intro">2006-09-05(威尼斯电影节) / 2006-11-18(中国香港) / 刘小东 / 韩三明 / 中国大陆 / 中国香港 / 贾樟柯 / 66 分钟 / Canada: 66 分钟(Toronto International Film Festival) / 纪录片 / 剧情 / 贾樟柯 Zhangke Jia / 汉语普通话 / 泰语</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-09-29</span>
                        
                    </li>
                    <li>
                        <span class="comment">真的就只是纪录片，但内容还是不错，认真作画，用力活着，刘小东一生画的都是未被侵犯的肉体和原始生命力</span>
                        
                    </li>
                </ul>
            </div>
        </div>
        

        <div class="item" >
            <div class="pic">
                <a title="受益人" href="https://movie.douban.com/subject/30299311/" class="nbg">
                    <img alt="受益人" src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2572429001.jpg" class="">
                </a>
            </div>
            <div class="info">
                <ul>
                    <li class="title">
                        <a href="https://movie.douban.com/subject/30299311/" class="">
                            <em>受益人</em>
                             / My Dear Liar
                        </a>
                            <span class="playable">[可播放]</span>
                    </li>
                        <li class="intro">2019-11-08(中国大陆) / 大鹏 / 柳岩 / 张子贤 / 张邵勃 / 刘刚 / 龙洁 / 陈卫 / 彭波 / 苏娜 / 唐茜 / 邓飞 / 陈正华 / 徐玉琨 / 丁文博 / 李宜儒 / 曹宇宙 / 马昕墨 / 李季 / 潘高琼 / 杨常金 / 王议伟 / 张傲然 / 中国大陆 / 申奥 / 112分钟 / 剧情 / 喜剧 / 爱情 / 申奥 Ao Shen / 许渌洋 Luyang Xu / 王燕秋 Yanqiu Wang / 汉语普通话</li>
                    <li>
                                    <span class="rating3-t"></span>
                        <span class="date">2021-09-29</span>
                        
                    </li>
                    <li>
                        <span class="comment">7.5分，大鹏能继续专注演一个小角色也很不容易了</span>
                        
                    </li>
                </ul>
            </div>
        </div>
</div>
    """

    text2 = '''
    <div>
        <ul>
             <li class="item-0"><a href="link1.html">第一个</a></li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0"><a href="link5.html">a属性</a>
         </ul>
     </div>
    '''



    html=etree.HTML(text,etree.HTMLParser())
    html21 = etree.HTML(text)  # 初始化生成一个XPath解析对象
    result = etree.tostring(html21, encoding='utf-8')  # 解析对象输出代码
    print(type(html21))
    print(type(result))
    print(result.decode('utf-8'))