from geeked import Geeked

challenges = {
    "ai": "55c86e822ef5984cc0b03a3bbfd1a7c7", # Invisible
    "slide": "54088bb07d2df3c46b79f80300b0abbe",
}

geeked = Geeked("54088bb07d2df3c46b79f80300b0abbe", "slide")
sec_code = geeked.solve()
print(sec_code)
# do something with sec_code
