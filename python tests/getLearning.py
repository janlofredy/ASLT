import json
import copy
import math

people = {}

class Person:
	def __init__(self):
		self.bodyX = {
			"neck": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"nose": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"midHip": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightShoulder": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightElbow": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightWrist": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightHandHeel": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},"rightRFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightRFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightRFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightRFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftShoulder": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftElbow": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftWrist": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftHandHeel": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFFourA": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFFourA": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftMFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftMFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFMThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftMFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			}
		}

		self.bodyY = {
			"neck": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"nose": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"midHip": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightShoulder": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightElbow": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightWrist": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightHandHeel": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightLFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},"rightRFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightRFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightRFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightRFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightMFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightPFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"rightTFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftShoulder": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftElbow": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftWrist": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftHandHeel": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFFourA": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftRFFourA": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftMFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftMFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftLFMThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftMFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftPFFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTOne": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTTwo": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTThree": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			},
			"leftTFour": {
				'value': [],
				'sum': 0,
				'mean': 0,
				'std': 0
			}
		}
		

with open('../Dataset/dataset.json', 'r') as json_file:
	people = json.load(json_file)
	for name, videos in people.items():
		people[name] = Person()
		for video in videos:
			for frame in video:
				for partName, bodyPart in frame.items():
					people[name].bodyX[partName]['value'].append(bodyPart[0])
					people[name].bodyY[partName]['value'].append(bodyPart[1])

for key, val in people.items():
	for attr, value in val.__dict__.items():
		for k, v in value.items():
			v['sum'] = sum(v['value'])
			v['mean'] = v['sum'] / len(v['value'])
			forStdDev = []
			for i in v['value']:
				forStdDev.append((i-v['mean'])**2)
			v['std'] = math.sqrt( sum( forStdDev ) / ( len( forStdDev ) -1 ) )


datas = {}

for key, val in people.items():
	datas[key] = {}
	for attr, value in val.__dict__.items():
		datas[key][attr] = value

filename = 'trained.json'
with open(filename, 'w') as f:
    json.dump(datas, f)

