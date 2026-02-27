import random
import hashlib
import urllib.parse
import binascii
import json
import re
import requests

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey.RSA import construct
from Crypto.Cipher import PKCS1_v1_5
from geeked.slide import SlideSolver
from geeked.gobang import GobangSolver
from geeked.icon import IconSolver

class LotParser:
    def __init__(self):
        self.mapping = {"n[15:18]+n[1:4]":'n[17:22]'}
        self.lot = []
        self.lot_res = []
        for k, v in self.mapping.items():
            self.lot = self._parse(k)
            self.lot_res = self._parse(v)

    @staticmethod
    def _parse_slice(s):
        return [int(x) for x in s.split(':')]

    @staticmethod
    def _extract(part):
        return re.search(r'\[(.*?)\]', part).group(1)

    def _parse(self, s):
        parts = s.split('+.+')
        parsed = []
        for part in parts:
            if '+' in part:
                subs = part.split('+')
                parsed_subs = [self._parse_slice(self._extract(sub)) for sub in subs]
                parsed.append(parsed_subs)
            else:
                parsed.append([self._parse_slice(self._extract(part))])
        return parsed

    @staticmethod
    def _build_str(parsed, num):
        result = []
        for p in parsed:
            current = []
            for s in p:
                start = s[0]
                end = s[1] + 1 if len(s) > 1 else start + 1
                current.append(num[start:end])
            result.append(''.join(current))
        return '.'.join(result)

    def get_dict(self, lot_number):
        i = self._build_str(self.lot, lot_number)
        r = self._build_str(self.lot_res, lot_number)
        parts = i.split('.')
        a = {}
        current = a
        for idx, part in enumerate(parts):
            if idx == len(parts) - 1:
                current[part] = r
            else:
                current[part] = current.get(part, {})
                current = current[part]
        return a


lotParser = LotParser()  # doesn't need to calculate the lot and lot_res every time, so were gonna cache it


class Signer:
    encryptor_pubkey = construct((
        int("00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81".lower(),
            16),
        int("10001", 16))
    )

    @staticmethod
    def rand_uid():
        result = ''
        for _ in range(4):
            result += hex(int(65536 * (1 + random.random())))[2:].zfill(4)[-4:]
        return result

    @staticmethod
    def encrypt_symmetrical_1(o_text, random_str):
        key = random_str.encode('utf-8')
        iv = b'0000000000000000'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_bytes = cipher.encrypt(pad(o_text.encode('utf-8'), AES.block_size))

        return encrypted_bytes

    @staticmethod
    def encrypt_asymmetric_1(message: str) -> str:
        message_bytes = message.encode('utf-8')
        cipher = PKCS1_v1_5.new(Signer.encryptor_pubkey)
        encrypted_bytes = cipher.encrypt(message_bytes)
        encrypted_hex = binascii.hexlify(encrypted_bytes).decode('utf-8')

        return encrypted_hex

    """ ill implement it when needed
function encrypt_asymmetric_2(input, key) {
	void 0 === key && (key = '9a4ea935b2576f37516d9b29cd8d8cc9bffe548ba6853253ba20f4ba44fba8c9e97a398882769aa0dd1e3e1b5601429287303880ca17bd244ed73bf702a68fc7');
	var moreargs = 2 < arguments['length'] && arguments[2] !== undefined ? arguments[2] : 1;
	var encryptor = new _ᖉᖉᕾᖉ;

	input = sortaGlobals['hexToArray'](sortaGlobals['parseUtf8StringToHex'](input)), 128 < key['length'] && (key = key['substr'](key['length'] - 128));
	var keyLeft = key['substr'](0, 64), keyRest = key['substr'](64);
	key = encryptor['createPoint'](keyLeft, keyRest);
	var initCypher = encryptor['initEncipher'](key);
	encryptor['encryptBlock'](input);
	var end = sortaGlobals['arrayToHex'](input);
	emptyArray = new Array(32);
	return encryptor['doFinal'](emptyArray), emptyArray = sortaGlobals['arrayToHex'](emptyArray), 0 === moreargs ? initCypher + end + emptyArray : initCypher + emptyArray + end
}
    """

    @staticmethod
    def encrypt_w(raw_input, pt) -> str:
        if not pt or '0' == pt:
            return urllib.parse.quote_plus(raw_input)

        random_uid = Signer.rand_uid()
        enc_key: str
        enc_input: bytes

        if pt == "1":
            enc_key = Signer.encrypt_asymmetric_1(random_uid)
            enc_input = Signer.encrypt_symmetrical_1(raw_input, random_uid)
        else:  # elif pt == "2" # there's either "1" or "2"
            raise NotImplementedError("This type of encryption is not implemented yet. Create an issue")

        return binascii.hexlify(enc_input).decode() + enc_key

    @staticmethod
    def generate_pow(lot_number_pow, captcha_id_pow, hash_func, hash_version, bits, date, empty) -> dict:
        """Generate the pow_msg & pow_sign | translated directly from the .js"""
        bit_remainder = bits % 4
        bit_division = bits // 4

        prefix = '0' * bit_division
        pow_string = f"{hash_version}|{bits}|{hash_func}|{date}|{captcha_id_pow}|{lot_number_pow}|{empty}|"

        while True:
            h = Signer.rand_uid()
            combined = pow_string + h
            hashed_value = None

            if hash_func == 'md5':
                hashed_value = hashlib.md5(combined.encode('utf-8')).hexdigest()
            elif hash_func == 'sha1':
                hashed_value = hashlib.sha1(combined.encode('utf-8')).hexdigest()
            elif hash_func == 'sha256':
                hashed_value = hashlib.sha256(combined.encode('utf-8')).hexdigest()

            if bit_remainder == 0:
                if hashed_value.startswith(prefix):
                    return {'pow_msg': pow_string + h, 'pow_sign': hashed_value}
            else:
                if hashed_value.startswith(prefix):
                    length = len(prefix)
                    threshold = None
                    if bit_remainder == 1:
                        threshold = 7
                    elif bit_remainder == 2:
                        threshold = 3
                    elif bit_remainder == 3:
                        threshold = 1

                    if length <= threshold:
                        return {'pow_msg': pow_string + h, 'pow_sign': hashed_value}

    @staticmethod
    def generate_w(data: dict, captcha_id: str, risk_type: str):
        lot_number = data['lot_number']
        pow_detail = data['pow_detail']
        abo = {"S59M":"rwPC"}
        base = abo | {
            **Signer.generate_pow(lot_number, captcha_id, pow_detail['hashfunc'], pow_detail['version'],
                                  pow_detail['bits'], pow_detail['datetime'], ""),
            **lotParser.get_dict(lot_number),
            "biht": "1426265548",  # static
            "device_id": "",  # why is this empty!!
            "em": {  # save to have this static (see em.js)
                "cp": 0,  # checkCallPhantom
                "ek": "11",  # checkErrorKeys "11" as value is also fine
                "nt": 0,  # checkNightmare
                "ph": 0,  # checkPhantom
                "sc": 0,  # checkSeleniumMarker
                "si": 0,  # checkScriptFn
                "wd": 1,  # checkWebDriver
            },
            "gee_guard": {
                "roe": {  # "3" = no | "1" = yes
                    "auh": "3",  # HEADCHR_UA            | regex(/HeadlessChrome/) in UserAgent
                    "aup": "3",  # PHANTOM_UA            | regex(/PhantomJS/) in UserAgent
                    "cdc": "3",  # CDC                   | cdc check
                    "egp": "3",  # PHANTOM_LANGUAGE      | language header !== undefined
                    "res": "3",  # SELENIUM_DRIVER       | 35 selenium checks 💀
                    "rew": "3",  # WEBDRIVER             | webDriver check
                    "sep": "3",  # PHANTOM_PROPERTIES    | phantomJS check
                    "snh": "3",  # HEADCHR_PERMISSIONS   | checks browser version etc.
                }
            },
            "ep": "123",  # static
            "geetest": "captcha",  # static
            "lang": "zh",  # static
            "lot_number": lot_number,
        }

        if risk_type in ("ai", "invisible"):
            pass
        elif risk_type == "slide":
            left = SlideSolver(
                requests.get(f"https://static.geetest.com/{data['slice']}", timeout=10).content,
                requests.get(f"https://static.geetest.com/{data['bg']}", timeout=10).content
            ).find_puzzle_piece_position() + random.uniform(0, .5)
            base |= {
                "passtime": random.randint(600, 1200),  # time in ms it took to solve
                "setLeft": left,
                "userresponse": left / 1.0059466666666665 + 2  # 1.0059466666666665 = .8876 * 340 / 300
            }
        elif risk_type in ("winlinze", "gobang"):
            base |= {
                "userresponse": GobangSolver(data["ques"]).find_four_in_line()
            }
        elif risk_type in 'icon':
            base |= {
                "passtime": random.randint(600, 1200),  # time in ms it took to solve
                "userresponse": IconSolver(data["imgs"], data["ques"]).find_icon_position()
            }
        else:
            raise NotImplementedError(f"This type ({risk_type}) of captcha is not implemented yet.")

        return Signer.encrypt_w(json.dumps(base), data["pt"])
