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
		self.allXYKeys = set()
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
			bodyParts = list(words[self.states[0]][0][0].keys())
			for word, videos in words.items():
				self.data[word] = {}
				for frames in videos:
					for frame in frames:
						for part in bodyParts:
							if part not in self.notIncludedParts:
								x = round(frame[part][0])
								y = round(frame[part][1])
								xy = str(x)+","+str(y)
								if part not in self.allBodyParts:
									self.allBodyParts.append(part)
								if part in self.data[word].keys():
									self.data[word][part]['values'].append(xy)
									self.allXYKeys.add(xy)
								else:
									self.data[word][part]= {}
									self.data[word][part]['values'] = [xy]
									self.allXYKeys.add(xy)


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
		# print('1')
		# SET EMISSION PROBABILITIES OF EVERY OBSERVATION IN EVERY WORD PER BODYPART
		# self.allBodyParts.sort()
		# print(self.allBodyParts)
		# print(len(self.allBodyParts))
		for part in self.allBodyParts:
			obs = list(self.allXYKeys)
			# print(len(obs),len(self.allXYKeys))
			self.allDatas['emissions'][part]['observations'] = obs
			# print(part)
			for obsEv in obs:
				# print(obsEv)
				self.allDatas['emissions'][part]['emissionProbabilities'][obsEv] = {}
				for word,history in self.data.items():
					self.allDatas['emissions'][part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])
					# try:
					# 	self.allDatas['emissions'][part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])
					# except:
					# 	self.allDatas['emissions'][part]['emissionProbabilities'][obsEv][word] = history[part]['values'].count(obsEv) / len(history[part]['values'])
		print('2')

		with open('Dataset/wordTransitions.json','r') as json_file:
		# with open('../Dataset/wordTransitions.json','r') as json_file:
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

			# print(sentences)
			for i in sentences:
				# print(i[0], self.allDatas['initialProbabilities'][i[0]])
				self.allDatas['initialProbabilities'][i[0]] += 1
				# print(self.allDatas['initialProbabilities'])
				for j in range(len(i)-1):
					tempTransitions[ i[j] ][ i[j+1] ] += 1

			perWordCount = {}
			# with open('../Dataset/dataset.json') as jsonFile:
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
			# print(self.allDatas['transitionProbabilities'])
			print('3')


	def saveLearningCache(self):
		# filename = '../Dataset/learningCache.json'
		filename = 'Dataset/learningCache.json'
		with open(filename, 'w') as file:
			json.dump(self.allDatas, file)

	def getAllDatas(self):
		return self.allDatas

# from . import hmmLearning
# a = hmmLearning('../Dataset/dataset.json')
# a.startLearnFromDataset()
# a.saveLearningCache()
