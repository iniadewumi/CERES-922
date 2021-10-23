

import re, requests
from datetime import datetime, timedelta
from selenium import webdriver
from time import sleep
import pandas as pd
from lxml.html import fromstring
                   
variables = {}


headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}


    
def check_response(response):   
    status_code = response.status_code
    #**********************************************************
    history = [x for x in response.history if x.status_code==301]
    redirecting = len(history)>0
    encoding = response.encoding
    header = response.headers

    resp_status = f"Basics:\nRedirecting: {redirecting}\nEncoding: {encoding}\nHeader: {header}\n"

    if response.status_code != 200:
        print(f"Response Code {response.status_code}\nRequest Failed")
        raise requests.exceptions.RequestException(f'Request unsuccessful, try again. Status Code is {response.status_code}, not 200!')
    if redirecting:
        print("NOTE: This link redirects, please check to ensure it is the correct link")

    return resp_status




class Investing:

    def __init__(self):
        try:
            self.base_url = 'https://www.investing.com/commodities/'
            self.main_url = self.base_url+'crude-oil-technical?period=86400'
            self.response = requests.get(self.main_url, headers=headers)
            self.data = self.response.text.replace("\\", "").replace("\n", "").replace("\t", "")
        except Exception as e:
            print(e)
            raise Exception(self.__name__, "\n\nInitialization failed. Check internet connection and if website is online")
            

                
    def get_basic_info(self):
        try:
            re.search(r'"inlineblock">(.*?) <i', self.data).group(1)
        except Exception as e:
            print(e)
            raise Exception("\n\nRegex Failed on initial response data!")
       
        check_response(self.response)
        oil_price = re.search(r'id="last_last" dir="ltr">(.*?)</span><span', self.data).group(1)
        time_stamp = re.search(r'time">(.*?)</span><span', self.data).group(1)
        latency = re.search(r'class="bold"></span>(.*?)<span class=', self.data).group(1).split(".")[0].replace(" - ", "")

        self.basic_info = pd.DataFrame(columns=["Source", "Price", "Time Stamp", "Latency"])
        self.basic_info.loc[0] = ("Investing", "$"+oil_price, time_stamp+" ET", latency)
        return self.basic_info

    def get_indicator(self):
        #HOURLY
        summ = re.search(r'techStudiesInnerWrap">(.*?)</div></div>', self.data).group(1)
    
        sum_indic = re.search(r'title="">(.*?)</span', summ.split("summaryTa")[0]).group(1)
        ma_indic = re.search(r'bold">(.*?)</span', summ.split("summary")[2]).group(1)
        tech_indic = re.search(r'bold">(.*?)</span', summ.split("summary")[3]).group(1)
        
        oil_tech_hourly = f"<strong>Summary (Hourly): {sum_indic.upper()}</strong><br>Moving Averages (Hourly): {ma_indic.upper()}<br>Other Technical (Hourly): {tech_indic.upper()}<br>" 
        

        
        #DAILY
        headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        data = requests.get("https://www.investing.com/commodities/crude-oil-technical?period=86400", headers=headers).text.replace("\\", "").replace("\n", "").replace("\t", "")
        summ = re.search(r'techStudiesInnerWrap">(.*?)</div></div>', data).group(1)
        
        sum_indic = re.search(r'title="">(.*?)</span', summ.split("summaryTa")[0]).group(1)
        ma_indic = re.search(r'bold">(.*?)</span', summ.split("summary")[2]).group(1)
        tech_indic = re.search(r'bold">(.*?)</span', summ.split("summary")[3]).group(1)
        
        oil_tech_daily = f"<strong>Summary (Daily): {sum_indic.upper()}</strong><br>Moving Averages (Daily): {ma_indic.upper()}<br>Other Technical (Daily): {tech_indic.upper()}" 
            
        return f"{oil_tech_hourly}<br>{oil_tech_daily}"
        

    def get_articles(self):
        response = requests.get(self.base_url + "crude-oil-news", headers=headers)
        out_articles = [] 
        articles = fromstring(response.text).find_class("mediumTitle1")[0].findall("article")
        
        for ind, item in enumerate(articles[:3]):
            item.make_links_absolute("https://www.investing.com")
            article = item.getchildren()
            p = item.xpath(f'//article[{ind+1}]/div[1]/p')[0].text_content().split("-")            
            img = article[0].values()[0]
            
            try:
                source_ = item.xpath(f'//article[{ind+1}]/div[1]/span')[0].text_content().replace("By ", "")
            except:
                source_ = 'Unspecified'
                
                
            if len(p)>1:
                by = p[0]
                news_text = p[1]
            else:
                by = 'By: Unspecified'
                news_text = p[0]
            
            if len(source_.split("-"))>1:
                source = source_.split("-")[0]
                time = source_.split("-")[1].split("\n")[0]
            else:
                source = source_
                time=""
        
            link = article[1].getchildren()[0].values()[0]
            title = article[1].getchildren()[0].values()[1]
            
            out_articles.append({'img':img, 'link':link, 'title': title, 'source':source, 'time':time, 'by': by, 'news_text': news_text})
            
        return out_articles
            
    
    def get_analysis(self):
        response = requests.get(self.base_url + "crude-oil-opinion", headers=headers)
        out_anals= [] 
        anals = fromstring(response.text).find_class("mediumTitle1")[0].findall("article")
                
        for ind, item in enumerate(anals[:3]):
            item.make_links_absolute("https://www.investing.com")
            article = item.getchildren()
            p = item.xpath(f'//article[{ind+1}]/div[1]/p')[0].text_content().split("-")       
            img = article[0].values()[0]
            
            try:
                source_ = item.xpath(f'//article[{ind+1}]/div[1]/span')[0].text_content().replace("By ", "")
            except:
                source_ = 'Unspecified'
                
                
            if len(p)>1:
                by = p[0]
                news_text = p[1]
            else:
                by = 'By: Unspecified'
                news_text = p[0]
            
            if len(source_.split("-"))>1:
                source = source_.split("-")[0]
                time = source_.split("-")[1].split("\n")[0]
            else:
                source = source_
                time = "Unknown"
            
        
            link = article[1].getchildren()[0].values()[0]
            title = article[1].getchildren()[0].values()[1]
            
            out_anals.append({'img':img, 'link':link, 'title': title, 'source':source, 'time':time, 'by': by, 'news_text': news_text})
        return out_anals
        
        
class OilPrice:
    def __str__(self):
        return self.__name__
    def __init__(self):
        try:
            self.url = 'https://oilprice.com/Energy/Oil-Prices/'
            self.response = requests.get(self.url, headers=headers)
            self.data = re.search(r'"Crude Oil WTI">(.*?)fa fa-caret', self.response.text.replace("\t", "").replace("\n", "")).group(1)

        except Exception as e:
            print(e)
            raise Exception(self.__name__, "\n\nInitialization failed. Check internet connection and if website is online")

    def get_basic_info(self):
        try:
            re.search(r'"value">(.*?) <i', self.data).group(1)
        except Exception as e:
            print(e)
            raise Exception("\n\nRegex Failed on initial response data!")

        check_response(self.response)
        oil_price = re.search(r'"value">(.*?) <i', self.data).group(1)
        latency = re.search(r'"last_updated">(.*?)</span', self.data).group(1)
        if int(latency.split(" ")[0]):
            
            time_stamp = (datetime.now()-timedelta(minutes=int(latency.split(" ")[0]))).strftime("%H:%M") 
        else:
            time_stamp = (datetime.now()-timedelta(minutes=10)).strftime("%H:%M") 
        
        
        self.basic_info = pd.DataFrame(columns=["Source", "Price", "Time Stamp", "Latency"])
        self.basic_info.loc[0] = ("Oil Price", "$"+oil_price, time_stamp+ " CST", latency+" delay")
        return self.basic_info
    

    
class CMEGroup:
    def __init__(self):
        self.url = "https://www.cmegroup.com/CmeWS/mvc/Quotes/Future/425/G?pageSize=50&_=1618193766629"
        self.response = requests.get(self.url, headers=headers)
        self.data = self.response.json()   
        self.wti = self.data['quotes'][0]

    def get_basic_info(self):
        oil_price = f"${self.wti['last']}"
        time_stamp = self.wti["updated"].split("<")[0]
        latency = self.data['quoteDelay']
        
        self.basic_info = pd.DataFrame(columns=["Source",  "Price", "Time Stamp", "Latency"])
        self.basic_info.loc[0] = ("CME Group", oil_price, time_stamp, latency+" delay")
        return self.basic_info

    def get_general_info(self):            
        prior = self.wti['priorSettle']
        open_ = self.wti["open"]
        change = self.wti['change']
        high = self.wti['high']
        low = self.wti['low']
        volume = self.wti['volume']
        
        return f"Prior Settle:   ${prior}    <br>Open:   ${open_}    <br>Change:   {change}<br>High:   ${high}<br>Low:   ${low}<br>Volume:   {volume}"

