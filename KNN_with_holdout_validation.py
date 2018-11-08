import csv
import random
import math
import operator 

class Knn:
	trainingSet = []
	testSet = []
	def __init__(self, filename,split):
		self.loadDataset(filename,split)
		print "Traning data and Test data is sorted"
		print 'Train set: ' + repr(len(self.trainingSet))
		print 'Test set: ' + repr(len(self.testSet))

	def loadDataset(self,filename, split):
		with open(filename, 'rb') as csvfile:
		    lines = csv.reader(csvfile)
		    dataset = list(lines)
		# for row in lines:
		# 	print ', '.join(row)
		for x in range(len(dataset)-1):
			for y in range(4):
				dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				self.trainingSet.append(dataset[x])
			else:
			    self.testSet.append(dataset[x])
		# print "Training set: \r" + str(trainingSet)
		# print "Test set \r" + str(testSet)
	

	def euclideanDistance(self,instance1, instance2, length):
		distance = 0
		for x in range(length):
			distance += pow((instance1[x] - instance2[x]), 2)
		return math.sqrt(distance)


	def getNeighbors(self,testInstance):
		distances = []
		length = len(testInstance)-1
		for x in range(len(self.trainingSet)):
			dist = self.euclideanDistance(testInstance, self.trainingSet[x], length)
			distances.append((self.trainingSet[x], dist))
		distances.sort(key=operator.itemgetter(1))
		neighbors = []
		for x in range(self.k):
			neighbors.append(distances[x][0])
		# print "in neighbours"
		#print neighbors
		return neighbors
	
	def getResponse(self,neighbors):
		classVotes = {}
		for x in range(len(neighbors)):
			response = neighbors[x][-1]
			# print "in get response: " + response
			if response in classVotes:
				classVotes[response] += 1
			else:
				classVotes[response] = 1
		sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
		# print "In response: " + sortedVotes[0][0]
		return sortedVotes[0][0]

	def getAccuracy(self,predictions):
		correct = 0
		for x in range(len(self.testSet)):
			# print "In Get accuracy" + "testSet:" + testSet[x][-1] + " predictions: " + predictions[x]
			if (self.testSet[x][-1] == predictions[x]):
				# print "x"
				correct += 1
		return (correct/float(len(self.testSet))) * 100.0

	def predict(self):
		# generate predictions
		predictions=[]
		self.k = 3
		for x in range(len(self.testSet)):
			neighbors = self.getNeighbors(self.testSet[x])
			result = self.getResponse(neighbors)
			predictions.append(result)
			print('> predicted=' + repr(result) + ', actual=' + repr(self.testSet[x][-1]))
		accuracy = self.getAccuracy(predictions)
		print('Accuracy: ' + repr(accuracy) + '%')
	
def main():
	# prepare data
	split = 0.67
	filename = 'iris.data'
	# loadDataset('iris.data', split, trainingSet, testSet)
	obj = Knn(filename,split)
	obj.predict()	
	
main()