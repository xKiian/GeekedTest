// i didnt fully reverse this, i just started pasting the py code directly
function _ᖃᕾᖗᖀ() {
	this['n'] = null;
	this['e'] = 0;
	this['d'] = null;
	this['p'] = null;
	this['q'] = null;
	this['dmp1'] = null;
	this['dmq1'] = null;
	this['coeff'] = null;
	this['setPublic'](
		'00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81',
		'10001'
	);
}

function parse(_ᕷᕶᖈᖈ) {

	for (var t = _ᕷᕶᖈᖈ['length'], s = [], n = 0; n < t; n++) s[n >>> 2] |= (255 & _ᕷᕶᖈᖈ['charCodeAt'](n)) << 24 - n % 4 * 8;
	return new (_ᖃᕾᕴᖗ['init'])(s, t)
}

function encrypt_symmetrical1(inputStr, _ᖀᕾᖂᖃ, _ᖆᕾᖁᖁ) {

	_ᖀᕾᖂᖃ = _ᖈᕶᖚᕿ['parse'](_ᖀᕾᖂᖃ), _ᖆᕾᖁᖁ && _ᖆᕾᖁᖁ['iv'] || ((_ᖆᕾᖁᖁ = _ᖆᕾᖁᖁ || {})['iv'] = _ᖈᕶᖚᕿ['parse']('0000000000000000'));
	for (var n = v['encrypt'](_ᕷᕶᖈᖈ, inputStr, _ᖀᕾᖂᖃ, _ᖆᕾᖁᖁ), i = n['ciphertext']['words'], r = n['ciphertext']['sigBytes'], o = [], a = 0; a < r; a++) {
		var _ = i[a >>> 2] >>> 24 - a % 4 * 8 & 255;
		o['push'](_)
	}
	return o
}

function enc(raw_input, pt) {

	if (!pt || '0' === pt) return _ᖁᖃᕺᕵ['default']['urlsafe_encode'](raw_input);

	var random_uid = "56e508d726649e0d"//(0, _ᖈᖁᖃᕿ['guid'])();

	funcs = {
		1: {
			symmetrical: encrypt_symmetrical,
			asymmetric: _ᖃᕾᖗᖀ
		},
		2: {
			symmetrical: new (_ᕷᕹᖚᖀ['default'])({key: random_uid, mode: 'cbc', iv: '0000000000000000'}),
			asymmetric: _ᖂᖉᖙᕷ['default']
		}
	};

	if (["1", "2"].includes(pt)) {
		if (pt === "1") {
			_ = asymmetric(random_uid);

			while (!_ || 256 !== _['length']) {
				random_uid = (0, _ᖈᖁᖃᕿ['guid'])();
				_ = (new (_ᖉᖉᕾᖉ['default']))['encrypt'](random_uid)
			}

			var u = encrypt_symmetrical1(raw_input, random_uid);
		} else {
			_ = funcs[pt]['asymmetric']['encrypt'](random_uid);

			var u = funcs[pt]['symmetrical'](raw_input, random_uid);
		}
		return (0, _ᖈᖁᖃᕿ['arrayToHex'])(u) + _
	}
}


encrypt_symmetrical("56e508d726649e0d", "Hello world!")
/*
enc(
	'{"setLeft":12,"passtime":127,"userresponse":13.929061845558413,"device_id":"","lot_number":"f4744c44df4541b3be48c5c270ced20b","pow_msg":"1|0|md5|2025-02-04T21:27:31.059838+08:00|54088bb07d2df3c46b79f80300b0abbe|f4744c44df4541b3be48c5c270ced20b||613f457c4ace81bf","pow_sign":"c8824ed8c8bb4a1dffe516548d1c75fc","geetest":"captcha","lang":"zh","ep":"123","biht":"1426265548","gee_guard":{"roe":{"aup":"3","sep":"3","egp":"3","auh":"3","rew":"3","snh":"3","res":"3","cdc":"3"}},"qCzt":"VLwx","0ce4c4":"b3be48","em":{"ph":0,"cp":0,"ek":"f1","wd":1,"nt":0,"si":0,"sc":0}}', "1"
)*/
