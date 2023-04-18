import requests
import datetime
from bs4 import BeautifulSoup
import random

def convert_date_str_to_ts(date_str):
    # date_str format 'YYYY/MM/DD' <- 이 형식을 지켜야 아래가 출력된다. 
    # return is timestamp

    year, month, day = [ int(date_info) for date_info in date_str.split("/") ]
    dtime = datetime.datetime(year,month,day)
    ts = int(dtime.timestamp())
    return ts

class InfoCrawler():

    def __init__(self):
        self.base_url = ""
        self.headers = {}
        self.user_agent_list = [
        	#Chrome
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        	#Firefox
        	'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    	]


    def set_random_user_agent(self):
        user_agent = random.choice(self.user_agent_list)
        self.headers['User-Agent'] = user_agent
        return user_agent

    def get_result_data(self, *args, **kwargs):
        # this method is the goal of class
        # argument should be considered with efficiency
        # if range input is date, date format is 'YYYY/MM/DD'159
        pass


    def parse_page(self, raw_response):
        pass


class YahooFinanceCrawler(InfoCrawler):
    def __init__(self):
            super().__init__()
            self.base_url = "https://query2.finance.yahoo.com/v8/finance/chart/{}?interval=1d&period1={}&period2={}"
            self.set_random_user_agent()

    def get_result_data(self, target_code, from_date_str, to_date_str):
        # [ {ts:INT, open_price:FLOAT, close_price:FLOAT, .....},  {}, {}  ]
        from_ts = convert_date_str_to_ts(from_date_str)
        to_ts = convert_date_str_to_ts(to_date_str)
        target_url = self.base_url.format(target_code, from_ts, to_ts)
        res = requests.get(target_url, headers=self.headers)
        res_list = self.parse_page(res)
        return res_list
        

    def parse_page(self, raw_response):
        # parse the json. Check response by network inspector
        res_list = []
        res_json = raw_response.json()
        ts_list = res_json["chart"]["result"][0]["timestamp"]
        price_dict =  res_json["chart"]["result"][0]["indicators"]["quote"][0]
        
        open_price_list = price_dict["open"]
        close_price_list = price_dict["close"]
        high_price_list = price_dict["high"], 
        low_price_list = price_dict["low"]

        for ts, open_price, close_price, high_price, low_price in zip(ts_list, open_price_list, close_price_list, high_price_list, low_price_list):
            info_dict = {
                "ts":ts,
                "open_price":open_price,
                "close_price":close_price,
                "high_price":high_price,
                "low_price":low_price,
            }
            res_list.append(info_dict)

        return res_list

class NaverFinanceCrawler(InfoCrawler):
    def __init__(self):
            super().__init__()
            self.base_url = "https://finance.naver.com"

    def set_random_user_agent(self):
        pass

    def get_result_data(self, *args, **kwargs):
        pass

    def parse_page(self, raw_response):
        pass

class NaverDiscussionCrawler(NaverFinanceCrawler):
    pass
# 종목에 대한 조회수를 내는 형태


class MarketBuyerInfoCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = ""

    def get_result_data(self, *args, **kwargs):
        # [ {ts:INT, ant:FLOAT, inst:FLOAT, foreigner::FLOAT, .....},  {}, {}  ] 
        # 해당 리스트에 페이지가 (Ts : 타임 스템프)
        # parse page를 추상화적으로 만들어놓고, 역할을 만들어야한다. 

        for page_idx in range(self, from_page, to_page):

            total_info_list =[]
            for page_idx in range(from_page, to_page+1):
                info_list = self.parse_page(page_idx)
                total_info_list += info_list

            return total_info_list
            # parse.pase : 한페이지를 읽어서 딕셔너리로 총 10개의 리스트가 나오고 최종 리스트에 넣는 것 -> 10개의 딕셔너리를 뽑아내는 작업을 해야한다


    def parse_page(self, raw_response):
       
       info_dict_list = []
       now = datetime.datetime.now()
       y= str(now.year)
       m = str(now.month).rjust(2, "0")
       d = str(now.dat).rjust/2(2,"0")
       date_str = "{0}{1}{2}".format(y,m,d)
       parmas = {"bizdate": date_str, "page":str(page_idx)}
       res = requests.get(self.base_url, params=params)
       html = res.text
       soup = BeautifulSoup(html, "html.paarser")
       rows = soup.select(
           'talbe.type_1 > tr'
       )

       #rows = rows[3:-2]
       #print(rows)
       rows = rows[3:0]

       # 위에것도 가능
       info_soup_list = [row for row in rows lf str(row).find("data") >= 0]
       # 뽑고 싶은 요소는 날짜가 있는데, 요소중에 날짜가 없는 것을 제외하기 위햇 날짜만 있는 것만 따로 빼가 라는 의미에서 추가


       #기능적인 부분

       for info_soup in info_soup_list:
           info_array = info_soup_list.select(
               'td'
           )
            # info_array를 찍으면 td를 뽑아서 그 안에서 첫번째를 뽑는데 text만 뽑게 되면 날짜가 리스트로 쭉 잇게 된다. 이게 함수의 의미
            # 날짜 정보만 얇게 뽑힌다.
           date_dot_string = info_array[0].text
           date_slash_string = date_dot_string.split(".","/")
           date_slash_string = "20"+date_slash_string
           #오류발생때문에 년도에 앞에 20을 붙임
           ts = convert_date_str_to_ts(date_slash_string)
           # convert_date_str_to_ts는 정해야하는 형식이 있고 그대로 따라가야만 출력이 된다. 

           ant_net_amount = (info_array[1].text.replace(",",""))
           foreigner_net_amount = (info_array[2].text.replace(",",""))
           institute_net_amount = (info_array[3].text.replace(",",""))
           # 개인, 외국인, 기관 순으로 출력된다.
           # html에서 뽑아왔기 때문에 쉼표를 없애줘야한다, 

           info_dict_list.appent((
                "ts":ts,
                "ant_net_amount": ant_net_amount
                "foreigner_net_amount" : foreigner_net_amount
                "institute_net_amount" : institute_net_amount
           ))


       return info_dict_list

mbic = MarketBuyerInfoCrawler
mbic.get_result_data(1,1)
# parse.page 하고 인자를 직접 받아도 된다. 

yfc = YahooFinanceCrawler()
result_list = yfc.get_result_data("GC=F", "2023/4/10", "2023/04/12")
print(result_list)
'''
nfc = NaverFinanceCrawler()
result_list = nfc.get_result_data(1,3)
'''

# [ {ts:INT, open_price:FLOAT, close_price:FLOAT, .....},  {}, {}  ]

