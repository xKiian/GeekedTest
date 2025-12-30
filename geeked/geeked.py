import json
import random
import time
from uuid import uuid4

from curl_cffi import requests

from .sign import Signer


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
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "accept": "*/*",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-dest": "script",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
        }
        self.session.base_url = "https://gcaptcha4.geevisit.com"

    @staticmethod
    def random() -> str:
        return f"geetest_{int(random.random() * 10000) + int(time.time() * 1000)}"

    def format_response(self, response: str) -> dict:
        parsed = json.loads(response.split(f"{self.callback}(")[1][:-1])
        return parsed.get("data", parsed)

    def load_captcha(self, payload=None, process_token=None):
        params = {
            "captcha_id": self.captcha_id,
            "challenge": self.challenge,
            "client_type": "web",
            "risk_type": self.risk_type,
            "lang": "eng",
            "callback": self.callback,
        }

        if payload:
            params["payload"] = payload
            params["process_token"] = process_token
            params["lot_number"] = self.lot_number
            params["pt"] = "1"
            params["payload_protocol"] = "1"

        res = self.session.get("/load", params=params)
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
            "w": Signer.generate_w(data, self.captcha_id, data["captcha_type"]),
        }
        res = self.session.get("/verify", params=params).text

        return res

    def initial_verify(self, data: dict, dummy_w: str) -> dict:
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
            "w": dummy_w,
        }

        res = self.session.get("/verify", params=params).text
        res = self.format_response(res)

        if res.get("result") != "fail":
            raise Exception(f"Expected initial verify to fail, got: {res}")

        return res

    def solve(self) -> str:
        initial_data = self.load_captcha()
        self.lot_number = initial_data["lot_number"]

        dummy_w = Signer.generate_dummy_w(initial_data, self.captcha_id)
        failed_data = self.initial_verify(initial_data, dummy_w)

        reload_data = self.load_captcha(payload=failed_data["payload"], process_token=failed_data["process_token"])

        seccode = self.submit_captcha(reload_data)
        return seccode

    def solve_from_load_data(self, load_data: str) -> str:
        # Parse JSONP with any callback name (browser may use different callback)
        match = json.loads(load_data.split("(", 1)[1].rsplit(")", 1)[0])
        parsed_load_data = match["data"]

        self.lot_number = parsed_load_data["lot_number"]

        dummy_w = Signer.generate_dummy_w(parsed_load_data, self.captcha_id)

        # Try initial verify - might succeed or fail
        self.callback = Geeked.random()
        params = {
            "callback": self.callback,
            "captcha_id": self.captcha_id,
            "client_type": "web",
            "lot_number": self.lot_number,
            "risk_type": self.risk_type,
            "payload": parsed_load_data["payload"],
            "process_token": parsed_load_data["process_token"],
            "payload_protocol": "1",
            "pt": "1",
            "w": dummy_w,
        }

        res = self.session.get("/verify", params=params).text
        verify_response = self.format_response(res)

        # If succeeded on first try, return immediately
        if verify_response.get("result") == "success":
            return res

        # If failed, continue with reload
        reload_data = self.load_captcha(
            payload=verify_response["payload"], process_token=verify_response["process_token"]
        )

        seccode = self.submit_captcha(reload_data)
        return seccode
