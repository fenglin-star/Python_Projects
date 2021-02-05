#coding=utf-8
import requests
import json
import random
import sys
from html.parser import HTMLParser
import re


#彩云小译API tokens，每个每月100字符，超过就无法使用
tokens = [
    "nayce5w4niupbzt7suwv", "oqbk1rmv5klxnunzll9h", "r9f3au6ewp3n21bq2ow9",
    "jqwp6km1cmuh0mc499je", "heh7enay4t0l68w8siyl", "zj0sqg5tpirb873voao2",
    "a8qjh8gins07q72qz2ww", "kbymilu02yje537nxrls", "d3xnbflunxut3hl2i0jv",
    "6se8xvgeeeceyq5cf889", "oo0qkkory6t37b4n55bd", "9sk3sdtwz9afpmkuxe1g",
    "p2j92sxjsrwetvveblwu","8j4802tg30z6xlxks3du","f0fd7fm8e3b823nd4v57",
    "pgbsrsurz2zx36y7xg45","r3f6b9h1j8mej5jeolev"
          ]

def tranlate_tokes(token,source):
    url = "http://api.interpreter.caiyunai.com/v1/translator"
    # WARNING, this token is a test token for new developers, and it should be replaced by your token
    payload = {
        "source": source,
        # 中to英 zh2en     中to日 zh2ja   auto自动识别源语言
        "trans_type": "auto2zh",
        "request_id": "demo",
        "detect": True,
    }
    headers = {
        'content-type': "application/json",
        'x-authorization': "token " + token,
    }

    response = requests.request("POST",url,data=json.dumps(payload), headers=headers,timeout=30)
    return json.loads(response.text)['target']



def caiyun_translate_list(source):
    try:
        i = 1
        while i < 20:
            token = random.choice(tokens)
            try:
                target = tranlate_tokes(token, source)
                return target
                break

            except (KeyError, TypeError) as e:
                print(e,"删除无效toke：", token)
                tokens.remove(token)
                # print(tokens,"  错误代码：",e)
                continue
    except IndexError as e:
        print("所有的彩云小译api都已用完，程序结束")
        sys.exit()


def caiyun_translate_txt(txt):
    list_txt = [txt]
    entxts = caiyun_translate_list(list_txt)
    entxt = entxts[0]
    return entxt


def tj_tokes(source):
    try:
        i = 1
        while i < 20:
            i = i +1
            token = random.choice(tokens)
            try:
                target = tranlate_tokes(token,source)
                print("有效toke：", token ,target)
                pass

            except (KeyError, TypeError) as e:
                tokens.remove(token)
                # print(tokens,"  错误代码：",e)
                continue

    except IndexError as e:
        print("所有的彩云小译api都已用完，程序结束")
        sys.exit()



def parse_html_zh2en(html):
    class MyHTMLParser(HTMLParser):
        def __init__(self, ):
            self.d = []
            super().__init__()

        def handle_data(self, data):
            data = data.strip()  # 去空格
            if len(data) == 0:
                pass
            else:
                self.d.append(data)
                print("Encountered some data:", data)

        def return_data(self):
            return self.d

    parser = MyHTMLParser()
    parser.feed(html)
    html_list = parser.return_data()
    en_html_list = caiyun_translate_list(html_list)

    new_html = html
    for cn,en in zip(html_list,en_html_list):
        html = new_html
        new_html = html.replace(cn,en,1)

    return new_html



if __name__ == '__main__':
    #文本翻译
    print(caiyun_translate_txt("Toke“  ”测试，"))

    #列表翻译
    print(caiyun_translate_list(["Toke“”测试，"]))

    html = '''
    <div class="wp_content_html"><img title="英語學習第一步：你必須要知道從哪裡開始插图" alt="英語學習第一步：你必須要知道從哪裡開始插图" loading="lazy" class="aligncenter size-full wp-image-184502" src="https://www.curiositynews.net/wp-content/uploads/2020/10/17d49d89a99458577af5f6dec03d0a57.png" width="400" height="225" srcset="https://www.curiositynews.net/wp-content/uploads/2020/10/17d49d89a99458577af5f6dec03d0a57.png 400w, https://www.curiositynews.net/wp-content/uploads/2020/10/17d49d89a99458577af5f6dec03d0a57-300x169.png 300w" sizes="(max-width: 400px) 100vw, 400px"><p></p>
    <div class="cont" id="daily-cont">
    <p>如果你只會一種語言，想要學習一門外語（英語）卻不知道該從哪開始入手，Jason 老師的建議會幫你進入真正的英語世界。</p>
    <p><strong>用正確的方式學習正確的詞彙</strong></p>
    <p>學習一門新的語言，意味著要學習新的詞彙，很多詞彙。</p>
    <p>當然很多人都提到學習新單詞時記不住，所以很多人沒開始就退出了。</p>
    <p>但是這裡有最重要的一點，你絕對不需要認識所有的詞彙以後再來說英語，因爲就算是母語，誰也不可能認識所有的單詞。</p>
    <p><strong>通過同源詞彙學習英語單詞</strong></p>
    <p>開始學習一門外語（英語）時你是不是感覺頭都大了？因爲正式學習之前至少要認識幾個單詞，從零開始好像不可能。</p>
    <p>同源詞可以幫我們快速認知新的詞彙，包括自己母語中的詞在目標語言中的對應詞。</p>
    <p>像法語、西班牙語、葡萄牙語、義大利語、有很多單詞和英語單詞一樣。英語最初是在英格蘭的諾曼征服時「借來的」, 已經持續了數百年。像 Action, nation, precipitation, solution, frustration, tradition, communication, extinction, 還有很多以 -tion 結尾的詞在法語中的拼寫是一模一樣的，而且很快就會適應新的發音。把 tion 換成 cion 就是西班牙語，換成 zione 就是義大利語。<img title="英語學習第一步：你必須要知道從哪裡開始插图(1)" alt="英語學習第一步：你必須要知道從哪裡開始插图(1)" loading="lazy" class="aligncenter size-full wp-image-184509" src="https://www.curiositynews.net/wp-content/uploads/2020/10/474df20742a6e64a573c2c8a9993838e.jpg" width="450" height="222" srcset="https://www.curiositynews.net/wp-content/uploads/2020/10/474df20742a6e64a573c2c8a9993838e.jpg 450w, https://www.curiositynews.net/wp-content/uploads/2020/10/474df20742a6e64a573c2c8a9993838e-300x148.jpg 300w" sizes="(max-width: 450px) 100vw, 450px"></p>
    <p>開始學習一門外語時可以很輕鬆，很多詞都有同源詞，我們可以通過同源詞加深對新詞的理解。</p>
    <p><strong>不用出國旅行就可以用英語和外國人互動<br></strong></p>
    <p>很多人都會找藉口，比如沒錢、沒時間、不能去英美國家就學不好英語。</p>
    <p>英美國家的空氣里沒有神奇的物質能讓你會說英語。</p>
    <p>很多人旅居國外也沒學會當地的語言，出國和把自己浸入到一門語言中是 2 個概念，我們需要不斷地聽和用英語才能浸入英語環境中，那麼虛擬的環境有效嗎？當然，從技術上講是可以辦到的，所以你不需要買機票出國。<img title="英語學習第一步：你必須要知道從哪裡開始插图(2)" alt="英語學習第一步：你必須要知道從哪裡開始插图(2)" loading="lazy" class="aligncenter size-full wp-image-184515" src="https://www.curiositynews.net/wp-content/uploads/2020/10/666d519e424c3ecb0b13511fd80ed9b5.gif" width="283" height="170"></p>
    <p><strong>用 skyppe 每天練習英語口語</strong></p>
    <p>你已經一直在聽、看和閱讀英語，這都是在家裡舒適地進行的。現在是時候放大招了，跟英美人在線聊天。</p>
    <p>Jason 老師有一條建議現在還有爭議，但是我還是堅持讓英語初學者必須馬上張口說英語，如果你學英語的目標里涉及口語的話。</p>
    <p>傳統教學和語言系統里這麼做是行不通的，這也是傳統教學讓學生失望的原因，一星期有 7 天，你哪一天才能會說英語呢？</p>
    <p>所以 Jason 老師建議：</p>
    <p>學習一些基本詞彙，留意你已經認知的詞彙，準備幾個小時然後與英美人交流，你只需要準備第一次對話需要的詞彙即可，然後在交流中會發現不足，然後改進，你不能孤立的學習，直到自己模糊的認爲可以對話了才去找英美人交流。</p>
    <p>開始的對話，Jason 老師建議你學會「Hello,」「Thank you,」「Could you repeat that?」or「I don’t understand,」等等。</p>
    <p>如果你還是覺得第一天準備的還是不夠的話，你可以在 skype 窗口邊上打開已經寫好句子的 word 頁面，這樣可以緩解下緊張情緒，也可以隨時參考直到把它們應用自如，遇到生詞還可以隨時查字典。你肯定會問，這是作弊吧? 非也，我們強調的實用，而不是傳統意義的方法。<span style="text-indent: 2em;"></span></p>
    </div>
    </div>
        '''
    new_html = parse_html_zh2en(html)
    print(new_html)

