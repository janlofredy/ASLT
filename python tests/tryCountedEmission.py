
testAnswers = {}
mgaAnswers = []
with open('Dataset/trainedDataHmmEmisCount.json') as json_file:
    hmmEmissions = json.load(json_file)
z = 1
for frame in testData:
    for part,keyPointsXnY in frame.items():
        if part not in self.notIncludedParts:
            for i in range(2):
                print(z)
                z+=1
                partName = part
                curPoint = str(int(round(keyPointsXnY[i])))
                if i == 0:
                    partName+='X'
                else:
                    partName+='Y'
                # print(partName)
                # print(hmmEmissions[partName]['emissionProbabilities'].keys())
                if curPoint not in hmmEmissions[partName]['emissionProbabilities'].keys():
                    print(curPoint,'Never Found ')
                else:
                    datas = hmmEmissions[partName]['emissionProbabilities'][curPoint]
                    maxs = self.getMax(datas)
                    print(maxs, datas)
                    mgaAnswers.append(maxs)
                    if maxs not in testAnswers.keys():
                        testAnswers[maxs] = 1
                    else:
                        testAnswers[maxs] += 1
print(testAnswers)
print(mgaAnswers)