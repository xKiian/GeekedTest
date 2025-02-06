from geeked.geeked import Geeked
import time

challenges = {
    "ai": "55c86e822ef5984cc0b03a3bbfd1a7c7", # Invisible
    "slide": "54088bb07d2df3c46b79f80300b0abbe",
}


while True:
    geeked = Geeked("54088bb07d2df3c46b79f80300b0abbe", "slide")
    start = time.time()
    sec_code = geeked.solve()
    print(f"[+] Solved in {round(time.time() - start, 6)} seconds! | {sec_code['pass_token']}")
    time.sleep(3)