import json
import math
import copy

class hmmLearning:

	def __init__(self, dataset):

		self.dataset = dataset
		self.data = {}

		self.notIncludedParts = ['neck','nose','midHip','rightShoulder','leftShoulder','rightElbow','leftElbow']

		self.allDatas = {}
		
		# WORDS
		self.states = [] 
		# KEYPOINTS IN INT
		self.observations = {}
		# ONE EACH STATE
		self.initialProbabilities = []
		# FROM STATE TO STATE
		self.transitionProbabilities = []
		# WORD TO OBSERVATIONS LIKELIHOOD
		self.emissionProbabilities = []

		self.dataCount = {}
		self.allXKeys = set()
		self.allYKeys = set()
		self.allBodyParts = []
		self.allWords = []
		self.emissionProbabilities = {}


	def startLearnFromDataset(self):
		tempState = [] # Words
		tempObservations = [] # Keypoints nga naka int
		tempInitialProbabilities = {} # One per State
		tempTransitionProbabilities = {} # from State to State
		tempEmissionProbabilities = {} # Word to Observation Likelihood
		
		#SEPARATE X POINTS AND Y POINTS PER PART PER WORD
		with open(self.dataset, 'r') as json_file:
			words = json.load(json_file)
			self.states = list(words.keys())
			bodyParts = list(words['you'][0][0].keys())
			for word, videos in words.items():
				self.data[word] = {}
				for frames in videos:
					for frame in frames:
						for part in bodyParts:
							if part not in self.notIncludedParts:
								x = round(frame[part][0])
								y = round(frame[part][1])
								if part+'X' in self.data[word].keys():
									self.data[word][part+'X']['values'].append(x)
									self.allXKeys.add(x)
								else:
									self.data[word][part+'X'] = {}
									self.data[word][part+'X']['values'] = [x]
									self.allXKeys.add(x)
									if part+'X' not in self.allBodyParts:
										self.allBodyParts.append(part+'X')
								if part+'Y' in self.data[word].keys():
									self.data[word][part+'Y']['values'].append(y)
									self.allYKeys.add( round(frame[part][1]) )
								else:
									self.data[word][part+'Y'] = {}
									self.data[word][part+'Y']['values'] = [y]
									self.allYKeys.add(y)
									if part+'Y' not in self.allBodyParts:
										self.allBodyParts.append(part+'Y')


		# CREATE DATASTRUCTURE PER BODYPART
		self.allDatas = {
						'states': copy.deepcopy(self.states),
						'initialProbabilities': copy.deepcopy(tempInitialProbabilities),
						'transitionProbabilities': copy.deepcopy(tempTransitionProbabilities),
						'emissions' : {}
						}
		for part in self.allBodyParts:
			self.allDatas['emissions'][part] = {
								'observations': copy.deepcopy(tempObservations),
								'emissionProbabilities': copy.deepcopy(tempEmissionProbabilities),
								}

		# SET EMISSION PROBABILITIES OF EVERY OBSERVATION IN EVERY WORD PER BODYPART
		for part in self.allBodyParts:
			obs = []
			if part[-1] == 'X':
				obs = list(self.allXKeys)
			elif part[-1] == 'Y':
				obs = list(self.allYKeys)
			self.allDatas['emissions'][part]['observations'] = [obs]
			for obsEv in obs:
				self.allDatas['emissions'][part]['emissionProbabilities'][obsEv] = {}
				for word,history in self.data.items():
					try:
						self.allDatas['emissions'][part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])
					except:
						self.allDatas['emissions'][part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])

		with open('Dataset/wordTransitions.json','r') as json_file:
			file = json.load(json_file)
			sentences = file['sentences']
			tempTransitions = {}
			for i in self.allDatas['states']:
				tempTransitions[i] = {}
				self.allDatas['initialProbabilities'][i] = 0
				self.allDatas['transitionProbabilities'][i] = {}
				for j in self.allDatas['states']:
					tempTransitions[i][j] = 0
					self.allDatas['transitionProbabilities'][i][j] = 0

			print(sentences)
			for i in sentences:
				# print(i[0], self.allDatas['initialProbabilities'][i[0]])
				self.allDatas['initialProbabilities'][i[0]] += 1
				# print(self.allDatas['initialProbabilities'])
				for j in range(len(i)-1):
					tempTransitions[ i[j] ][ i[j+1] ] += 1

			perWordCount = {}
			with open('Dataset/dataset.json') as jsonFile:
				fil = json.load(jsonFile)
				words = list(fil.keys())
				for word in words:
					wordLen = 0
					wordCount = len(fil[word])
					for video in fil[word]:
						wordLen+=len(video)
					perWordCount[word] = wordLen - wordCount

			for i in self.allDatas['states']:
				tempTransitions[i][i]+=perWordCount[i]

			# print(tempTransitions)
			for k,v in tempTransitions.items():
				total = sum(v.values())
				# print(total)
				if total != 0:
					# print('asdasd')
					for key,val in v.items():
						# print(k, sum(v.values()))
						self.allDatas['transitionProbabilities'][k][key] = val/total
			print(self.allDatas['transitionProbabilities'])


	def getData(self):
		return self.data

	def saveData(self):
		filename = 'Dataset/trainedData.json'
		with open(filename, 'w') as file:
			json.dump(self.data, file)

	def getCount(self):
		return self.dataCount

	def saveLearningCache(self):
		filename = 'Dataset/learningCache.json'
		with open(filename, 'w') as file:
			json.dump(self.allDatas, file)

	def getAllDatas(self):
		return self.allDatas

# from . import hmmLearning
# a = hmmLearning('../Dataset/dataset.json')
# a.startLearnFromDataset()
# a.saveLearningCache()
