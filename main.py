from geeked import Geeked

challenges = {
    "ai": "55c86e822ef5984cc0b03a3bbfd1a7c7", # Invisible
    "slide": "54088bb07d2df3c46b79f80300b0abbe",
}
proxy = "http://127.0.0.1:8050"
geeked = Geeked("6ba6b71b4f3958a1c69ad839ba47836b", "slide", proxy=proxy, verify=False)
sec_code = geeked.solve()
print(sec_code)
# do something with sec_code
