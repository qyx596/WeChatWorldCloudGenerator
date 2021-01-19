import sqlite3
import pandas as pd
import jieba
from wordcloud import WordCloud
import random
import hashlib
import matplotlib.pyplot as plt
jieba.enable_paddle() #启用paddlepaddle分词

DATABASE_PATH = 'WECHATFILES/wechat.sqlite' #微信聊天记录数据库路径
CSV_PATH = 'WECHATFILES/cleandata.csv' #处理后聊天记录保存路径
CONTACTBASE_PATH = 'WECHATFILES/WCDB_Contact.sqlite' #微信联系人数据库路径
WORDLIST_PATH = 'WECHATFILES/wordlist.txt' #分词保存路径
MASK_PATH = 'SOURCE/heart.jpg' #词云背景图片路径
FONT_PATH = 'SOURCE/simhei.ttf' #词云字体路径
WORDCLOUD_IMAGE_PATH = 'result.png' #词云图片保存路径
NICK_NAME = '' #联系人备注或微信号


def getContact(CONTACTBASE_PATH=CONTACTBASE_PATH):
    try:
        conn_contact = sqlite3.connect(CONTACTBASE_PATH)
        contact = pd.read_sql('select dbContactRemark, userName from Friend', conn_contact)
        contact['dbContactRemark'] = contact['dbContactRemark'].str.decode('utf-8')
        wechat_id = contact[contact['dbContactRemark'].str.contains(NICK_NAME)]['userName'].values[0]
        wechat_id_encode = hashlib.md5(wechat_id.encode('utf-8')).hexdigest()
        conn_contact.close()
        print('获取联系人ID成功！')
    except:
        print('获取联系人ID失败！')
    return wechat_id_encode

def getChat2csv(wechat_id_encode, DATABASE_PATH=DATABASE_PATH):
    try:
        conn_chat = sqlite3.connect(DATABASE_PATH)
        chat = pd.read_sql('select Des,Message from Chat_' + wechat_id_encode, conn_chat)
        cleandata = chat[(chat['Des'] == 0) & (~chat['Message'].str.contains('<roomid>')) & (~chat['Message'].str.contains('<msg>'))]
        cleandata.to_csv(CSV_PATH, sep=',', index=False)
        conn_chat.close()
        print('获取聊天记录成功！')
    except:
        print('获取聊天记录失败！')

def csvProcess(CSV_PATH=CSV_PATH, WORDLIST_PATH=WORDLIST_PATH):
    print('开始分词...')
    try:
        with open(CSV_PATH, 'r') as f:
            content = f.read()
        remove_words = ["，", "!", "。", '\n', '\xa0', "我", "你", "的", "了", "就", "吗", "嗯", "哈","不", "不是", "现在", "然后","啊","是","要","没","又","那","也", \
              "有","想","去","这","个","还","都","会","啥","吧","说","真","呢","呀","得","到","看","啦","咋","老","什么","他们","别","给","刚刚","哼","跟","能","过",
              "一","人","他"] #移除常用语气词
        for i in remove_words:
            content = content.replace(i, '')
        splitWords = jieba.cut(content, use_paddle=True)
        with open(WORDLIST_PATH, 'w') as f:
            for i in splitWords:
                f.write(str(i) + ' ')
        print('分词成功！')
    except:
        print('分词失败！')

def random_Color_func(word=None, font_size=None, position=None,  orientation=None, font_path=None, random_state=None):
        h  = random.randint(320,350)
        s = int(100.0 * 255.0 / 255.0)
        l = int(100.0 * float(random.randint(60, 120)) / 255.0)
        return "hsl({}, {}%, {}%)".format(h, s, l)

def generateImage(MASK_PATH=MASK_PATH, WORDLIST_PATH=WORDLIST_PATH, FONT_PATH=FONT_PATH, WORDCLOUD_IMAGE_PATH=WORDCLOUD_IMAGE_PATH):
    try:
        custom_mask = plt.imread(MASK_PATH)
        with open(WORDLIST_PATH, 'r') as f:
            txt = f.read()
        wcloud = WordCloud(background_color='white',
                        width=800,
                        height=800,
                        mask=custom_mask,
                        color_func=random_Color_func,
                        font_path=FONT_PATH).generate(txt)
        wcloud.to_file(WORDCLOUD_IMAGE_PATH)
        print("词云生成成功！")
    except:
        print("词云生成失败！")

if __name__ == '__main__':
    target_contact_id = getContact()
    getChat2csv(target_contact_id)
    csvProcess()
    generateImage()