from geeked.geeked import Geeked
from geeked.sign import Signer
from geeked.sign import LotParser

challenges = {
    "ai": "99b142aaece96330d0f3ffb565ffb3ef", # Invisible
    "slide": "54088bb07d2df3c46b79f80300b0abbe",
    "": "6370a348ba8bddd565b19cb9aea370de",

}

while True:
    Geeked("54088bb07d2df3c46b79f80300b0abbe", "slide").solve()
# res = LotParser().get_dict("d4e28584909a47b3b47a2bbc5846ac51")
