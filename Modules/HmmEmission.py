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
		self.allKeys = set()
		self.allBodyParts = []
		self.allWords = []
		self.emissionProbabilities = {}


	def startLearnFromDataset(self):
		print('WORKING ON IT PLEASE WAIT')
		tempState = [] # Words
		tempObservations = [] # Keypoints nga naka int
		tempInitialProbabilities = {} # One per State
		tempTransitionProbabilities = {} # from State to State
		tempEmissionProbabilities = {} # Word to Observation Likelihood

		forEmission = {}

		#SEPARATE X POINTS AND Y POINTS PER PART PER WORD
		with open(self.dataset, 'r') as json_file:
			words = json.load(json_file)
			self.states = list(words.keys())
			for i in self.states:
				# print(i)
				forEmission[i] = []
			bodyParts = list(words[self.states[0]][0][0].keys())
			bodyParts.sort()
			for word, videos in words.items():
				for frames in videos:
					for frame in frames:
						tempObs = []
						for i in range(250):
							tempObs.append('0'*250)
						for part in bodyParts:
							if part not in self.notIncludedParts:
								x = round(frame[part][0])
								y = round(frame[part][1])
								tempStr = list(tempObs[x])
								tempStr[y] = '1'
								tempObs[x] = "".join(tempStr)
								
								# tempObs += part + str(round(frame[part][0])) +"~"+ str(round(frame[part][1]))+" "

						self.allKeys.add( "".join(tempObs) )
						forEmission[word].append("".join(tempObs))

		# CREATE DATASTRUCTURE PER BODYPART
		self.allDatas = {
						'states': copy.deepcopy(self.states),
						'initialProbabilities': copy.deepcopy(tempInitialProbabilities),
						'transitionProbabilities': copy.deepcopy(tempTransitionProbabilities),
						'observations': copy.deepcopy(tempObservations),
						'emissionProbabilities': copy.deepcopy(tempEmissionProbabilities),
						}

		# SET EMISSION PROBABILITIES OF EVERY OBSERVATION IN EVERY WORD
		obs = list(self.allKeys)
		self.allDatas['observations'] = obs
		for obsEv in obs:
			self.allDatas['emissionProbabilities'][obsEv] = {}
			for word,history in forEmission.items():
				try:
					self.allDatas['emissionProbabilities'][obsEv][word] = history.count(obsEv) / len(history)
				except:
					self.allDatas['emissionProbabilities'][obsEv][word] = history.count(obsEv) / len(history)
		# print(self.allDatas['emissionProbabilities'])


		# with open('../Dataset/wordTransitions.json','r') as json_file:
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


	def getData(self):
		return self.data

	def saveData(self):
		filename = 'Dataset/trainedData.json'
		with open(filename, 'w') as file:
			json.dump(self.data, file)

	def getCount(self):
		return self.dataCount

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
