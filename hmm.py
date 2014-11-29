# 50.007 ML
# Li Hanwei
# Wang Tianchi
# Wang Yingbei

# import libs
import os

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
			
		for i in range(0, self.get_size):
			if self.tags[i] == y:
				if self.tags[i + 1] == x:
					temp += 1
		return temp

	def count_emis(self, y, x):


	def tag_exist(self, y):
		return y in self.tags


def readtrain():
	# read training files from current directory
	# return a list of tweets, within which contains two sequential lists
	# of words and tags (why not dictionary? words might duplicate)
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	train = open(path + "\\train").read()
	print "Reading train file with " + str(len(train.split("\n\n"))) + " tweets"

	train_set = []
	for i in train.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0])
			tweet.add_to_tags(j.split("\t")[1])
		train_set.append(tweet)
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

	devout_set = []
	for i in devout.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0])
			tweet.add_to_tags(j.split("\t")[1])
		devout_set.append(tweet)
	return devout_set
	

def readdevin():
	# read devin files from current directory
	# return a list of tweets, within which contains one sequential list of words
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	devin = open(path + "\\dev.in").read()
	print "Reading dev.in file with " + str(len(devin.split("\n\n"))) + " tweets"

	devin_set = []
	for i in devin.split("\n\n"):
		tweet = HMM()
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			tweet.add_to_words(j.split("\t")[0])
		devin_set.append(tweet)
	return devin_set

if __name__=="__main__":
	# main function here
	# read files
	readtrain()
	readdevin()
	readdevout()
	test()