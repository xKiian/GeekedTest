from uuid import uuid4
from curl_cffi import requests
import random, time, json
from geeked.sign import Signer


class Geeked:
    def __init__(self, captcha_id: str, risk_type: str, **kwargs):
        self.pass_token = None
        self.lot_number = None
        self.captcha_id = captcha_id
        self.challenge = str(uuid4())
        self.risk_type = risk_type
        self.callback = Geeked.random()
        self.session = requests.Session(impersonate="chrome124", **kwargs)
        self.session.headers = {
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "script",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9"
        }
        self.session.base_url = "https://gcaptcha4.geevisit.com"

    @staticmethod
    def random() -> str:
        return f"geetest_{int(random.random() * 10000) + int(time.time() * 1000)}"

    def format_response(self, response: str) -> dict:
        # print(json.loads(response.split(f"{self.callback}(")[1][:-1]))
        return json.loads(response.split(f"{self.callback}(")[1][:-1])["data"]

    def load_captcha(self):
        params = {
            "captcha_id": self.captcha_id,
            "challenge": self.challenge,
            "client_type": "web",
            "risk_type": self.risk_type,
            "lang": "eng",
            "callback": self.callback,
        }
        res = self.session.get("/load", params=params)
        return self.format_response(res.text)

    def submit_captcha(self, data: dict) -> dict:
        self.callback = Geeked.random()

        params = {
            "callback": self.callback,
            "captcha_id": self.captcha_id,
            "client_type": "web",
            "lot_number": self.lot_number,
            "risk_type": self.risk_type,
            "payload": data["payload"],
            "process_token": data["process_token"],
            "payload_protocol": "1",
            "pt": "1",
            "w": Signer.generate_w(data, self.captcha_id, self.risk_type),
        }
        res = self.session.get("/verify", params=params).text
        res = self.format_response(res)

        if res.get("seccode") is None:
            raise Exception(f"Failed to submit captcha: {res}")

        return res["seccode"]

    def solve(self) -> dict:
        data = self.load_captcha()
        self.lot_number = data["lot_number"]
        seccode = self.submit_captcha(data)
        return seccode
