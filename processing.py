import csv
import json
from mapping import mapping as MAPPING

MAX_NAME_LENGTH = 10
PADDING = 'Q'
with open('grams.json') as data:
	GRAMS = json.load(data)

def process(filename):
	first_names = []
	last_names = []
	sources = []
	with open(filename, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			first = convert_to_numerical(get_3grams(row[0]))
			#print(first)
			first_names += [first]
			last_names += [row[1]]
			source = row[2]
			sources += [source]
	new_filename = filename[:-4] + '_processed.csv'
	with open(new_filename, 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
		for i in range(0, len(first_names)):
			csvwriter.writerow([first_names[i],last_names[i], sources[i]])
	print('done')

def get_3grams(name):
	""" Get 3-grams of names 
	"""
	name = name[2:-1]
	if len(name) < MAX_NAME_LENGTH:
		grams = [name[i:i+3] for i in range(0, len(name) - 2)]

		# Padding names that are shorter than average
		overflow = MAX_NAME_LENGTH - len(name)
		if overflow > 0:
			grams += [name[len(name) - 2:] + PADDING]
		if overflow > 1:
			grams += [name[-1:] + PADDING*2]
		if overflow > 2:
			for i in range(len(name), MAX_NAME_LENGTH):
				grams += [PADDING*3]
		return grams
	
	else:
		# truncating names that are longer than average
		return [name[i:i+3] for i in range(0, len(name) - 2)]

def convert_to_numerical(grams):
	print(grams)
	result = []
	for gram in grams:
		try:
			result += [int(GRAMS[gram])]
		except KeyError:
			converted_gram = []
			for letter in gram:
				
				if letter.encode('utf-8') == b"'"  : continue
				
				converted_gram += [(MAPPING[letter.encode('utf-8')])]
				
			num_val = '0'.join([str(c) for c in converted_gram])
			result += [int(num_val)]

			# Saving grams to dictionary
			GRAMS[gram] = num_val
	return result

process('data/training.csv')