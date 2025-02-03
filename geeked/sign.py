from datetime import datetime
import pytz, random, hashlib


class Signer:
    @staticmethod
    def rand_uid():
        result = ''
        for _ in range(4):
            result += hex(int(65536 * (1 + random.random())))[2:].zfill(4)[-4:]
        return result

    @staticmethod
    def pow(lot_number, captcha_id) -> dict:
        current_time = datetime.now(
            # pytz.timezone("Asia/Singapore")
        )
        timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        timestamp = timestamp[:-2] + ':' + timestamp[-2:]

        return Signer.generate_pow(lot_number, captcha_id, "md5", "1", 0, timestamp, "")

    @staticmethod
    def generate_pow(lot_number_pow, captcha_id_pow, hash_type, hash_version, bits, date, empty) -> dict:
        """Generate the pow_msg & pow_sign | translated directly from the .js"""
        bit_remainder = bits % 4
        bit_division = bits // 4

        prefix = '0' * bit_division
        pow_string = f"{hash_version}|{bits}|{hash_type}|{date}|{captcha_id_pow}|{lot_number_pow}|{empty}|"

        while True:
            h = Signer.rand_uid()
            combined = pow_string + h
            hashed_value = None

            if hash_type == 'md5':
                hashed_value = hashlib.md5(combined.encode('utf-8')).hexdigest()
            elif hash_type == 'sha1':
                hashed_value = hashlib.sha1(combined.encode('utf-8')).hexdigest()
            elif hash_type == 'sha256':
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
    def generate_w(lot_number, captcha_id):
        raw = {
            **Signer.pow(lot_number, captcha_id),
            "697604": "00b921",
            "biht": "1426265548",
            "device_id": "",
            "em": {
                "cp": 0,
                "ek": "f1",
                "nt": 0,
                "ph": 0,
                "sc": 0,
                "si": 0,
                "wd": 0
            },
            "ep": "123",
            "gee_guard": {
                "roe": {
                    "auh": "3",
                    "aup": "3",
                    "cdc": "3",
                    "egp": "3",
                    "res": "3",
                    "rew": "3",
                    "sep": "3",
                    "snh": "3",
                }
            },
            "geetest": "captcha",
            "lang": "zh",
            "lot_number": lot_number,
            "passtime": 753,
            "qCzt": "VLwx",
            "setLeft": 104,
            "userresponse": 105.38520266150626
        }
