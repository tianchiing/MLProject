# 50.007 ML
# Li Hanwei
# Wang Tianchi
# Wang Yingbei

# import libs
import os

def readtrain():
	# read training files from current directory
	# return a list of tweets, within which contains two sequential lists
	# of words and tags (why not dictionary? words might duplicate)
	# current file path
	path = os.path.dirname(os.path.realpath(__file__))
	# read files to look for
	train = open(path + "\\train").read()
	devout = open(path + "\\dev.out").read()
	devin = open(path + "\\dev.in").read()
	print "Reading train file with " + str(len(train.split("\n\n"))) + " tweets"

	train_set = []
	for i in train.split("\n\n"):
		word = []
		tag = []
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			word.append(j.split("\t")[0])
			tag.append(j.split("\t")[1])
		train_set.append([word, tag])
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
		word = []
		tag = []
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			word.append(j.split("\t")[0])
			tag.append(j.split("\t")[1])
		devout_set.append([word, tag])
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
		word = []
		for j in i.split("\n"):
			# handle file ending
			if len(j) == 0:
				continue
			word.append(j.split("\t")[0])
		devin_set.append(word)
	return devin_set

if __name__=="__main__":
	# main function here
	# read files
	readtrain()
	readdevin()
	readdevout()