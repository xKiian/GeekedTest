from uuid import uuid4
from tls_client import Session
import random, time, json
from geeked.sign import Signer


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

    def submit_captcha(self, init_response: dict) -> str:
        self.callback = Geeked.random()
        data = init_response["data"]
        params = {
            "callback": self.callback,
            "captcha_id": self.captcha_id,
            "client_type": "web",
            "lot_number": data["lot_number"],
            "risk_type": self.risk_type,
            "payload": data["payload"],
            "process_token": data["process_token"],
            "payload_protocol": "1",
            "pt": "1",
            "w": Signer.generate_w(data, self.captcha_id),
        }

    def solve(self):
        init_res = self.load_captcha()
        self.submit_captcha(init_res)
