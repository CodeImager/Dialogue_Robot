#----------------------------------------- 功能区 ----------------------------------------- 
import requests,json,random,re
from lxml import etree
from urllib.request import urlopen
from bs4 import BeautifulSoup

#功能1 天气预报
def act_weater(info_list):
    try:
        outstrs=[]
        page=requests.get("http://wthrcdn.etouch.cn/weather_mini?city=%s"%(info_list)[0])
        data=page.json()
        temperature=data["data"]["wendu"]
        notice=data["data"]["ganmao"]
        outstrs.append("地点：%s\r\n气温：%s\r\n注意：%s" %(info_list,temperature,notice))
        return outstrs[0]
    except BaseException:
        error_print = "输入城市名错误，请重新输入"
        return error_print

#功能2：疫情查询
def epidemic_situation(province):
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    r = requests.get(url, headers)
    res = json.loads(r.text)
    data_res = json.loads(res['data'])
    
    data = data_res['areaTree'][0]['children']
    path = province
    for i in data:
        if path in i['name']:
            for item in i['children']:
                list_city = [
                    '\n'+'地区: ' + str(item['name'])+'\t'
                    ' 确诊人数：' + str(item['total']['confirm'])+'\t'
                    ' 新增确诊：' + str(item['today']['confirm'])+'\t'
                    ' 治愈：' + str(item['total']['heal'])+'\t'
                    ' 死亡：' + str(item['total']['dead']),
                ]
                res_city = ''.join(list_city)
                # 写入爬取到的内容
                with open('./data/epidemic_situation.txt', 'a+', encoding="utf-8") as f:
                    f.write(res_city)
    file_object = open("./data/epidemic_situation.txt","rb")
    # readlines() 返回列表，一行数据就是列表中的一个元素
    contents = file_object.readlines()
    # 遍历列表
    me = []
    for content in contents:
        me.append(content.decode())# 使用decode()解码中文，默认解码格式为utf-8
    file_object.close()
    re = ("".join(me))
    # 清空缓存
    f=open("./data/epidemic_situation.txt", "r+")
    f.seek(0)
    f.truncate(0)
    return re

def province_check (p):
    if (epidemic_situation(p)==""):
        return '我没有查找到这个省份的信息，请检查一下，看看是不是输错了'
    else:
        return epidemic_situation(p)

#功能3：汇率兑换
def Get_huilv(v):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    }
    url = "https://www.huilv.cc/USD_CNY/"
    res = requests.get(url, headers, timeout=2)
    html = etree.HTML(res.text)
    USD_VS_RMB_0 = html.xpath('//div[@id="main"]/div[1]/div[2]/span[1]/text()')
    for a in USD_VS_RMB_0:
        b = a
    USD_VS_RMB_1 = float(b)

    USD_VS_RMB = float(str(USD_VS_RMB_1))
    # 输入带单位的货币金额
    currency_str_value = v
    # 获取货币单位
    unit = currency_str_value[-3:].upper() # 第一次判断
    if unit == 'CNY':
        exchange_rate = 1 / USD_VS_RMB
        string = "美元"
    elif unit == 'USD':
        exchange_rate = USD_VS_RMB
        string = "元"
    else:
        exchange_rate = -1
    if exchange_rate != -1:
        in_money = eval(currency_str_value[0:-3])
        # 使用lambda定义函数
        convert_currency2 = lambda x: x * exchange_rate
        # 调用lambda函数
        out_money = convert_currency2(in_money)
        return '实时汇率为：1 美元 = {} 人民币\n转换后的金额是：{} {} '.format(USD_VS_RMB_1, out_money, string)
    else:
        return '无法计算'

#功能4：笑话
def Joke(joke_start):
    joke_list=[
        "突然想到：假如每个周末都比平时上班更早起，那不就变成一个星期有五天可以多睡一会儿了吗？幸福来得如此突然！" ,
        "一场很大很大的风，吹落了树叶，给我把电动车吹倒了，找不着了...",
        "有些男的真的很幽默。你已经和他交往了半年，他却在某一天突然问你：像你这么优秀的人怎么还没有男朋友？",
        "在公交车上儿子问我，爸：我是不是长得特别丑啊！我对儿子大吼：给你说了多少次了，不要在公共场合叫我爸！"
        "小学开学了，刚满6岁的冬冬不肯到学校上学。妈妈向冬冬解释，小朋友满6岁就要去上学，一直到15岁。最后冬冬终于在书桌前坐下来，满含热泪地问：等我15岁的时候，您会记得来接我吗",
        "本家的一个大爷和大妈吵架，大爷趁大妈烧火做饭的时候，把自己的手机扔到柴火里，说要炸死她...",
        "突然想到：假如每个周末都比平时上班更早起，那不就变成一个星期有五天可以多睡一会儿了吗？幸福来得如此突然！",
        "有个漂亮妹子，补姓熊的和姓余同时喜欢,有一天，那姓熊的向她摊牌，说：鱼与熊掌，不可兼得，你到底要哪一个？妹子来了句：对不起，我不吃荤！"]
    if joke_start=="笑话":
        joke_start=random.choice(joke_list)
        return "{}".format(joke_start)
    elif joke_start=="再来一个":
        joke_start=random.choice(joke_list)
        return "{}".format(joke_start)
    elif joke_start == "结束":
        return '0'
    else:
        return "如果想再听笑话可以输入“再来一个”"
        
#功能5：NBA当日东西部排名
def NBA_rank():
    resp = urlopen('https://m.hupu.com/nba/stats')
    soup = BeautifulSoup(resp,'html.parser')
    east = soup.find_all('li',class_= "weast")[0]
    west = soup.find_all('li',class_= "weast")[1]
    rankHtml = '今日NBA东部排名：（1.排名  2.球队  3.胜负  4.胜负差  5.最近情况）' + '\n' + '\n'
    for tag in east.find_all('li', class_=''): 
        list = tag.find('p', class_='right-data')
        rankHtml = rankHtml + tag.find('span', class_='rank').get_text() + '. ' + tag.find('div', class_='').h1.get_text() + '    ' + list.find_all('span')[0].get_text() + '    ' + list.find_all('span')[1].get_text() +'    '+ list.find_all('span')[2].get_text() +'\n'

    rankHtml = rankHtml + '\n' + '\n' + '---------------------------------------------' + '\n' + '\n'
    rankHtml = rankHtml + '今日NBA西部排名：（1.排名  2.球队  3.胜负  4.胜负差  5.最近情况）' + '\n' + '\n'        
    for tag in west.find_all('li', class_=''): 
        list = tag.find('p', class_='right-data')
        rankHtml = rankHtml + tag.find('span', class_='rank').get_text() + '. ' + tag.find('div', class_='').h1.get_text() + '    ' + list.find_all('span')[0].get_text() + '    ' + list.find_all('span')[1].get_text() +'    '+ list.find_all('span')[2].get_text() +'\n'
    
    return rankHtml

#功能6：脑筋急转弯
def Brain_twists(message):
    questions = [
        "埋在地下一千年的酒，出来以后叫什么?",
        "有一只猪，它走啊走啊，走到了英国,结果他变成了什么?",
        "上课老师抽查背课文,小猪,小狗,小猫都举手了,老师会叫谁?",
        "蝴蝶, 蚂蚁, 蜘蛛, 蜈蚣,他们一起工作,最后哪一个没有领到酬劳?",
        "动物园里大象的鼻子最长,那第二长的是谁呢?",
        "哪种水果视力最差?",
        "一只乌龟从一堆大便上走过，却只在上面留下3个脚印,为什么？",
        "人为什么要走去床上睡觉呢?",
        "原来其实是斯巴达800勇士，为什么到了电影里面变成300了？",
        "小强为什么能用一只手让车子停下来？",
        "如果有一辆车,司机是王子,乘客是公主,请问这辆车是谁的呢?",
        "金木水火土，谁的腿长？",
        "一颗心值多少钱?",
        "台风天气要带多少钱才能出门?",
        "要考试了,不能看什么书?",
        "如果明天就是世界末日，为什么今天就有人想自杀？",
        "布和纸怕什么？",
        "铅笔姓什么？"
    ]
    answers = [
        "酒精",
        "Pig",
        "小狗",
        "蜈蚣",
        "小象",
        "芒果",
        "有一只脚捏着鼻子呢",
        "床不会自己走过来",
        "伍佰去唱歌了",
        "打的",
        "如果的",
        "火腿肠",
        "1亿",
        "四千万",
        "百科全书",
        "去天堂占位置",
        "一万和万一",
        "萧"
    ]
    reasons = [
        "",
        "",
        "因为旺旺仙贝",
        "因为无功不受禄",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "因为一心一意",
        "因为台风天气没事(四)千万要出门.",
        "百科全输",
        "",
        "不(布)怕一万，只(纸)怕万一",
        "削(萧)铅笔"
    ]
    global i
    i = random.randint(0,len(questions)-1)
    if message == "开始" or message == "继续":
        question_return = questions[i]
        return question_return
    elif message == "结束":
        return '0'
    elif message == answers[i]:
        return "回答正确，输入”继续“可继续下一题"
    elif message == "答案":
        answer_return = answers[i]+'\n'+reasons[i]
        return answer_return
    elif message != answers[i]:
        return "回答错误，再仔细想想？"+'\n'+"实在想不出来可以输入“答案”进行查看"

#功能7：对话
#将问-答语句输入X-Y中
def XY(user_input):

    #读取分词后的对话文本
    f = open('data/chatterbot.txt','r',encoding='utf-8')
    subtitles = f.read()

    X = []
    Y = []

    #将对话文本切分
    subtitles_list = subtitles.split('E')

    #将"问句"放入X中，将”答句“放入Y中
    for q_a in subtitles_list:
        if re.findall('.*M.*M.*',q_a,flags=re.DOTALL):
            q_a = q_a.strip()
            q_a_pair = q_a.split('M')

            X.append(q_a_pair[1].strip())
            Y.append(q_a_pair[2].strip())

    f.close()

    for i in range(len(X)):
        if X[i] == user_input:
            return Y[i]
    
    return '你问的问题太复杂了，我还没学会哦'