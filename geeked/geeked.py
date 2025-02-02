from uuid import uuid4
from tls_client import Session
import random, time, json


class Geeked:
    def __init__(self, captcha_id: str, risk_type: str = "slide"):
        self.captcha_id = captcha_id
        self.challenge = str(uuid4())
        self.risk_type = risk_type
        self.base_url = "https://gcaptcha4.geetest.com"
        self.callback = Geeked.random()
        self.session = Session(client_identifier="chrome_120")
        self.session.headers = {
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "script",
            "referer": "https://gt4.geetest.com/demov4/slide-popup-en.html",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9"
        }

    @staticmethod
    def random() -> str:
        return f"geetest_{int(random.random() * 10000) + int(time.time() * 1000)}"

    def format_response(self, response: str) -> dict:
        return json.loads(response.split(f"{self.callback}(")[1][:-1])

    def load_captcha(self):
        url = f"{self.base_url}/load?captcha_id={self.captcha_id}&challenge={self.challenge}&client_type=web&risk_type={self.risk_type}&lang=eng&callback={self.callback}"
        res = self.session.get(url)
        return self.format_response(res.text)

    def submit_captcha(self):
        self.callback = Geeked.random()
        params = {
            "callback": self.callback,
            "captcha_id": self.captcha_id,
            "client_type": "web",
            "lot_number": "c1d2754558e34edcad51363dedd582c1",
            "risk_type": self.risk_type,
            "payload": "AgFD8gWUUuHFx-XvpP7J2XMJ2xiSXHGxBm8nyjZlqWF1wQJu01Xh-fA3W0HZF9lBtbIwu4zmxvmCx0JOP2SKpV7QSR2u-dYhR0OalZIo7XqGHpfwyDzTnhB4lA1C69zwVIUEQSjqYoaqapDRdG9ghqoDJOkZTB2v7ZA-99ZZ8Wt5zEstuCPpIt7huKU29irYUaRsjILhnVj0eXUKmrNrK8yoZPTCKfB2Wmc5LcukjVFHFM6CjSBtrrfa4UWN_d5t03tqY94i-T6tw1s7otfXDduAoYp5Bmxm0hCXer3PQwf6y2BiLsvFfa89zesXwk4mgWwkLqqquZJOgunamokYe7Xn_o1z5195nF3IlCEIqvr_gM7v-_IIBhMlP__Q9G8H2WvtEw1stKuec3FoLjoSC5Llha4IgRuBqRu_Vl9UWoVrODrlfihY80aUt3HCaWsTG6EtJ7oIu_EJm47tIEaw8mmiSI-fLPp-AqAE_tQeBlTX75Ey776Clv0H10ei9pzzuxd2rIaLDjjv_5phU71-FXwsD2fly1F0rDnrWB1GfoH8j6hN1D5FfTsmOEosqk5jRLwXXkP_DWUyv_huDbElwQVhcn6mLC4y-NaBCpClTzULjntCcatStGxbMbgFhwfKOTK6s2ukZ6yXAk4XpsRKnDGcnKX0_g12GcYM0ZFLFgra5kBF3WaG8RK_dxC2DLsiOFmH2ySgJckrqSS3tipF8rFY2nTsvAjSqZAv1HkjGEmE-5fmUKmnWEGSqvfyq9my1IsasCnYhRUP62GnHIisZ_sDjxVUGhWzqjBvgCbVXmOaEspiOi_oYASxGnov7lseEdDmUDh8rQ4INvzXHeZwI_rNzj25RlCS82ncgrVd6hvnGqMr7V3uMqNgVAikMCfSDTaNM3rUE7QLuA1FQPj-iqZX4JEQ0pUppI0iTKWW9mI=",
            "process_token": "37637ada171e609ea8e31bd43da38f4a8b7b8057d6c0e8466367928339caf2e0",
            "payload_protocol": "1",
            "pt": "1",
            "w": "0ae436dcbd105cc3f09b6e68ebada40dff329acbe7bcc30ce14b637227d10b26b866053103439fc0dd04717c6062f5f11d7dadfa8ac94dfac762ba89f31c2c47c97c8688b1e7a1983c5412dcc2f26aa02383154ca68446daae9216fea2a29157446df2b0be2447e9cb140937573727e9f242659e79660d4de4871f4e5a66bf1600ef9b30c2cebaff85bd169aff749be4fd86fd902671e78cb1a6ae7cddb4f6354b2771aabecc7061d7633985173d131ee6517910f155a749ac1c2ec320cb5b7cf2f26b910e2ffabb0c072e13296ca8a261b2f043045ec529a425e55d933fb9c4c4072aca7e3be80e572eee0049392c32ce3892879c52b37b54f6edb28f779c55bdeb7961717ca71c4ae2723b56ce0c6c43bf4127ff97e9521fa8b5d82d8f0be4b42ed259206ac406560cac9f51105a69bfb36437c04e4b3f8add4457c1034ef77d171e6e35c448b326176899e1e31e3fad5a1ec07c62e6460cb598dd7d5b998535297ae3e2b56602caa1fd3208f18989e5868ae8d8ae1b55cbb29183638c6374d50f9aa59d27e7c423b574a4cfdcbeb0fbbf910fd020c4a2feafbbb0d6cfde369f3eaf30cd9a92ee0772b49b8807b03a8adb282ffd98ad1dcc16cc03f97f994d54db812af50b6192127af4a2aeaec00bcd4bc038a50cc1192346bd9cf499f1c500e883132476457aba2d5009fd6d4e657020bb584a4046448c50b68ad9285ebb9025c51e98b89ba3c79e1a4cc03ba3670dcb7d18849de9197506ee361437abf81ec30e807619e3e0e4435ea8cc2c3c874af3b64ab630b2ab277c82b8f4e8e737b9cd9b66e3cb2140e93481265cfd6dc22fe3042d92c9b6bccad1c48b322ddb99946a9d554c5354255553bcd9301bb3c8b94892475922bf09a2ed81a160bcd0151ef3aaf634d3b8621711b0fe56b6895e72002702b40c09b178a0a9ae79bba6421884c38e93cc2ccc16f4a136658af18aa7f3a05d4c3b371f66827b9ae877ed99"
        }

    def solve(self):
        init_res = self.load_captcha()
        print(init_res)
