var corpi = {
	'common' : {}, // words based on frequency
	'pron' : {}, // pronounciations
	'pos' : {} // part of speech, not being used yet
}

require(['text.js', 'json.js'], function() {
	require(['json!./common.json', 'json!./pron.json'/*, 'json!./pos.json'*/], function(a, b, c) {
		corpi.common = a;
		corpi.pron = b;
		corpi.pos = c;
	})
})

var mms = {
	'B': 9,
	'CH': 6,
	'D': 1,
	'DH': 1,
	'F': 8,
	'G': 7,
	'JH': 6,
	'K': 7,
	'L': 5,
	'M': 3,
	'N': 2,
	'NG': 2, // 2, 27, or 7?
	'P': 9,
	'R': 4,
	'S': 0,
	'SH': 6,
	'T': 1,
	'TH': 1,
	'V': 8,
	'Z': 0,
	'ZH': 6,
	'ER': 4,
}

function getcommon(nstr) {
	var words = corpi['pron'][nstr];
	words = words.filter(function(x) {
		return x in corpi['common'];
	});
	words = words.sort(function(a, b) { // sort by frequency
		return corpi['common'][b] - corpi['common'][a];
	});
	return words;
}

function possibilities(nstr) {
	var arr = [];
	for(i = 0; i < nstr.length; i++) {
		var pron = nstr.substr(0, i+1);
		if(pron in corpi['pron']) {
			arr.push(pron.slice());
		}
	}
	arr.reverse();
	narr = arr.map(getcommon);
	for(i = 0; i < narr.length; i++) {
		if(narr[i].length > 0 && corpi['common'][narr[i][0]] > 1000000) {
			var word = narr[i][0];
			return [word, nstr.substr(arr[i].length)];
		}
	}
}

function memms(nstr) {
	nstr = nstr.replace(/[^\d]/g, ''); // remove non-digits
	var out = [];
	while(nstr.length != 0) {
		var temp = possibilities(nstr);
		out.push(temp[0]);
		nstr = temp[1];
	}
	return out.join(' ');
}
