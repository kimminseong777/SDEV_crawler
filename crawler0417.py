
import requests
import datetime
from bs4 import BeautifulSoup
import random
import pandas as pd

def convert_date_str_to_ts(date_str):
    # date_str format 'YYYY/MM/DD'
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

    def save_result_date(self, dict_list, file_path):
        result_df = pd.DateFrame(dict_list)
        result_df.to_csv(file_path)
        # 엑셀로 나오는 형태를 csv로 저장하는 형태

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


    def get_result_data(self, *args, **kwargs):
        pass

    def parse_page(self, raw_response):
        pass

class NaverDiscussionCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = self.base_url + "/item/board.naver"

    def get_result_data(self, code, from_page, to_page):
            # [ {ts:INT, view_count:INT},  {}, {}  ]
            # marketBuyerinfoCrawler 와 같은 구조
        
        total_info_list = []
        for page_idx in range(from_page, to_page+1):
            info_list = self.parse_page(page_idx)
            total_info_list += info_list

        return total_info_list
        
    def parse_page(self, code, page_idx):
        # 한페이지를 읽어내는 코드로
        params = {"code":str(code), "page":str(page_idx)}
        #코드랑 페이지
        res = requests.get(self.base_url, params=params, headers=self.headers)
        html = res.text
        print(html)
        soup = BeautifulSoup(html, "html.parser")
        # 어떻게 저기만 뽑아야할 것인가. 페이지 코드를 보고 뽑아야할 부분을 찾아보고 특징을 찾아보면 된다.
        rows = soup.select(
            'table.type2 > tr'
        )
        Info_Soup_List = [row for row in rows if str(row).find('mouseOut') >= 0]
        print(Info_Soup_List)
        date_view_selector = 'td > span,tah'

    



class MarketBuyerInfoCrawler(NaverFinanceCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = self.base_url + "/sise/investorDealTrendDay.naver"

    def get_result_data(self, from_page, to_page):
        # [ {ts:INT, ant:FLOAT, inst:FLOAT, foreigner:FLOAT,.....},  {}, {}  ]
        
        total_info_list = []
        for page_idx in range(from_page, to_page+1):
            info_list = self.parse_page(page_idx)
            total_info_list += info_list

        return total_info_list

    def parse_page(self, page_idx):

        info_dict_list = []

        now = datetime.datetime.now()
        y = str(now.year)
        m = str(now.month).rjust(2,"0")
        d = str(now.day).rjust(2,"0")
        date_str = "{0}{1}{2}".format(y,m,d)
        params = {"bizdate": date_str, "page":str(page_idx)}
        res = requests.get(self.base_url, params=params)
        # 안들키고 하고 싶다면 proxy를 붙혀서 한다.
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select(
            'table.type_1 > tr'
        )

        rows = rows[3:]
        info_soup_list = [row for row in rows if str(row).find("date") >= 0]

        for info_soup in info_soup_list:
            data_view_list = info_soup.select()
            #이부분 없음..
            break

mbic = MarketBuyerInfoCrawler()
result_list = mbic.get_result_data(1,19)
mbic.save_result_date(result_list,"test.csv")
# 만약 naverDissasion 뭐시기를 한다면 위의 코드가 계속 돌아간다. 
ndc = NaverDiscussionCrawler()
result_list = ndc.get_result_data(1,3)
print(result_list)


'''
yfc = YahooFinanceCrawler()
result_list = yfc.get_result_data("GC=F", "2023/4/10", "2023/04/12")
print(result_list)

nfc = NaverFinanceCrawler()
result_list = nfc.get_result_data(1,3)
'''

