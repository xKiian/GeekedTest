import json
import re
import urllib.parse
import uuid

import requests


def getPath() -> str:
    params = {
        "callback": "geetest_1738850809870",
        "captcha_id": "588a5218557e1eadf33d682a6958c31b",
        "challenge": str(uuid.uuid4()),
        "client_type": "web",
        "lang": "en"
    }

    res = requests.get("https://gcaptcha4.geevisit.com/load", params=params).text
    formatted = json.loads(res.split(f"{params['callback']}(")[1][:-1])

    return formatted["data"]["static_path"]


path = getPath()
print("[~] Version:", path.split("/")[3])

script = requests.get(f"https://static.geevisit.com{path}/js/gcaptcha4.js").text

# open("raw.js", "w", encoding="utf8").write(script)


def decrypt_table(table_encrypted, _key):
    key_length = len(_key)

    decrypted_chars = [chr(ord(table_encrypted[i]) ^ ord(_key[i % key_length])) for i in range(len(table_encrypted))]
    decrypted = "".join(decrypted_chars)

    return decrypted.split("^")


table_enc = urllib.parse.unquote(script.split("decodeURI(\"")[1].split("\"")[0])
key = re.findall(r"}}}\(\"(.+?)\"\)}", script)[0]

#print("[~] Key:", key)

table = decrypt_table(table_enc, key)

obfuscated_names = re.findall(r"(_.{4})\((\d+?)\)", script)

#print(f"[#] Replacing {len(obfuscated_names)} obfuscated names...\n")

for (name, index) in obfuscated_names:
    script = script.replace(f"{name}({index})", repr(table[int(index)]))

# open("deobfuscated.js", "w", encoding="utf8").write(script)


# constants that might change on a version update

abo = re.findall(r"\['_lib']=(.+?),", script)[0].replace("'", '"')
abo = re.sub(r'([{,])\s*([A-Za-z0-9_]+)\s*:', r'\1"\2":', abo)
print("[+] abo:", abo)

mappings = re.findall(r"\['_abo']=(.+?)}\(\)", script)[0]
print("[+] mappings", mappings)

device_id = re.findall(r"\['options']\['deviceId']='(.*?)'", script)[0]
print(f"[+] device_id: \"{device_id}\" (probably empty)")
