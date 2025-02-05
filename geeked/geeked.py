from uuid import uuid4
from tls_client import Session
import random, time, json
from geeked.sign import Signer


class Geeked:
    def __init__(self, captcha_id: str, risk_type: str):
        self.pass_token = None
        self.lot_number = None
        self.captcha_id = captcha_id
        self.challenge = str(uuid4())
        self.risk_type = risk_type
        self.base_url = "https://gcaptcha4.geetest.com"
        self.callback = Geeked.random()
        self.session = Session(client_identifier="chrome_120")
        self.session.headers = {
            "connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "user-agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "script",
            #"referer": "https://gt4.geetest.com/demov4/slide-popup-en.html",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9"
        }

    @staticmethod
    def random() -> str:
        return f"geetest_{int(random.random() * 10000) + int(time.time() * 1000)}"

    def format_response(self, response: str) -> dict:
        print(json.loads(response.split(f"{self.callback}(")[1][:-1]))
        return json.loads(response.split(f"{self.callback}(")[1][:-1])["data"]

    def load_captcha(self):
        url = f"{self.base_url}/load?captcha_id={self.captcha_id}&challenge={self.challenge}&client_type=web&risk_type={self.risk_type}&lang=eng&callback={self.callback}"
        res = self.session.get(url)
        return self.format_response(res.text)

    def submit_captcha(self, data: dict) -> str:
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
            "w": Signer.generate_w(data, self.captcha_id),
        }
        res = self.session.get(f"{self.base_url}/verify", params=params).text
        res = self.format_response(res)
        return res["seccode"]

    def verify(self, data: dict):
        params = {
            "captcha_id": self.captcha_id,
            "lot_number": self.lot_number,
            "pass_token": data["pass_token"],
            "gen_time": data["gen_time"],
            "captcha_output": data["captcha_output"],
        }
        res = self.session.get("https://gt4.geetest.com/demov4/demo/login", params=params).json()
        if res["result"] == "success":
            print(f"[+] Solved! lotNumber: {self.lot_number} | passToken: {data['pass_token']}")

    def solve(self):
        data = self.load_captcha()
        self.lot_number = data["lot_number"]
        seccode = self.submit_captcha(data)
        self.verify(seccode)