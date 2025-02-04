import random, hashlib, urllib.parse, binascii, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey.RSA import construct
from Crypto.Cipher import PKCS1_v1_5


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

    """
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
        else: #there's either "1" or "2" but pycharm won't stop giving me a warning 🤷
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
    def generate_w(data: dict, captcha_id: str):
        lot_number = data['lot_number']
        pow_detail = data['pow_detail']

        return Signer.encrypt_w(json.dumps({
            **Signer.generate_pow(lot_number, captcha_id, pow_detail['hashfunc'], pow_detail['version'],
                                  pow_detail['bits'], pow_detail['datetime'], ""),
            "697604": "00b921",
            "biht": "1426265548",
            "device_id": "",  # why is this empty!!
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
        }), data["pt"])
