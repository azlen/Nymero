import re

mobypron = open('mpron/mobypron.unc', 'r')
commonwords = open('common-words.txt', 'r')

lines = mobypron.read().split('\r')

mms = {
	'b':9, #b
	'tS':6, #ch
	'd':1, #d
	'f':8, #f
	'g':7, #g
	'dZ':6, #soft g right?
	'k':7, #k
	'l':5, #l
	'm':3, #m
	'n':2, #n
	'N':2, #2, 27, or 7, ng
	'p':9, #p
	'r':4, #r
	'S':6, #sh
	's':0, #s
	'T':1, #th
	'D':1, #th in the
	't':1, #t
	'v':8, #v
	'Z':6, #s in vision
	'z':0, #z

	'R':4, #r
}

prondata = {}
commondata = {}
discards = {}

for line in lines:
	match = re.match(r'^([^ ]*) (.*)', line)
	if match:
		word = match.group(1)
		pron = match.group(2)

		pron.split('/')
		for i in pron:
			if i not in mms:
				discards[i] = True
		pron = map((lambda x: str(mms[x])), filter((lambda x: x in mms), pron)) # filter out consonants and convert to numbers
		pron = ''.join(pron)

		if (pron in prondata) == False:
			prondata[pron] = [word]
		else:
			prondata[pron].append(word)

for line in commonwords:
	match = re.match(r'(.*)\t(\d*)', line)
	if match:
		word = match.group(1).lower()
		freq = match.group(2)

		commondata[word] = int(freq)

print 'READY'
print discards

def generate_words(inp):
	out = []

	for number in inp:
		words = prondata[number]
		words = map(lambda x: x.lower(), words) # make all words lowercase
		words = filter(lambda x: x in commondata, words) # filter out words not in common words list
		words = sorted(words, key=lambda x: commondata[x]) # sort by reverse frequency
		words = map(lambda x: (x, commondata[x]), words) # tuple with frequency
		words.reverse() # flip order to frequency instead of reverse frequency
		out.append(words[0][0]) # haha, all that for nothing?

	return ' '.join(out)

while True:
	inp = raw_input()
	#print generate_words(inp)
	if inp in prondata:
		words = prondata[inp]
		words = map(lambda x: x.lower(), words) # make all words lowercase
		words = filter(lambda x: x in commondata, words) # filter out words not in common words list
		words = sorted(words, key=lambda x: commondata[x]) # sort by reverse frequency
		words = map(lambda x: (x, commondata[x]), words) # tuple with frequency
		words.reverse() # flip order to frequency instead of reverse frequency
		print words
	else:
		print 'cannot find '+inp
