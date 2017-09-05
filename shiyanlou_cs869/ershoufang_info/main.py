# _*_ coding: utf-8 _*_
# filename: main.py

import sys
import csv

from urllib import urlopen
from bs4 import BeautifulSoup

from house_info import house

# 将从 citys.csv 文件中读取的城市信息保存到字典中
def get_city_dict():

    # 创建城市字典，保存信息
    city_dict = {}

    # 将 citys.csv 中的数据读取到 city_dict 中
    with open("./citys.csv", "r") as f:
        reader = csv.reader(f)

        for city in reader:

            # 字典格式： {city_name: city_url}
            city_dict[city[0]] = city[1]

    return city_dict

# 将城市对应的区域信息保存到字典中
def get_district_dict(url):
    # 将信息保存到字典中
    district_dict = {}

    html = urlopen(url).read()
    bsobj = BeautifulSoup(html, "html5lib")
    # 通过浏览器的开发者工具分析页面源码，容器 
    # <div data-role="ershoufang"> 下的每一个 <a> 标签对应一条信息
    # 得到<div data-role="ershoufang"> 下的每一个 <a> 标签
    roles = bsobj.find("div", {"data-role": "ershoufang"}).findChildren("a")
    '''
        roles 内数据的格式如下

        <a href="/ershoufang/jinjiang" title="成都锦江在售二手房 ">锦江</a>
        <a href="/ershoufang/gaoxing" title="成都高新在售二手房 ">高新</a>
        <a href="/ershoufang/qingyang" title="成都青羊在售二手房 ">青羊</a>
        ...

    '''
    for role in roles:
        # 对应区域的 url
        district_url = role.get("href").encode("utf-8")
        # 对应区域的名称
        district_name = role.get_text().encode("utf-8")
        # 保存在字典中
        district_dict[district_name] = district_url
    return district_dict

def run():
    city_dict = get_city_dict()

    # 打印城市名
    for city in city_dict.keys():
        print city,
    print

    input_city = raw_input("请输入城市：")
    city_url = city_dict.get(input_city)

    # 输入错误，退出程序
    if not city_url:
        print "输入错误"
        sys.exit()

    # 在新获取的城市 url 中，已有相应的后缀，此处不需要手动添加后缀
    # ershoufang_city_url = city_url + "ershoufang"
    ershoufang_city_url = city_url

    district_dict = get_district_dict(ershoufang_city_url)

    # 打印区域名
    for district in district_dict.keys():
        print district,
    print

    input_district = raw_input("请输入地区：")
    district_url = district_dict.get(input_district)

    # 输入错误，退出程序
    if not district_url:
        print "输入错误"
        sys.exit()

    # district_url="/ershourfang/gaoxin"，我们只需后面的"gaoxin"，
    # 即该字符串第十二个字符开始，所以此处将"1"修改为"12"
    # house_info_url = city_url + district_url[1:]
    house_info_url = city_url + district_url[12:]
    print house_info_url
    house(house_info_url)

if __name__ == "__main__":
    run()
