#-*-coding: utf-8-*-

from wordpress_xmlrpc.exceptions import ServerConnectionError
from wordpress_xmlrpc import Client,WordPressPost ,WordPressTerm
from wordpress_xmlrpc.methods import posts,taxonomies
from wordpress_xmlrpc.methods.posts import GetPosts,NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from xmlrpc.client import ProtocolError

def wordpress_artice(wppost_status,wp_title,wp_slug_title,wp_content,wp_category,wp_post_tag,
                     wp_host,wp_user,wp_password):
    # 如果遇到错误就出试5次
    success_num = 0
    while success_num < 5:
        try:
            client = Client(wp_host, wp_user, wp_password)

            newpost= WordPressPost() # 创建一个类实例，注意，它不是一个函数。只要在一个类名后面加上括号就是一个实例
            # newpost.post_status = 'draft'
            newpost.post_status = wppost_status
            newpost.slug = wp_slug_title # 文章别名，固定链接形式为文章标题时需要
            # 设置发布目录（一篇文章可以属于多个分类目录）
            newpost.terms_names={
            'category':wp_category,# 目录
            'post_tag':wp_post_tag# 标签
            }
            newpost.title= wp_title
            newpost.content= wp_content
            client.call(posts.NewPost(newpost))  #发布新建的文章，返回的是文章id
            print("Wordpress发布成功：",wp_title)

        except Exception as e:
            print("正在重试:", e)
            success_num = success_num + 1
            continue



if __name__ == '__main__':
    # wp_host = 'https://wordpress.202014.xyz/xmlrpc.php'
    # wp_user = 'root'
    # wp_password = 'kZBHKNVlKObpe@v@BA'

    # config WP 连接设置部分
    wp_host = 'http://144.172.126.40/xmlrpc.php'
    wp_user = 'root'
    wp_password = 'kZBHKNVlKObpe@v@BA'

    wp_category = ['百科']  #  目录
    wp_post_tag = ['有何', '愛因斯坦', '大腦', '2014']  # 标签
    wp_title = "愛因斯坦的大腦有何不同？"
    wp_slug_title = "How are the Albert Einstein’s brain different?"
    wp_content = '''
    <img alt="愛因斯坦的大腦有何不同？的頭圖" id="daily-img" src="https://gss0.bdstatic.com/70cFsj3f_gcX8t7mm9GUKT-xh_/jctuijian/0519/4.jpg"/><div class="cont" id="daily-cont">
<p>自1955年愛因斯坦去世起，科學家一直想弄清究竟他的大腦有什麼特別之處，能讓他對物理學定律有超凡的洞見。這種基於解剖學的研究幾十年前就開始了，進展卻十分緩慢，這是因爲很多腦組織的屍檢圖像和組織切片分散於各處，研究人員很難加以分析。</p><p>2012年11月《大腦》雜誌在線發表文章稱，研究人員綜合迄今爲止所有能收集到的屍檢圖像，詳盡分析後發現，愛因斯坦的大腦皮層（負責腦高級意識過程的腦區）與普通人之間的區別之大，超乎想像。美國佛羅里達州立大學人類學家迪恩·福克（Dean Falk）是這個項目的首席研究員，以下是我們整理後的採訪報導：</p><p><strong>【你們在研究中有什麼發現？】</strong></p><p>愛因斯坦的前額葉皮層非常特別，前額葉皮層屬於大腦表層腦區，位於前額正後方，結構異常複雜。通過與靈長類動物比較，我們發現這一結構在早期人類進化過程中變得高度特化。特別是對人類來說，前額葉皮層負責腦高級認知功能，其中包括工作記憶、計劃制定、計劃實施、憂慮、展望未來以及想像力等。這一腦區高度進化的原因，就在於其中神經元之間錯綜複雜的聯繫。我們推測愛因斯坦的大腦之所以看上去與衆不同，正是由於其中神經元的聯繫更爲複雜。</p><p><strong>【還有什麼不尋常的地方嗎？】</strong></p><p>愛因斯坦大腦最有趣的地方之一，是他的感覺和運動皮層。我們在他運動皮層內的下部發現一個異常區域，這個區域通常負責處理從面部和喉舌傳來的信息。愛因斯坦大腦左半球運動皮層面部區格外擴成一個大矩形，我從來都沒遇過這種情況，也不太確定該怎麼解釋。愛因斯坦有句名言：「My primary process of perceiving is muscular and visual」，說他的見解是圖像和「感覺」的結合，對他而言，思想的基礎不僅要看，也要「摸」。這究竟是什麼意思？我不知道，但對照我們在他運動皮層的發現，兩者倒是相映成趣。</p><p><strong>【你認爲這和那張著名的愛因斯坦吐舌頭的照片有沒有關係？】</strong></p><p>這是三天來我第4次被這麼問了。第一次被問的時候，我很意外，我說我覺得這只是一個巧合。然後我開始認真琢磨這個問題，後來乾脆到鏡子前面親自試試能不能把舌頭伸到他那麼長，結果就差那麼一點點。所以我想，可能照這張照片，只是愛因斯坦一時興起。</p>
</div>
    '''

    # publish：已发布   pending：等待复审  draft：草稿
    wppost_status = "publish"
    wordpress_artice(wppost_status,wp_title,wp_slug_title,wp_content,wp_category,wp_post_tag,wp_host,wp_user,wp_password)