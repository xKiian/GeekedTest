import asyncio
from geeked import Geeked

captcha_id = "54088bb07d2df3c46b79f80300b0abbe"
geeked = Geeked(captcha_id, "slide", verify=False)
result = asyncio.run(geeked.solve())
print(result)
