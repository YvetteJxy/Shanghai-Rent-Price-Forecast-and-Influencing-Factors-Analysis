import requests
from lxml import etree
from sklearn import preprocessing as prep
import random
import time
import pandas as pd
import numpy as np
import csv
import json
import math
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.mlab as mal
import seaborn as sns
from pyecharts.charts import Map, Geo
from pyecharts import options as opts
from sklearn.tree import DecisionTreeRegressor  
from sklearn.ensemble import RandomForestRegressor 
from sklearn.ensemble import AdaBoostRegressor 
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neighbors import LocalOutlierFactor

#伪装请求头
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
 
def getHeaders():
    user_agent = user_agents[random.randint(0, len(user_agents)-1)] 
    headers = {
        'User-Agent': user_agent
    }
    return headers
 
 
#对一个URL发送请求，解析结果，获取所需数据
def get_data(url):
    #反爬虫策略1：随机取headers
    response = requests.get(url, headers=getHeaders(), stream=True)
    tree = etree.HTML(response.text)
    # 定位到content__list
    li_list = tree.xpath('//div[@class="content w1150"]/div[@class="content__article"]/div[@class="content__list"]/div')
    # all_house_list = []
    for li in li_list:
        try:
             Nbhood = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()')[0].strip().split(' ')[0].split('·')[1]
             HouseOrientation = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()')[0].strip().split(' ')[2]
             District = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a/text()')[0]
             Location = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/a/text()')[1]
             Size = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()')[4].strip()
             Size = float(Size.replace("㎡",""))
             HouseType = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()')[6].strip()
             BedRoom = int(HouseType[0])
             LivingRoom = int(HouseType[2])
             Toilet = int(HouseType[4])
             High = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/span[@class="hide"]/text()')[1].strip()
             High = High.split()
             Height = High[0]
             ##Floor = High[1].replace("（","").replace("）","").replace("层","")
             Floor = int(High[1][1:-2])
             releaseTime = li.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--brand oneline"]/span[@class="content__list--item--time oneline"]/text()')[0]
             releaseTime = int(releaseTime[0])
             Rent = li.xpath('.//div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()')[0]
             Rent = float(Rent)
             all_house_list.append((Nbhood,HouseOrientation,District,Location,Size,BedRoom,LivingRoom,Toilet,Height,Floor,releaseTime,Rent))
        except:
            continue
        
    return all_house_list
  
#循环爬取所需租房信息
num = [94,87,47,68,70,101,94,44,64,101,4,46,3,18,71,50]
distr = ["jingan","xuhui","huangpu","changning","putuo","pudong","baoshan","hongkou","yangpu","minhang","jinshan","jiading","chongming","fengxian","songjiang","qingpu"]
#pages = ['https://sh.lianjia.com/zufang/jingan/pg{}rt200600000001/#contentList'.format(x) for x in range(1,3)]
all_house_list = []
count = 0
for i in range(len(num)):
    if num[i]!=101 :
        u = "https://sh.lianjia.com/zufang/"+distr[i]+"/pg{}rco11rt200600000001/#contentList"
        #https://sh.lianjia.com/zufang/xuhui/pg2rco11/#contentList
        pages = [u.format(x) for x in range(1,num[i])]         
    else:
      if distr[i]=='pudong':
        u = "https://sh.lianjia.com/zufang/pudong/pg{}rco11rt200600000001erp5999/#contentList"  
        pages = [u.format(x) for x in range(1,97)]
        u = "https://sh.lianjia.com/zufang/pudong/pg{}rco11rt200600000001brp6000erp8999/#contentList"
        pages.extend([u.format(x) for x in range(1,78)])
        u = "https://sh.lianjia.com/zufang/pudong/pg{}rco11rt200600000001brp9000/#contentList"
        pages.extend([u.format(x) for x in range(1,64)])
      else:
        u = "https://sh.lianjia.com/zufang/minhang/pg{}rco11rt200600000001erp7999/#contentList"  
        pages = [u.format(x) for x in range(1,100)]
        u = "https://sh.lianjia.com/zufang/minhang/pg{}rco11rt200600000001brp8000/#contentList"
        pages.extend([u.format(x) for x in range(1,37)])
    for page in pages:
         a = get_data(page)
        #反爬虫策略2：每次爬取随机间隔5-10s
         time.sleep(random.randint(5,10))
         count=count+1
         if count%100 == 0:
            print ('the '+str(count)+' page is successful')  
 
name = ["小区","朝向","行政区","街区","房屋面积","卧室","客厅","厕所","楼层相对位置","楼层","发布时长","每月租金"]
page_data = pd.DataFrame( columns= name,data=all_house_list)#25905
#查看每一列是否存在缺失值
page_data.isnull().sum()#无缺失值
page_data.drop_duplicates(subset=None,keep='first',inplace=True)#25830
page_data.to_csv(r'D:\上财\研一\数据处理与可视化\final\house1.csv',encoding="utf_8_sig")

house = page_data.sample(n=5000,random_state=3264,axis=0)
house.index=[i for i in range(house.shape[0])]
#百度地图定位
def baidu_loc(addr):
    url = "http://api.map.baidu.com/geocoding/v3/?" #百度地图API接口
    para = {
        "address": addr, #传入地址参数
        "output": "json",
        "ak": "biFo8fEyBFeVU8o3R5GV4rp93gCNlBxV" #百度地图开放平台申请ak
    }
    req = requests.get(url,para)
    req = req.json()
    m = req["result"]["location"]
    g = f"{m['lng']},{m['lat']}"
    return g

NHood = house.loc[:,("行政区","街区","小区")]
NHood.drop_duplicates(subset=None,keep='first',inplace=True)
NHood.index=[i for i in range(NHood.shape[0])]
NHood["经度"] = ""
NHood["纬度"] = ""

N2 = pd.read_csv(r'F:\本科\毕业论文\df2.csv')
for i in range(len(NHood)):
    if NHood['小区'][i] in N2["小区"].values:
       NHood['经度'][i] = float(N2.loc[N2.loc[:,"小区"]==NHood['小区'][i],"经度"])
       NHood['纬度'][i] = float(N2.loc[N2.loc[:,"小区"]==NHood['小区'][i],"纬度"])
    else:
      NHood['经度'][i] = 0.0
      NHood['纬度'][i] = 0.0
                        
for i in range(len(NHood)):
  if NHood['经度'][i] == 0.0:
    try:
       r = baidu_loc("上海"+NHood["行政区"][i]+NHood["街区"][i]+NHood["小区"][i])
    except:
        try:
           r = baidu_loc("上海"+NHood["行政区"][i]+NHood["小区"][i])
        except:
          try:
           r = baidu_loc("上海"+NHood["小区"][i])
          except:
           r = '0.0,0.0'
    r = r.split(",")
    NHood["经度"][i] = float(r[0])
    NHood["纬度"][i] = float(r[1])
'''
for i in range(len(NHood)):
    if NHood["经度"][i]<120.52 or NHood["经度"][i]>122.12 or NHood["纬度"][i]<30.40 or NHood["纬度"][i]>31.53:
        out = NHood["小区"][i]
        NHood = NHood.drop(NHood[(NHood["小区"]==out)].index)#6855
        page_data = page_data.drop(page_data[(page_data["小区"]==out)].index)#22922
'''
NHood.to_csv(r'D:\上财\研一\数据处理与可视化\final\nhood1.csv',encoding="utf_8_sig")
NHood = pd.read_csv(r'D:\上财\研一\数据处理与可视化\final\nhood2.csv')

def get_directory(keyword,radius,choice): #定义圆形区域检索函数
    for i in range(len(NHood)):
        location=str(NHood["纬度"][i])+","+ str(NHood["经度"][i]) #构造圆中心点的经纬度               
        url="http://api.map.baidu.com/place/v2/search?query="+keyword+"&page_size=20&page_num=0&location="+location+"&radius="+str(radius)+"&output=json&ak=KREinqYEY6GxnCmg8a2imRHgHKHmP00A&scope=2"#
        #print(url) #测试请求接口拼接是否正确，此url可以直接复制到浏览器查看返回结果
        response=requests.get(url) #发出请求
        answer=response.json()
        if choice==2:
            count = 0
            min_d = radius
            try:
               for k in range(len(answer['results'])):
                   distance=answer['results'][k]['detail_info']['distance'] #距离
                   if distance<=min_d:
                       min_d = distance
                       count = count + 1
            except:
               print("第"+str(i)+"个小区"+NHood["小区"][i]+"应当扩大radius")
            if count == 0:
                min_d = radius+1 
            distances.append(min_d)
        elif choice==3:
             counts.append(answer['total'])
            #centers.append(NHood["小区"][i])
        else:
            print("输入错误的choice")    
            break
        
##地铁站
distances = []
if __name__=='__main__':
    get_directory("地铁站",1000,2) #调用函数get_directory
    dict={"距离":distances} #构造字典
    df_subway=pd.DataFrame(dict)
NHood["1000米内最近地铁站距离"] = df_subway["距离"]
##最近公交车站
distances = []
if __name__=='__main__':
    get_directory("公交车站",1000,2) #调用函数get_directory
    dict={"距离":distances} #构造字典
    df_bus=pd.DataFrame(dict)
NHood["1000米内最近公交车站距离"] = df_bus["距离"]
##购物
counts = []
if __name__=='__main__':
    get_directory("购物中心",1000,3) #调用函数get_directory
    dict={"数量":counts} #构造字典
    df_buy=pd.DataFrame(dict) 
NHood["1000米内购物中心数量"] = df_buy["数量"]
##公司数量
counts = []
if __name__=='__main__':
    get_directory("公司",1000,3) #调用函数get_directory
    dict={"数量":counts} #构造字典
    df_company=pd.DataFrame(dict)
NHood["1000米内公司数量"] = df_company["数量"]
##旅游景点数量
counts = []
if __name__=='__main__':
    get_directory("公园",1000,3) #调用函数get_directory
    dict={"数量":counts} #构造字典
    df_tour=pd.DataFrame(dict)
NHood["1000米内公园数量"] = df_tour["数量"]
##医院
counts = []
if __name__=='__main__':
    get_directory("综合医院",1000,3) #调用函数get_directory
    dict={"数量":counts} #构造字典
    df_h1=pd.DataFrame(dict)
counts = []
if __name__=='__main__':
    get_directory("专科医院",1000,3) #调用函数get_directory
    dict={"数量":counts} #构造字典
    df_h2=pd.DataFrame(dict)
NHood["1000米内医院数量"] = df_h1["数量"]+df_h2["数量"]

NHood.to_csv(r'D:\上财\研一\数据处理与可视化\final\nhood3.csv',encoding="utf_8_sig") 
NHood = pd.read_csv(r'D:\上财\研一\数据处理与可视化\final\nhood3.csv')

def  class_d(x):
    if 0<x<=500:
        x=1
    elif 500<x<=1000:
        x=2
    else:
        x=3
    return(x)

NHood["1000米内最近地铁站距离"] = NHood["1000米内最近地铁站距离"].apply(class_d)
NHood["1000米内最近公交车站距离"] = NHood["1000米内最近公交车站距离"].apply(class_d)

house['经度'] = ''
house['纬度'] = ''
house['1000米内最近地铁站距离'] = ''
house['1000米内最近公交车站距离'] = ''
house['1000米内购物中心数量'] = ''
house['1000米内公司数量'] = ''
house['1000米内公园数量'] = ''
house['1000米内医院数量'] = ''

for i in range(house.shape[0]):
  try:
    house['经度'][i] = float(NHood.loc[NHood['小区']==house['小区'][i],"经度"])
    house['纬度'][i] = float(NHood.loc[NHood['小区']==house['小区'][i],"纬度"])
    house['1000米内最近地铁站距离'][i] = int(NHood.loc[NHood['小区']==house['小区'][i],"1000米内最近地铁站距离"])
    house['1000米内最近公交车站距离'][i] = int(NHood.loc[NHood['小区']==house['小区'][i],"1000米内最近公交车站距离"])
    house['1000米内购物中心数量'][i] = int(NHood.loc[NHood['小区']==house['小区'][i],"1000米内购物中心数量"])
    house['1000米内公司数量'][i] = int(NHood.loc[NHood['小区']==house['小区'][i],"1000米内公司数量"])
    house['1000米内公园数量'][i] = int(NHood.loc[NHood['小区']==house['小区'][i],"1000米内公园数量"])
    house['1000米内医院数量'][i] = int(NHood.loc[NHood['小区']==house['小区'][i],"1000米内医院数量"])
  except:
      print(house['小区'][i])
house.isnull().sum()

def  class_h(x):
    if x == '错层':
        x=1
    elif x == '复式':
        x=2
    elif x == '跃层':
        x=3
    else:
        x =4
    return(x)

def is_south(x):
    if x=='错层' or x=='复式' or x=='跃层':
        x=1
    else:
        x=x.split('/')
        if '南' in x:
            x=1
        else:
            x=0
    return(x)
    
house['房屋类型'] = house['朝向'].apply(class_h)
house['是否朝南'] = house['朝向'].apply(is_south)  
house.to_csv(r'D:\上财\研一\数据处理与可视化\final\house2.csv',encoding="utf_8_sig")

df = house.drop(["小区","街区","朝向"],axis = 1) 
df.to_csv(r'D:\上财\研一\数据处理与可视化\final\house3.csv',encoding="utf_8_sig")


