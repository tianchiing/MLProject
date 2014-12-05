# 50.007 ML
# Li Hanwei
# Wang Tianchi
# Wang Yingbei

# import libs
import os

TAGS = ['~', '@', 'O', 'V', '^', ',', '$', 'R', 'A', '!', 'P', 'T', 'N', '&', 'D', '#', 'G', 'U', 'L', 'E', 'X', 'Z', 'S', 'M', 'Y']

class HMM:
	def __init__(self):
		self.words = []
		self.tags = []

	def add_to_words(self, word):
		self.words.append(word)

	def add_to_tags(self, tag):
		self.tags.append(tag)

	def get_size(self):
		return len(self.words)

	def count_y(self, y):
		temp = 0
		# print "here"
		for i in self.tags:
			if i == y:
				temp += 1
		return temp

	def count_tran(self, y = "start", x = "end"):
		temp = 0
		if y == "start":
			return 1 if self.tags[0] == x else 0

		if x == "end":
			return 1 if self.tags[-1] == y else 0
			
		for i in range(0, self.get_size()):
			if self.tags[i] == y:
				if self.tags[i + 1] == x:
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

	def estimate_emission_param(self, y, x):
		# return self.overall_count_y(y)
		# print self.overall_count_y_to_x(y, x)
		return self.overall_count_y_to_x(y, x)/float(self.overall_count_y(y) + 1)

	def size(self):
		return len(self.hmmset)

	# def getfirst(self):
	# 	return self.hmmset[1].getwords()

	def is_new_word(self, x):
		result = True
		for i in self.hmmset:
			result = result and i.is_word_not_exist(x)
		return result

	def pos_tagger(self, x):
		maximum = 0
		y = ""
		for i in TAGS:
			temp = self.estimate_emission_param(i, x)
			# print temp
			if temp > maximum:
				maximum = temp
				y = i
		return y

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
			for j in i.get_unique_words():
				if j not in result:
					result.append(j)
		return result


def readtrain():
	# read training files from current directory
	# return a list of tweets, within which contains two sequential lists
	# of words and tags (why not dictionary? words might duplicate)
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	train = open(path + "\\train").read()
	print "Reading train file with " + str(len(train.split("\n\n"))) + " tweets"

	train_set = SETS()
	for i in train.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0])
			tweet.add_to_tags(j.split("\t")[1])
		train_set.add(tweet)
	return train_set

def readdevout():
	# read devout files from current directory
	# return a list of tweets, within which contains two sequential lists
	# of words and tags (why not dictionary? words might duplicate)
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	devout = open(path + "\\dev.out").read()
	print "Reading dev.out file with " + str(len(devout.split("\n\n"))) + " tweets"

	devout_set = SETS()
	for i in devout.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0])
			tweet.add_to_tags(j.split("\t")[1])
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
			tweet.add_to_words(j.split("\t")[0])
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
		devin_set.add(tweet)
	return devin_set

if __name__=="__main__":
	# main function here
	# read files
	trainingset = readtrain()
	devinset = readdevin()
	# print trainingset.size()
	# print devinset.size()
	# print readdevout().size()
	# print trainingset.estimate_emission_param("N", "yard")
	# print trainingset.estimate_emission_param("Y", "yard")
	# print trainingset.gettags()
	# print trainingset.pos_tagger("yard")
	# print trainingset.pos_tagger("@USER_0240cb3a")

	# print len(devinset.getwords())
	# pairs = {}

	# filename = "dev.p1.out"
	# f = open(filename, "r+")
	# counter = 0
	# for i in devinset.getwords():
	# 	print counter
	# 	counter += 1
	# 	pairs[i] = trainingset.pos_tagger(i)
	# devin = open(os.path.dirname(os.path.realpath(__file__)) + "\\dev.in").read()
	# for i in devin.split("\n\n"):
	# 	for j in i.split("\n"):
	# 		if len(j) == 0:
	# 			continue
	# 		f.write(j + "\t" + pairs[j] + "\n")
	# 	f.write("\n")
	# f.close()

	print readdevoutp1().get_accuracy(readdevout())

	# filename = "dev.p1.out"
	# counter = 0
	# for i in devinset.get_hmm_set():
	# 	counter += 1
	# 	print counter
	# 	# temp = []
	# 	for j in i.getwords():
	# 		# print j
	# 		i.add_to_tags(trainingset.pos_tagger(j))
	# f = open(filename, "r+")
	# # print "here"
	# for i in devinset.get_hmm_set():
	# 	i.write_to_file(f)
	# f.close()

	# print trainingset.getfirst()
	# test()