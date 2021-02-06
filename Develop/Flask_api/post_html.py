#-*-coding: utf-8-*-
# 创建时间: 2021/1/9

from multiprocessing import Pool
import requests,json,time
from requests.adapters import HTTPAdapter


def post_mail(title,mail_content,send_mail):
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {"token": '202014xyz',
                "title": title,
                "mail_content": mail_content,
                "send_mail": send_mail,}

            # requests 设置最多五次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            res = s.post(
                url="https://hk-api.202014.xyz/mail",  # HTML文本翻译
                data=post_data,timeout=60,)
            data_txt = res.text
            return data_txt


        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue


def post_img(img_type,content):
    # 如果遇到错误就重试5次
    success_num = 0
    while success_num < 5:
        try:
            post_data = {
                "token": '202014xyz',
                "img_type" : img_type,  #url or html
                "content": content,   }

            # requests 设置最多五次超时
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=5))
            s.mount('https://', HTTPAdapter(max_retries=5))
            res = s.post(
                url="https://hk-api.202014.xyz/img",
                data=post_data,timeout=120,)
            data_txt = res.text
            return data_txt


        except Exception as e:
            print("正在重试:",e)
            success_num = success_num + 1
            continue



def post_google_translate(language,source):
    post_data = {
        "token": '202014xyz',
        "language": language,
        "source": source,
    }

    # requests 设置最多五次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    res = s.post(
        url="https://hk-api.202014.xyz/translate-google",  # 翻译
        data=post_data,timeout=120,)

    data_txt = res.text
    return data_txt


def post_caiyun_translate(language,source):
    post_data = {
        "token": '202014xyz',
        "language": language,
        "source": source,
    }

    # requests 设置最多五次超时
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    res = s.post(
        url="https://hk-api.202014.xyz/translate-caiyun",  # 翻译
        data=post_data,timeout=120,)

    data_txt = res.text
    return data_txt



#列表翻译
def post_list_translate(language,source,api_type="google"):
    txt_list =[]
    for i in source:
        if api_type == "caiyun":
            new_txt = post_caiyun_translate(language, source=i)
        else:
            new_txt = post_google_translate(language, source=i)
        txt_list.append(new_txt)
    return txt_list


def test():
    title = '邮件发送测试'
    send_mail = "1094470534@qq.com"

    mail_content = """
    <p>邮件发送测试</p>
    <p><a href="https://xirikm.net/">这是一个链接</a></p>
    """
    print("正在测试邮件发送系统：",post_mail(title, mail_content, send_mail))


    print("正在测试图床系统：",post_img(img_type="url",content='https://www.jingjiniao.info/data/attachment/block/07/07306bb630860722b381096f4caaaa59.jpg'))

    source='''<div id="daily-cont" class="cont">
    <p>你能想象吗，黑帮们有一天不再打打杀杀，而是武器装备齐全，趁着夜色偷走沙子卖给房地产的开发商们？</p><p>这一幕早在10年前就已经上演了，联合国环境署的研究员曾经在牙买加尼格瑞尔调查海岸侵蚀问题，但分析了各种因素之后都无法找到导致该国的海岸线被破坏的原因，直到他听当地人介绍说，当地的黑帮会装备各种武器，偷走沙子。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/00e93901213fb80e697d08a926d12f2eb938941b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p>于是，该研究人员在当地认真研究，并且研究了各国的沙子用量以及存量，发布了第一个关于沙子的开采综合报告《砂子，比人们想象的更稀缺》，据了解，人类每年沙子使用量，成为了仅次于水资源的第二大资源，然而我们会提倡节约用水，却没人知道沙子也已经濒临枯竭。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/203fb80e7bec54e722407360a9389b504fc26a1b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p>其实，早在许多年前，我国就已经陆续出现了用沙荒，全国多条高速、机场以及建筑都因缺少沙子而停工，各地的砂石价格也从原来的每吨几十元涨到了最高两百元，并且还在不断地上升中。但沙子的缺口依旧很大，据联合国统计，到2030年，全球将可能会面临无沙可用的局面。</p><p>然而我们知道，地球上有许多沙漠，海边也有许多沙滩，那为什么我们不用这些沙子修建建筑呢？</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/7dd98d1001e9390131aee4406bec54e736d1961b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p class="ql-long-560225" style="background: rgb(255, 255, 255); outline: 0px; border: 0px currentColor; border-image: none; color: rgb(51, 51, 51); line-height: 26px; font-family: -apple-system-font, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, sans-serif; font-size: 18px; vertical-align: baseline; white-space: normal; position: relative; -ms-word-break: break-all; -ms-word-wrap: break-word;" data-diagnose-id="77fd343f00af0c4bca5b3bfd260cb44c"><strong>为什么不使用沙漠沙子？<br></strong></p><p>我们知道，由于气候原因，我国西北部地区有许多沙漠，而沙漠中最不缺的就是各种沙子。据统计，沙漠地表面积约占地球陆地表面积的20%，如果我们能够开采这些沙子，将这些沙子用于建筑行业，岂不是可以缓解用沙荒？</p><p>实际上，想法很美好，现实很糟糕。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/55e736d12f2eb9388cc1138cc5628535e5dd6f1b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p>沙子又分为三种：海沙、河沙以及风沙。海沙和河沙一样，都是因为流水侵蚀而形成的沙子，而风沙则是沙漠中的沙子，是由于风力侵蚀而形成的，而目前我们主要使用的沙子则是来源于河沙。</p><p>海沙虽然也可以用于修建建筑，但是海沙中有许多氯化物以及贝壳碎片，想要开采海沙不仅需要专门的大型设备，还要对开采后的沙子进行二次加工，使得开采成本较高。并且海沙中的氯化物会腐蚀混凝土，缩短建筑物使用年限，所以目前并没有作为主流用沙。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/8c1001e93901213fa99f27a244e736d12f2e951b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p>沙漠中的沙子是由风力侵蚀而形成，这些沙子由于长时间的相互摩擦，以至于表面非常光滑，且颗粒非常小，无法聚合在一起，造成修建的建筑物质量较差，无法达到国家标准，所以沙漠中的沙子很少被应用于建筑行业，就连位于沙漠的迪拜，在修建道路时都只能从其他国家进口。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/3801213fb80e7bec47766a9f3f2eb9389b506b1b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p>只有河沙，不仅没有氯化物以及贝壳碎片，而且尺寸和光滑度都刚好符合混凝土的需要，以至于人们开采河沙不仅不需要专业化工具，也不用二次加工，直接可以出售，因此开采成本非常低。所以在过去，人们的采沙力度非常大，甚至有许多偷沙船偷偷开采。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/a2cc7cd98d1001e936907d71a80e7bec54e7971b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p class="ql-long-560225" style="background: rgb(255, 255, 255); outline: 0px; border: 0px currentColor; border-image: none; color: rgb(51, 51, 51); line-height: 26px; font-family: -apple-system-font, &quot;Helvetica Neue&quot;, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, sans-serif; font-size: 18px; vertical-align: baseline; white-space: normal; position: relative; -ms-word-break: break-all; -ms-word-wrap: break-word;" data-diagnose-id="e2a1678af6d7c9656c2e65b9b37f8c7d"><strong>如何缓解用沙荒？</strong></p><p>虽然目前我国多地面临沙子荒，但并不是全球都面临用沙荒。我国之所以会出现沙子资源短缺，是因为我国城市化进程实在是太快了，全国各地都在修建公路、建筑等，以至于沙子的供给量出现短缺。</p><p>而在美国一些城市化进程较慢的地方，当地还是拥有着较多的沙子储备量。只不过从美国运输到中国的路途较远，以至于交通成本非常高昂，远远超出了我们的承担范围，所以我们很少会从遥远的国外进口沙子。</p><p><div class="detail-img-wp"><div class="detail-img-in"><img src="https://iknow-pic.cdn.bcebos.com/b90e7bec54e736d13abfe5768b504fc2d562691b?x-bce-process=image/resize,m_lfit,w_450,h_600,limit_1"></div></div></p><p>除此之外，大量开采河沙还会导致河床被毁坏，河流生态系统遭到破坏，以至于很多国家即使可以开采河沙，也不会轻易开采河沙。</p><p>为了缓解用沙荒，一些国家和地区在已经干枯的河道上开采河沙，还有一些国家正在研究新材料，以便替代河沙。</p><p>但由于全球各地对沙子的需求量大，以至于现如今人们并没有较好的方法来替代沙子，所以未来沙子涨价会必然趋势，而在涨价的过程中，也会反向促进人们积极研究新材料。</p><p>其实用沙荒并不是最近才出现，但由于开采河沙工艺简单，且没有专门的部门管理，以至于很多国家和地区都不知道自己国家每年的沙子产量以及用量。再加上各国都面临着偷采河沙的情况，使得河沙的开采量更加难以追踪。</p><p>在最近几年，各国都已经做出了改进，并且取缔了许多非法采砂厂以及排污不达标的公司，只留下极少数公司维持着全国的沙子供给。</p><p>但由于沙子已经被过度开发，以至于现如今许多工程不得不因为沙子短缺而停工。</p>
    <div class="detail_statement article-source">
    <p class="tit clearfix"><span class="left"></span><span class="center">特别声明</span><span class="right"></span></p>
    <p class="cont">
    本文为自媒体、作者等在百度知道日报上传并发布，仅代表作者观点，不代表百度知道日报的观点或立场，知道日报仅提供信息发布平台。合作及供稿请联系zdribao@baidu.com。</p>
    </div>
    </div>'''

    html = post_img(img_type="html", content=source)
    print(html)


    language = "en"
    # source = ["测试文件","湖南第一师范学院.明天"]
    # print("正在测试翻译系统：",post_list_translate(language,[html],"caiyun")[0])
    # print(post_caiyun_translate(language,source))
    print(post_google_translate(language,html))



def main(source):
    language = "en"
    print(post_google_translate(language, source))

    # print("正在测试图床系统：", post_img(img_type="url",
    #                             content=source))


if __name__ == '__main__':
    # test()

    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    pool = Pool()
    for i in range(10):
        # 因为无法post列表字符，所以先转为str，后端再解析
        source = "湖南第一师范学院"
        # source = 'https://www.jingjiniao.info/data/attachment/block/07/07306bb630860722b381096f4caaaa59.jpg'
        pool.apply_async(func=main, args=(source,))  # 多进程运行
    pool.close()
    pool.join()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print("\n", "开始时间：", start_time + "\n" + "结束时间：", end_time)
