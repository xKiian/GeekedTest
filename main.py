from geeked.geeked import Geeked
from geeked.sign import Signer
from geeked.sign import LotParser
import time

# Actual: 55c86e822ef5984cc0b03a3bbfd1a7c7 - from https://auth.geetest.com/login/
challenges = {
    "ai": "99b142aaece96330d0f3ffb565ffb3ef", # Invisible
    "slide": "54088bb07d2df3c46b79f80300b0abbe",

}
while True:
    geeked = Geeked("99b142aaece96330d0f3ffb565ffb3ef", "ai")
    start = time.time()
    sec_code = geeked.solve()
    print(f"[+] Solved in {round(time.time() - start, 6)} seconds! | {sec_code['pass_token']}")
    time.sleep(1)