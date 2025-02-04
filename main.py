from geeked.geeked import Geeked
from geeked.sign import Signer
from geeked.sign import LotParser
#Geeked("54088bb07d2df3c46b79f80300b0abbe", "slide").solve()
res = LotParser().get_dict("d4e28584909a47b3b47a2bbc5846ac51")
print(res)