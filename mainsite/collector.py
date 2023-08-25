# -*- coding: BIG5 -*-
import requests, time, random, time
from bs4 import BeautifulSoup

def collect_news(date):
    tech_list = []

    udn_item = collect_udn_tech(date)
    if udn_item:
        tech_list.extend(udn_item)

    apple_item = collect_apple_tech(date)
    if apple_item:
        tech_list.extend(apple_item)

    if tech_list:
        store_news(tech_list)

def collect_udn_tech(date):
    udn_list = []
    cate_num = [[123153, "科技新情報"], [123454, "AI浪潮"]]
    
    for cate in cate_num:
        item = udn_tech(cate, date)
        if item:
            udn_list.extend(item)

    return udn_list
            
def udn_tech(cate, date):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    base_url = "https://tech.udn.com/tech/api/article?cate_id={}&limit=20&skip={}&page={}"
    page_num = 1
    skip_num = (20*(page_num-1))
    is_end = False
    udn_list = []

    while True:
        page_url = base_url.format(cate[0], skip_num, page_num)
        r = requests.get(page_url, headers=HEADERS)

        for item in r.json()["lists"]:
            if item["time"]["date"] < date:
                is_end = True
                break
            udn_list.append({"news_source": "聯合新聞網",
                                           "news_cate": cate[1],
                                           "news_title": item["title"],
                                           "news_date": item["time"]["date"],
                                           "news_url": "https://tech.udn.com"+item["url"]})

        if is_end == True:
            break

        page_num += 1    
        time.sleep(random.uniform(1, 2))

    return udn_list   

def collect_apple_tech(date):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    page_url = "https://tw.nextapple.com/realtime/blockchain/"
    page_num = 1
    is_end = False
    apple_list = []

    while True:
        r = requests.get(page_url+str(page_num), headers=HEADERS)
        soup = BeautifulSoup(r.text, features="lxml")
        item_blocks = soup.select("article.post-style3")

        for item_block in item_blocks:
            if item_block.select_one("div").select_one("time").text.replace("/", "-") < date:
                is_end = True
                break

            apple_list.append({"news_source": "壹蘋新聞網",
                                             "news_cate": item_block.select_one("div").find(class_="category blockchain").text,
                                             "news_title": item_block.select_one("div").find(class_="post-title").text,
                                             "news_date": item_block.select_one("div").select_one("time").text.replace("/", "-"),
                                             "news_url": item_block.select_one("a").get("href")})                               

        if is_end == True:
            break

        page_num += 1
        time.sleep(random.uniform(1, 2))

    return apple_list

def get_time(element):
    return element["news_date"]

def store_news(news_list):
    news_list.sort(key=get_time)
    response = requests.post("http://127.0.0.1:8000/api/loginapi/", {"username": "test001", "password": "ggyy123456"})
    token = response.json().get("token")
    headers = {
        "Authorization": f"Token {token}"}
    
    for row in news_list:
        requests.post("http://127.0.0.1:8000/api/newscrawlerapi/", data=row, headers=headers)

    response = requests.post("http://127.0.0.1:8000/api/logoutapi/", headers=headers)
    return response
