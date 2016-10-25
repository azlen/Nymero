import re

#pron = open('./mpron/mobypron.unc', 'r')
pronfile = open('cmudict-0.7b.txt', 'r')
commonwordsfile = open('common-words.txt', 'r')
posfile = open('mpos/mobypos.i', 'r')

mms = {
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
	'NG': 2, #2, 27, or 7?
	'P': 9,
	'R': 4,
	'S': 0,
	'SH': 6,
	'T': 1,
	'TH': 1,
	'V': 8,
	'Z': 0,
	'ZH': 6,
}

corpi = {
	'pron': {},
	'common': {},
	'pos': {},
	'final': {}
}

for line in pronfile.readlines():
	match = re.match(r'([^ ]+) (.+)', line)
	if match:
		word = match.group(1)
		pron = match.group(2)

		word = word.lower()

		pron = re.sub(r'[^[a-zA-Z ]]*', '', pron) # remove stress numbers
		pron = pron.split(' ') # split pronouciation into phonemes
		pron = filter(lambda x: x in mms, pron) # filter out vowels
		pron = map(lambda x: mms[x], pron) # convert consonants to numbers
		pron = map(str, pron) # convert numbers to strings so that we can join them together
		pron = ''.join(pron) # create string of numbers representing word

		if pron in corpi['pron']:
			corpi['pron'][pron].append(word)
		else:
			corpi['pron'][pron] = [word]

for line in commonwordsfile.readlines():
	match = re.match(r'([^\t]+)\t(\d+)', line)
	if match:
		word = match.group(1)
		count = match.group(2)

		word = word.lower()
		count = int(count)

		corpi['common'][word] = count

for line in posfile.readlines():
	match = re.match(r'(.*)◊(.*)')
	if match:
		word = match.group(1)
		pos = match.group(2)

		word = word.lower()
		#pos =
		corpi['pos'][word] = pos


print 'READY'

def getcommon(nstr):
	words = corpi['pron'][nstr]
	words = filter(lambda x: x in corpi['common'], words) # only include words in both common and pron corpi
	words = sorted(words, key=lambda x: corpi['common'][x]) # sort words in reverse frequency order
	words.reverse() # reverse order so that higher frequency appears first
	return words

def possibilities(nstr):
	arr = []
	for i in range(len(nstr)):
		pron = nstr[0:i+1]
		if pron in corpi['pron']:
			arr.append(pron[:])
	arr.reverse()
	narr = map(getcommon, arr)
	for i in range(len(narr)):
		if len(narr[i]) > 0 and corpi['common'][narr[i][0]] > 1000000:
			word = narr[i][0]
			return (word, nstr[len(arr[i]):])
	print "SOMETHING WENT WRONG", arr, narr, nstr
	return ('','')

def memms(nstr):
	out = []
	while len(nstr) != 0:
		temp = possibilities(nstr)
		out.append(temp[0])
		nstr = temp[1]
	return ' '.join(out)

while True:
	inp = raw_input()
	inp = re.sub(r'[^\d]*', '', inp)
	print memms(inp)
