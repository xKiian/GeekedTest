from geeked import Geeked

captcha_id = "54088bb07d2df3c46b79f80300b0abbe"
geeked = Geeked(captcha_id, "slide", verify=False)
result = geeked.solve()
print(sec_code)
# do something with sec_code
