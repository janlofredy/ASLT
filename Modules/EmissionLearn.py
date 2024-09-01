import json
import math
import copy

class emissionLearn():

	def __init__(self, dataset):
		self.dataset = dataset
		self.data = {}

	def start(self):
		dictForm = {'values': [], 'sum': 0, 'mean':0,'std':0}
			
		with open(self.dataset, 'r') as json_file:
			words = json.load(json_file)
			# temp = {}
			bodyParts = list(words['you'][0][0].keys())
			# print(bodyParts)
			for word, videos in words.items():
				self.data[word] = {}
				for frames in videos:
					for frame in frames:
						for part in bodyParts:
							if part+'X' in self.data[word].keys():
								self.data[word][part+'X']['values'].append(frame[part][0])
							else:
								self.data[word][part+'X'] = {}
								self.data[word][part+'X']['values'] = [frame[part][0]]
							if part+'Y' in self.data[word].keys():
								self.data[word][part+'Y']['values'].append(frame[part][1])
							else:
								self.data[word][part+'Y'] = {}
								self.data[word][part+'Y']['values'] = [frame[part][1]]
						# for part, values in frame.items():
						# 	if part == 'nose' and word=='you':
						# 		noseX.append(values[0])
						# 	if part+'X' not in temp.keys():
						# 		temp[part+'X'] = copy.deepcopy(dictForm)

						# 	if part+'Y' not in temp.keys():
						# 		temp[part+'Y'] = copy.deepcopy(dictForm)
						# 	# print(temp[part+'Y'])
						# 	temp[part+'X']['values'].append(values[0])
						# 	temp[part+'Y']['values'].append(values[1])
				# print(self.data['you']['leftShoulderY']['values'])
				# self.data[word] = copy.deepcopy(temp)
		# print('with self.data',sum(self.data['you']['noseX']['values']))
		# print('with self.data',self.data['you']['noseX']['sum'])
		for word, parts in self.data.items():
			for part, emData in parts.items():
				lim = 500
				values =  copy.deepcopy(emData['values'][0:lim])
				tempSum   = sum(values)
				tempMean = tempSum / len(values)
				forStdDev = []
				for i in values:
					forStdDev.append(( i - tempMean )**2 )
				# print(sum(forStdDev))
				tempStd = math.sqrt( sum(forStdDev)/ (len(forStdDev)-1) )
				# tempStd
				self.data[word][part]['sum'] = tempSum
				self.data[word][part]['mean'] = tempMean
				self.data[word][part]['std'] = tempStd

	def getData(self):
		return self.data
					
	def saveData(self):
		filename = 'Dataset/trainedData.json'
		with open(filename, 'w') as file:
			json.dump(self.data, file)

# from . import emissionLearn

# a = emissionLearn('../Dataset/dataset.json')
# a.start()

# vals= []
# learned = a.getData()
# # print(learned)
# for word, ls in learned.items():
# 	# print(word)
# 	# print(ls.keys())
# 	# print(word)
# 	vals.append(ls['noseX']['sum'])
# 	for key , data in ls.items():
# 		pass
# 		# print(key)
# 		# vals.append(data['mean']['rightHandHeel'])
# 		# print(word, data['mean'])
# print(vals)