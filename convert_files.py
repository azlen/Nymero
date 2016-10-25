#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re

pronfile = open('cmudict-0.7b.txt', 'r')
commonwordsfile = open('common-words.txt', 'r')
posfile = open('mpos/mobyposi.i', 'r')

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
	'ER': 4,
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
	match = re.match(r'(.*)◊(.*)', line)
	if match:
		word = match.group(1)
		pos = match.group(2)

		word = word.lower()
		#pos =
		corpi['pos'][word] = pos



with open('pron.json', 'w') as fp:
	json.dump(corpi['pron'], fp)

with open('common.json', 'w') as fp:
	json.dump(corpi['common'], fp)

with open('pos.json', 'w') as fp:
	json.dump(corpi['pos'], fp)
