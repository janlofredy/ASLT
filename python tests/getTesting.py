import json
import math
import copy

normalDistribution = []
with open('trained.json', 'r') as json_file:
	people = json.load(json_file)

# for wK, wV in people.items():
# 	print(wK)
# 	# print(wV)
# 	for x,y in wV.items():
# 		print(x)
# 		for i,j in y.items():
# 			print(i)


def normalFunc(inputXY, mean, stdDev):
	# normal = (1 / math.sqrt( 2* math.pi * stdDev**2 )) * (math.e - ( ( (inputXY - mean)**2 ) / (2 (stdDev**2)) ))
	normal = deviStd = normalDev = 0
	try:
		normal = (1 / math.sqrt( 2* math.pi * stdDev**2 )) 
		deviStd = (math.e - ( ( (inputXY - mean)**2 ) / (2 (stdDev**2)) ))
		normalDev = normal * deviStd
	except:
		normalDev = 0
	# math.sqrt(5.55124)
	# normal =  math.sqrt(2( math.pi (math.sqrt(stdDev))))
	# deviStd = math.e -(inputXY - mean) / 2 (math.sqrt(stdDev))
	# normalDev = 1 / normal * deviStd
	# return normalDev 	
	return normalDev



with open('try.json', 'r') as json_file:
	testing = json.load(json_file)
	# print(testing)
	for key, val in testing.items():
		# print(key)
		for frame in val:
			# print(frame.keys())
			frameTempNormal = {}
			for k, v in frame.items():
				# print(k)
				# print(v)
				for i in range(2):
					partName = k
					partNameXY = ""
					if i == 0:
						partNameXY = 'bodyX'
					else:
						partNameXY = 'bodyY'
					# print(people['you']['bodyX']['nose']['mean'])
					for wK, wV in people.items():
						# print(wK)
						# print(wK)

						norm = normalFunc(v[i], wV[partNameXY][partName]['mean'], wV[partNameXY][partName]['std'])
						# print(partNameXY)
						if partNameXY not in frameTempNormal.keys():
							frameTempNormal[partNameXY] = {} 
							# print(frameTempNormal.keys(), i)frameTempNormal
						if k not in frameTempNormal[partNameXY].keys():
							frameTempNormal[partNameXY][k] = {}
							# print(frameTempNormal[partNameXY].keys(), i, k, wK)
						if wK not in frameTempNormal[partNameXY][k]:
							frameTempNormal[partNameXY][k][wK] = norm
							# print(frameTempNormal[partNameXY][k].keys())

						# pass
			normalDistribution.append(copy.deepcopy(frameTempNormal))

# print(normalDistribution[0]['bodyY']['nose'].keys())
fNum = 1
for w in normalDistribution:
	youFr = 0
	okayFr = 0
	for e,r in w.items():
		you = 0
		okay = 0
		print(e)
		for t,y in r.items():
			# print('\t',t,y)

			if y['you'] > y['okay']:
				you+=1
				print(t,'you', end=", ")
			else:
				okay+=1
				print(t,'okay', end=", ")
		print()
		print(e, 'you =',you)
		print(e, 'okay =',okay)
		print()
		youFr += you
		okayFr += okay
	print('you=',youFr, 'okay=',okayFr)
	print('Frame =',fNum, ', Answer =', 'you' if youFr>okayFr else 'Okay')
	print('\n\n')
	fNum+=1

# [
# 	{
# 		'noseX' : { 'good' : 0, 'morning' : 0, 'you' : 0 }
# 		'noseY' : { 'good' : 0, 'morning' : 0, 'you' : 0 }
# 	},
# 	{
# 		'noseX' : { 'good' : 0, 'morning' : 0, 'you' : 0 }
# 		'noseY' : { 'good' : 0, 'morning' : 0, 'you' : 0 }
# 	}
# ]

# print(people['you']['bodyX'].keys())
# print(testing['test'][0].keys())
# for i in people['you']['bodyX'].keys():
# 	if i not in testing['test'][0].keys():
# 		print(i)