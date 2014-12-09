# 50.007 ML
# Li Hanwei
# Wang Tianchi
# Wang Yingbei

# import libs
import os
import sys
import math
import copy
import json

TAGS = ['~', '@', 'O', 'V', '^', ',', '$', 'R', 'A', '!', 'P', 'T', 'N', '&', 'D', '#', 'G', 'U', 'L', 'E', 'X', 'Z', 'S', 'M', 'Y']
TAGS_INDEX = {'!': 9, '#': 15, '$': 6, '&': 13, ',': 5, 'A': 8, '@': 1, 'E': 19, 'D': 14, 'G': 16, 'M': 23, 'L': 18, 'O': 2, 'N': 12, 'P': 10, 'S': 22, 'R': 7, 'U': 17, 'T': 11, 'V': 3, 'Y': 24, 'X': 20, 'Z': 21, '^': 4, '~': 0}
TRANS_PARAM = []
TRANS_PARAM_SS = []
EMISS_PARAM = {}

PENALTY = -99999

def log(i):
	if i == 0:
		# return - sys.maxint - 1
		return PENALTY
	else:
		return math.log(i)

class HMM:
	def __init__(self):
		self.words = []
		self.tags = []

	def add_to_words(self, word):
		self.words.append(word)

	def add_to_tags(self, tag):
		self.tags.append(tag)

	def get_size(self):
		return len(self.tags)

	def count_y(self, y):
		if y == "start" or y == "end":
			return 1
		temp = 0
		# print "here"
		for i in self.tags:
			if i == y:
				temp += 1
		return temp

	def count_tran(self, y = "start", yp = "end"):
		temp = 0
		if y == "start":
			return 1 if self.tags[0] == yp else 0

		if yp == "end":
			return 1 if self.tags[-1] == y else 0
			
		for i in range(0, self.get_size() - 1):
			if self.tags[i] == y:
				if self.tags[i + 1] == yp:
					temp += 1
		return temp

	def count_emis(self, y, x):
		temp = 0
		for i in range(0, self.get_size()):
			if self.tags[i] == y:
				if self.words[i] == x:
					# print self.words[i]
					temp += 1
		return temp

	def tag_exist(self, y):
		return y in self.tags

	def is_word_not_exist(self, x):
		return x not in self.words

	def getwords(self):
		return self.words

	def gettags(self):
		return self.tags

	def set_tags(self, t):
		self.tags = t

	def write_to_file(self, f):
		for i in range(0, self.get_size()):
			f.write(self.words[i] + "\t" + self.tags[i] + "\n")
		f.write("\n")

	def get_unique_words(self):
		result = []
		for i in self.words:
			if i not in result:
				result.append(i)
		return result

	def get_accuracy_count(self, hmm):
		correct = 0
		for i in range(self.get_size()):
			if self.tags[i] == hmm.gettags()[i]:
				correct += 1
		return correct, self.get_size()

	def viterbi(self):
		# forward
		# start point
		result = []
		steps = []
		temp = []
		for i in TAGS:
			temp.append(log(TRANS_PARAM_SS[TAGS_INDEX[i]][0]) + log(EMISS_PARAM[self.words[0]][i]))
		result.append(temp)
		for i in self.words[1:]:
			temp = []
			for j in TAGS:
				maximum = - sys.maxint - 1
				previous = result[-1]
				for k in range(0, len(previous)):
					pi = previous[k] + log(TRANS_PARAM[k][TAGS_INDEX[j]]) + log(EMISS_PARAM[i][j])
					if pi > maximum:
						maximum = pi
				temp.append(maximum)
			result.append(temp)
		maximum = - sys.maxint - 1
		temptag = "V"
		for i in range(0, len(result[-1])):
			pi = result[-1][i] + log(TRANS_PARAM_SS[i][1])
			if pi > maximum:
				maximum = pi
				temptag = TAGS[i]
		steps.append(temptag)
		## maximum is the final largest pi
		## backward
		## final case
		# print result
		for i in range(1, len(self.words)):
			currentword = self.words[-i]
			maximum = - sys.maxint - 1
			previoustag = steps[-1]
			temptag = "V"
			# print currentword
			# print previoustag
			for j in TAGS:
				# print "t:" + j
				pi = result[-i-1][TAGS_INDEX[j]] + log(TRANS_PARAM[TAGS_INDEX[j]][TAGS_INDEX[previoustag]]) + log(EMISS_PARAM[currentword][previoustag])
				if pi > maximum:
					maximum = pi
					temptag = j
			steps.append(temptag)
		steps_inverse = [i for i in reversed(steps)]
		self.tags = copy.deepcopy(steps_inverse)

	# def pre_word_process(self):
	# 	for i in range(0, self.get_size()):
	# 		self.words[i] = self.words[i].lower()

	def post_tag_process(self):
		for i in range(0, self.get_size()):
			k = self.words[i]
			if k[0] == "@":
				self.tags[i] = "@"
			elif k[0] == "#":
				self.tags[i] = "#"
			elif k[:4] == "http":
				self.tags[i] = "U"
			elif k[0].isdigit():
				self.tags[i] = "$"

class SETS:
	def __init__(self):
		self.hmmset = []

	def add(self, input):
		self.hmmset.append(input)

	def overall_count_y(self, y):
		temp = 0
		# print len(self.hmmset)
		for i in self.hmmset:
			# print i.get_size()
			temp += i.count_y(y)
		return temp

	def overall_count_y_to_x(self, y, x):
		temp = 0
		if self.is_new_word(x):
			return 1
		for i in self.hmmset:
			temp += i.count_emis(y, x)
		return temp

	def estimate_emission_param(self, y, x, no_new_word):
		# return self.overall_count_y(y)
		# print self.overall_count_y_to_x(y, x)
		return self.overall_count_y_to_x(y, x)/float(self.overall_count_y(y) + no_new_word)

	def size(self):
		return len(self.hmmset)

	# def getfirst(self):
	# 	return self.hmmset[1].getwords()

	def is_new_word(self, x):
		result = True
		for i in self.hmmset:
			result = result and i.is_word_not_exist(x)
		return result

	def pos_tagger(self, x, no_new_word = 1):
		maximum = 0
		y = ""
		# d = {}
		for i in TAGS:
			# temp = self.estimate_emission_param(i, x, no_new_word)
			if x not in EMISS_PARAM.keys():
				y = "G"
			else:
				temp = EMISS_PARAM[x][i]
				# d[i] = temp
				if temp > maximum:
					maximum = temp
					y = i
		# EMISS_PARAM[x] = d
		return y

	def calculate_emis(self, word_list):
		for i in word_list:
			d = {}
			for j in TAGS:
				no_new_word = len(word_list)
				d[j] = self.estimate_emission_param(j, i, no_new_word)
			EMISS_PARAM[i] = d

	def get_hmmset(self):
		return self.hmmset

	def get_accuracy(self, sets):
		correct = 0
		total = 0
		for i in range(0, len(self.hmmset)):
			temp1, temp2 = self.hmmset[i].get_accuracy_count(sets.get_hmmset()[i])
			correct += temp1
			total += temp2
		return correct/float(total)

	def getwords(self):
		result = []
		for i in self.hmmset:
			for j in i.getwords():
				if j not in result:
					result.append(j)
		return result

	def trans_y_to_yp(self, y, yp):
		temp1 = 0
		temp2 = 0
		for i in self.hmmset:
			temp1 += i.count_tran(y, yp)
			temp2 += i.count_y(y)
		return float(temp1)/temp2

	def count_new_words(self, word_list):
		existing_words = self.getwords()
		counter = 0
		for i in word_list:
			if i not in existing_words:
				counter += 1
		return counter


def readtrain():
	# read training files from current directory
	# return a list of tweets, within which contains two sequential lists
	# of words and tags (why not dictionary? words might duplicate)
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	train = open(path + "\\trainc").read()
	print "Reading train file with " + str(len(train.split("\n\n"))) + " tweets"

	train_set = SETS()
	for i in train.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0].lower())
			tweet.add_to_tags(j.split("\t")[1])
		if tweet.get_size() > 0:
			train_set.add(tweet)
	return train_set

def readdevout(filename = "\\dev.out"):
	# read devout files from current directory
	# return a list of tweets, within which contains two sequential lists
	# of words and tags (why not dictionary? words might duplicate)
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	devout = open(path + filename).read()
	print "Reading dev.out file with " + str(len(devout.split("\n\n"))) + " tweets"

	devout_set = SETS()
	for i in devout.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0 or len(j.split("\t")) == 1:
				continue
			tweet.add_to_words(j.split("\t")[0])
			tweet.add_to_tags(j.split("\t")[1])
		if tweet.get_size() > 0:
			devout_set.add(tweet)
	return devout_set
	

def readdevin():
	# read devin files from current directory
	# return a list of tweets, within which contains one sequential list of words
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	devin = open(path + "\\dev.in").read()
	print "Reading dev.in file with " + str(len(devin.split("\n\n"))) + " tweets"

	devin_set = SETS()
	for i in devin.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words((j.split("\t")[0]).lower())
		if len(tweet.getwords()) > 0:
			devin_set.add(tweet)
	return devin_set

def readtestin():
	# read devin files from current directory
	# return a list of tweets, within which contains one sequential list of words
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	devin = open(path + "\\test.in").read()
	print "Reading test.in file with " + str(len(devin.split("\n\n"))) + " tweets"

	devin_set = SETS()
	for i in devin.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0].lower())
		if len(tweet.getwords()) > 0:
			devin_set.add(tweet)
	return devin_set

def readdevoutp1():
	# read devin files from current directory
	# return a list of tweets, within which contains one sequential list of words
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	devin = open(path + "\\dev.p1.out").read()
	# print "Reading dev.in file with " + str(len(devin.split("\n\n"))) + " tweets"

	devin_set = SETS()
	for i in devin.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0])
			tweet.add_to_tags(j.split("\t")[1])
		if tweet.get_size() > 0:
			devin_set.add(tweet)
	return devin_set

def emis_improvement():
	for k in EMISS_PARAM.keys():
		if k[0] == "@":
			for kp in EMISS_PARAM[k].keys():
				EMISS_PARAM[k][kp] = 0
			EMISS_PARAM[k]["@"] = 1
		elif k[0] == "#":
			for kp in EMISS_PARAM[k].keys():
				EMISS_PARAM[k][kp] = 0
			EMISS_PARAM[k]["#"] = 1
		elif k[:4] == "http":
			for kp in EMISS_PARAM[k].keys():
				EMISS_PARAM[k][kp] = 0
			EMISS_PARAM[k]["U"] = 1
		if k[0] != "@" and k[0] != "#" and k[:4] != "http":
			EMISS_PARAM[k]["#"] = 0
			EMISS_PARAM[k]["@"] = 0
			EMISS_PARAM[k]["U"] = 0

def readparam(filename):
	f = open(filename)
	c = f.read()
	return json.loads(c)

if __name__=="__main__":
	# main function here
	# read files
	trainingset = readtrain()
	devinset = readdevin()
	devoutset = readdevout()
	pairs = {}

	print "Generating params"
	for i in TAGS:
		temp = []
		for j in TAGS:
			temp.append(trainingset.trans_y_to_yp(i, j))
		TRANS_PARAM.append(temp)
	for i in TAGS:
		temp = [trainingset.trans_y_to_yp("start", i), trainingset.trans_y_to_yp(i, "end")]
		TRANS_PARAM_SS.append(temp)

	trainingset.calculate_emis(devinset.getwords())

	# print "\nCheck if there is trans param file:"
	# if os.path.isfile("trans.p") and os.path.isfile("trans_ss.p"):
	# 	TRANS_PARAM = readparam("trans.p")
	# 	TRANS_PARAM_SS = readparam("trans_ss.p")
	# else:
	# 	print "Generating trans params"
	# 	for i in TAGS:
	# 		temp = []
	# 		for j in TAGS:
	# 			temp.append(trainingset.trans_y_to_yp(i, j))
	# 		TRANS_PARAM.append(temp)
	# 	for i in TAGS:
	# 		temp = [trainingset.trans_y_to_yp("start", i), trainingset.trans_y_to_yp(i, "end")]
	# 		TRANS_PARAM_SS.append(temp)
	# 	f = open("trans.p", 'w')
	# 	f.write(json.dumps(TRANS_PARAM))
	# 	f.close()
	# 	f = open("trans_ss.p", 'w')
	# 	f.write(json.dumps(TRANS_PARAM_SS))
	# 	f.close()

	# print "\nCheck if there is emis param file:"
	# if os.path.isfile("emis.p"):
	# 	EMISS_PARAM = readparam("emis.p")
	# else:
	# 	print "Generating emis params"
	# 	trainingset.calculate_emis(devinset.getwords())
	# 	f = open("emis.p", 'w')
	# 	f.write(json.dumps(EMISS_PARAM))
	# 	f.close()

	print "\n###Part 1###\nProcessing:"

	filename = "dev.p1.out"
	f = open(filename, "w+")
	counter = 0
	word_list = devinset.getwords()
	no_new_word = trainingset.count_new_words(word_list)
	length = len(word_list)
	for i in word_list:
		if counter%(length/10) == (length/10)-1:
			print ".",
		counter += 1
		pairs[i] = trainingset.pos_tagger(i, no_new_word)
	devin = open(os.path.dirname(os.path.realpath(__file__)) + "\\dev.in").read()

	for i in devin.split("\n\n"):
		for j in i.split("\n"):
			if len(j.lower()) == 0:
				continue
			f.write(j + "\t" + pairs[j.lower()] + "\n")
		f.write("\n")
	f.close()
	print "\nAccuracy:" + str(readdevoutp1().get_accuracy(devoutset))

	# # Generate TRANS PARAMS
	# for i in TAGS:
	# 	temp = []
	# 	for j in TAGS:
	# 		temp.append(trainingset.trans_y_to_yp(i, j))
	# 	TRANS_PARAM.append(temp)
	# for i in TAGS:
	# 	temp = [trainingset.trans_y_to_yp("start", i), trainingset.trans_y_to_yp(i, "end")]
	# 	TRANS_PARAM_SS.append(temp)

	print "\n###Part 2###\nProcessing:"
	
	filename = "dev.p2.out"
	f = open(filename, "w+")
	counter = 0
	length = len(devinset.get_hmmset())
	for i in devinset.get_hmmset():
		# print counter
		if counter%(length/10) == (length/10)-1:
			print ".",
		counter += 1
		i.viterbi()
		i.write_to_file(f)
	f.close()
	# devoutsetp2 = readdevout("\\dev.p2.out")
	print "\nAccuracy:" + str(devinset.get_accuracy(devoutset))

	emis_improvement() ######
	filename = "dev.p3.out"
	f = open(filename, "w+")
	counter = 0
	length = len(devinset.get_hmmset())
	for i in devinset.get_hmmset():
		# print counter
		if counter%(length/10) == (length/10)-1:
			print ".",
		counter += 1
		i.viterbi()
		i.post_tag_process()
		i.write_to_file(f)
	f.close()
	# devoutsetp2 = readdevout("\\dev.p2.out")
	print "\nAccuracy:" + str(devinset.get_accuracy(devoutset))


	# print "\n###Part 3###\nProcessing:"
	
	# testinset = readtestin()
	# filename = "dev.p3.out"
	# f = open(filename, "w+")
	# counter = 0
	# length = len(testinset.get_hmmset())
	# for i in testinset.get_hmmset():
	# 	# print counter
	# 	if counter%(length/10) == (length/10)-1:
	# 		print ".",
	# 	counter += 1
	# 	i.viterbi()
	# 	i.write_to_file(f)
	# f.close()
	# # devoutsetp2 = readdevout("\\dev.p2.out")
	# print "\nAccuracy:" + str(testinset.get_accuracy(devoutset))
