import urllib.parse, re

encoded_string = urllib.parse.unquote(open("table").read())


def decrypt_table():
    key = "MKsKRB"
    key_length = len(key)

    decrypted_chars = [chr(ord(encoded_string[i]) ^ ord(key[i % key_length])) for i in range(len(encoded_string))]
    decrypted = "".join(decrypted_chars)

    return decrypted.split("^")

decrypted_values = decrypt_table()

def get_decrypted_value(list_index):
    return decrypted_values[list_index]

script = open("./rev2.js", encoding="utf8").read()

obfuscated_names = re.findall(r"(_.{4})\((\d+?)\)", script)

print(len(obfuscated_names))

for (name, index) in obfuscated_names:
    #print(index)
    #print(get_decrypted_value(int(index)))
    script = script.replace(f"{name}({index})", repr(get_decrypted_value(int(index))))

open("rev2.js", "w", encoding="utf8").write(script)