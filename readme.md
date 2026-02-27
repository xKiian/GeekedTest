# Geetest v4 solver

<div>
    <img src="https://wakatime.com/badge/user/839267df-3912-44c6-97f4-9e3f0425b716/project/f6428644-935c-4ab9-82ab-fb782b33935a.svg" alt="wakatime">
    <br>
    <img src="assets/slide.png">
    <img src="assets/gobang.png">
    <img src="assets/icon.png">
</div>

Version: v1.9.4-4e51fe

---

# ⭐️ Show Your Support

Please star the repository if you find it useful! Your support helps improve the project. ❤️

---

## Disclaimer

This repository currently supports only **risk_type** `slide`, `gobang`, `icon` and `ai`. If the project gains enough attention,
I will
consider adding more risk types.

---

## How to Obtain the Captcha ID & Risk Type

To use this solver, you'll need to obtain the **captcha_id** and **risk_type**. Here's how you can do it:

1. **Open DevTools** in your browser (Press `Ctrl + Shift + I`).
2. Navigate to the **Network** tab.
3. **Solve the captcha** on the page.
4. Filter the network requests by searching for `verify`.
5. Find the request with the **GET** method and click on the small arrow to the left of it.
6. Look for the `captcha_id` and `risk_type` parameters in the request details and copy them.

![Captcha ID](assets/captcha_id.png)

---

## Example Usage

```python
from geeked import Geeked

# Replace with your own captcha_id
captcha_id = "54088bb07d2df3c46b79f80300b0abbe"

# Instantiate the solver with captcha_id and risk_type
geeked = Geeked(captcha_id, risk_type="slide")

# Solve the captcha
sec_code = geeked.solve()

# Output the solution
print(sec_code)
# Output will be in the following format:
# {
#    'captcha_id': '...',
#    'lot_number': '...',
#    'pass_token': '...',
#    'gen_time': '...',
#    'captcha_output': '...'
# }

```

---

## Note

There are 2 constants in `sign.py`

- self.mapping
- abo
- device_id (probably empty)

If the solver doesn't work, run `deobfuscate.py` to get the updated constants.

---

[Here](https://gt4.geetest.com/demov4/index-en.html) is a demo site from Geetest, where you can test each captcha type

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Star History

 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=xKiian/GeekedTest&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=xKiian/GeekedTest&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=xKiian/GeekedTest&type=Date" />
 </picture>

---

## Disclaimer #2

This package is **unofficial** and not affiliated with **WUHAN JIYI NETWORK TECHNOLOGY CO., LTD**. Use it responsibly
and in accordance with their terms of service.
