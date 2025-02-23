from geeked import Geeked

challenges = {
    "ai": "55c86e822ef5984cc0b03a3bbfd1a7c7", # Invisible
    "slide": "54088bb07d2df3c46b79f80300b0abbe",
}

geeked = Geeked("588a5218557e1eadf33d682a6958c31b", "slide")
sec_code = geeked.solve()
print(sec_code)
# do something with sec_code
