import json
import math
import copy

class emissionTest():

	def __init__(self, data):
		self.dataset = data
		self.learned = 'Dataset/trainedData.json'
		self.data = []

	def normalFunction(self, inputXY, mean, stdDev):
		normal = devStd = normalDev = 0
		normal = (1 / math.sqrt( 2* math.pi * stdDev ** 2 ) ) 
		deviStd = (math.e - ( ( (inputXY - mean)**2 ) / (2 * (stdDev**2)) ))
		normalDev = normal * deviStd
		# print(inputXY)
		return normalDev if normalDev>=0 else -normalDev

	def start(self):
		# vals= []
		with open(self.learned, 'r') as json_file:
			self.learned = json.load(json_file)
			print(self.learned.keys())
			# for word, ls in self.learned.items():
			# 	# print(word)
			# 	# print(ls.keys())
			# 	vals.append(ls['rightHandHeelX']['mean'])
			# 	for key , data in ls.items():
			# 		pass
			# 		# print(key)
			# 		# vals.append(data['mean']['rightHandHeel'])
			# 		# print(word, data['mean'])
		# print(vals)
		for frame in self.dataset:
			frameTempNormal = {}
			for part, xAndY in frame.items():
				if part not in ['neck','nose','midHip','rightShoulder','leftShoulder','rightElbow','leftElbow']:
					for i in range(2):
						partName = part
						if i == 0:
							partName += 'X'
						else:
							partName += 'Y'
						# print(partName)

						for word, learnedSet in self.learned.items():
							norm = self.normalFunction(xAndY[i], learnedSet[partName]['mean'], learnedSet[partName]['std'])	
							# print(word, partName, self.learned[word][partName]['mean'])
							if partName not in frameTempNormal.keys():
								frameTempNormal[partName] = {}
							else:
								frameTempNormal[partName][word] = copy.deepcopy(norm)
			self.data.append(copy.deepcopy(frameTempNormal))


	def getEmissions(self):
		return self.data

# from . import emissionTest

# test = [{'neck': [0, 0], 'nose': [0.013152197943385608, 34.974242935152695], 'midHip': [-3.936598979988017, -78.92598913297854], 'rightShoulder': [23.6924161385853, -1.6528513290985398], 'rightElbow': [28.19925934887067, -43.40649698904224], 'rightWrist': [10.720982003733583, -12.96078377722823], 'rightHandHeel': [9.575010537951817, -12.00335637574153], 'rightLFOne': [-2.4418195339050475, -8.922112050356922], 'rightLFTwo': [-4.598686469879357, -8.305864354364264], 'rightLFThree': [-3.212129153895872, -8.768050126358759], 'rightLFFour': [-1.517447989916058, -9.538359746349583], 'rightRFOne': [-1.8255718379123878, -5.840873570393624], 'rightRFTwo': [-4.906810317875687, -4.76244010240647], 'rightRFThree': [-3.0580672298977074, -5.99493549439179], 'rightRFFour': [-0.9012002939233983, -6.919307038380778], 'rightMFOne': [-0.5930764459270684, -2.143381549016358], 'rightMFTwo': [-4.444624545881192, -1.6811957770218628], 'rightMFThree': [-2.9040053058995423, -3.0677589384266555], 'rightMFFour': [-0.5930764459270684, -3.992130482415645], 'rightPFOne': [1.8719143380435705, 1.091918854945106], 'rightPFTwo': [-2.9040053058995423, 2.1703523229322603], 'rightPFThree': [-2.9040053058995423, 1.4000427029414357], 'rightPFFour': [-1.517447989916058, -0.6027623090347084], 'rightTOne': [9.729084152792598, -7.073368962378944], 'rightTTwo': [8.188453221968333, -2.143381549016358], 'rightTThree': [2.950347806030725, 0.013485386957951378], 'rightTFour': [0.4853570220600862, -0.9108861570310383], 'leftShoulder': [-25.91250715142879, 1.7090725912405322], 'leftElbow': [-31.565731006987498, -41.696641111346416], 'leftWrist': [-35.51599658199402, -82.27845516164099], 'leftHandHeel': [-34.82523145516479, -83.03949394343707], 'leftLFOne': [-37.816754408890276, -96.6676377805766], 'leftLFTwo': [-36.65339866013801, -101.48733963011792], 'leftLFThree': [-34.492837417896936, -102.15212770465364], 'leftLFFour': [-32.49847319428979, -102.65071876055542], 'leftRFOne': [-37.816754408890276, -97.66481989238018], 'leftRFTwo': [-36.32100462287015, -103.1493098164572], 'leftRFThree': [-32.66467021292372, -105.4760680773322], 'leftRFFour': [-29.673123877513, -106.80564422640364], 'leftMFOne': [-36.98579269740586, -98.49580498554982], 'leftMFTwo': [-34.99142847379872, -105.4760680773322], 'leftMFThree': [-31.833685119754076, -107.80282633820721], 'leftMFFour': [-29.008335802977285, -108.46761441274292], 'leftPFOne': [-34.65903443653086, -98.66200200418375], 'leftPFTwo': [-33.49565530609336, -105.64226509596614], 'leftPFThree': [-30.8365030079505, -108.301417394109], 'leftPFFour': [-28.17735070980764, -109.63099354318042], 'leftTOne': [-31.00270002658443, -87.36061642791921], 'leftTTwo': [-29.008335802977285, -93.67609144516588], 'leftTThree': [-28.17735070980764, -100.15776348104649], 'leftTFour': [-28.17735070980764, -104.14649192826077]}]

# a = emissionTest(test)
# a.start()
# print(a.getEmissions())
