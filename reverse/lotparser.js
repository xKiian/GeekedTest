str = {"n[25:27]+n[4:6]": 'n[14:19]'}

function s(r) {
	return r.split(':').map(function (r) {
		return parseInt(r.trim(), 10)
	});
}

function parseLotString(f) {
	return f.split('+.+').map(function (_ᕷᕶᖈᖈ) {
		return -1 !== _ᕷᕶᖈᖈ.indexOf('+') ? function _ᕷᕶᖈᖈ(random2me) {
			return random2me.split('+').map(function (_ᕷᕶᖈᖈ) {
				return s(_ᕷᕶᖈᖈ.match(/\[(.*?)\]/)[1])
			})
		}(_ᕷᕶᖈᖈ) : [s(_ᕷᕶᖈᖈ.match(/\[(.*?)\]/)[1])]
	})
}


//lot is technically static

function getStringByIndexes(lot, lotNumber) {
	return lot.map(function (loti) {
		return loti.map(function (lotj) {
			var first = lotj[0];
			var odl = 1 < lotj.length ? lotj[1] + 1 : lotj[0] + 1;

			return lotNumber.slice(first, odl)
		}).join('')
	}).join('.')
}

for (var i in str) if (str['hasOwnProperty'](i)) {
	lot = parseLotString(i);
	lotRes = parseLotString(str[i])
}
console.log(lot, lotRes)
var i = getStringByIndexes(lot, "d4e28584909a47b3b47a2bbc5846ac51")
var r = getStringByIndexes(lotRes, "d4e28584909a47b3b47a2bbc5846ac51")
console.log(i, r)
var o = i['split']('.');
var a = {};
o['reduce'](function (_ᕷᕶᖈᖈ, _ᖀᕵᕺᕷ, _ᖀᕾᖂᖃ) {
	return _ᖀᕾᖂᖃ === o['length'] - 1 ? _ᕷᕶᖈᖈ[_ᖀᕵᕺᕷ] = r : _ᕷᕶᖈᖈ[_ᖀᕵᕺᕷ] || (_ᕷᕶᖈᖈ[_ᖀᕵᕺᕷ] = {}), _ᕷᕶᖈᖈ[_ᖀᕵᕺᕷ]
}, a)
console.log(a)