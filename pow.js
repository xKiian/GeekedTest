const crypto = require('crypto')

function sign(lotNumPow, captchaIdPow, hashType, hashVersion, bits, date, empty) {


	var _ᕵᕹᖄᖂ = bits % 4, _ᖃᕾᖗᖀ = parseInt(bits / 4, 10), _ᖃᕷᖙᖆ = function _ᕷᕶᖈᖈ(_ᖀᕵᕺᕷ, _ᖀᕾᖂᖃ) {

			return new Array(_ᖀᕾᖂᖃ + 1)['join'](_ᖀᕵᕺᕷ)
		}('0', _ᖃᕾᖗᖀ),
		pow = hashVersion + '|' + bits + '|' + hashType + '|' + date + '|' + captchaIdPow + '|' + lotNumPow + '|' + empty + '|';
	while (1) {
		var h = "305bd4e7d6279bf1", l = pow + h, p = void 0;
		switch (hashType) {
			case 'md5':
				p = crypto.createHash('md5').update(l).digest("hex")
				break;
			case 'sha1':
				p = crypto.createHash('sha1').update(l).digest("hex")
				break;
			case 'sha256':
				p = crypto.createHash('sha256').update(l).digest("hex")
		}
		if (0 == _ᕵᕹᖄᖂ) {
			if (0 === p['indexOf'](_ᖃᕷᖙᖆ)) return {pow_msg: pow + h, pow_sign: p}
		} else if (0 === p['indexOf'](_ᖃᕷᖙᖆ)) {
			var f = void 0, d = p[_ᖃᕾᖗᖀ];
			switch (_ᕵᕹᖄᖂ) {
				case 1:
					f = 7;
					break;
				case 2:
					f = 3;
					break;
				case 3:
					f = 1
			}
			if (d <= f) return {pow_msg: pow + h, pow_sign: p}
		}
	}
}

out = sign("c1d2754558e34edcad51363dedd582c1", "54088bb07d2df3c46b79f80300b0abbe", "md5", "1", 0, "2025-02-03T21:47:56.826264+08:00", "")
console.log(out)