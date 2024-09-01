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
		tempInitialProbabilities = [] # One per State
		tempTransitionProbabilities = [] # from State to State
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
									self.allBodyParts.append(part+'X')
								if part+'Y' in self.data[word].keys():
									self.data[word][part+'Y']['values'].append(y)
									self.allYKeys.add( round(frame[part][1]) )
								else:
									self.data[word][part+'Y'] = {}
									self.data[word][part+'Y']['values'] = [y]
									self.allYKeys.add(y)
									self.allBodyParts.append(part+'Y')

		# CREATE DATASTRUCTURE PER BODYPART
		for part in self.allBodyParts:
			self.allDatas[part] = {'states': copy.deepcopy(tempState),
								'observations': copy.deepcopy(tempObservations),
								'initialProbabilities': copy.deepcopy(tempInitialProbabilities),
								'transitionProbabilities': copy.deepcopy(tempTransitionProbabilities),
								'emissionProbabilities': copy.deepcopy(tempEmissionProbabilities),
								}

		# SET EMISSION PROBABILITIES OF EVERY OBSERVATION IN EVERY WORD PER BODYPART
		for part in self.allBodyParts:
			obs = []
			if part[-1] == 'X':
				obs = list(self.allXKeys)
			elif part[-1] == 'Y':
				obs = list(self.allYKeys)
			for obsEv in obs:
				self.allDatas[part]['emissionProbabilities'][obsEv] = {}
				for word,history in self.data.items():
					try:
						self.allDatas[part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])
					except:
						self.allDatas[part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])

	def getData(self):
		return self.data

	def saveData(self):
		filename = 'Dataset/trainedData.json'
		with open(filename, 'w') as file:
			json.dump(self.data, file)

	def getCount(self):
		return self.dataCount

	def saveAllDatas(self):
		filename = 'Dataset/trainedDataHmmEmisCount.json'
		with open(filename, 'w') as file:
			json.dump(self.allDatas, file)

	def getAllDatas(self):
		return self.allDatas

# from . import hmmLearning
# a = hmmLearning('../Dataset/dataset.json')
# a.startLearnFromDataset()
# a.saveAllDatas()
