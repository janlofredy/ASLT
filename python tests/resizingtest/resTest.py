z = {
'body' : {'nose': [977.6597, 209.47661], 'neck': [962.9873, 412.71307], 'midhip': [998.27875, 833.42194], 'rightShoulder': [839.358, 412.53613], 'rightElbow': [836.34515, 645.1577], 'rightWrist': [865.84454, 865.8559], 'leftShoulder': [1089.5183, 418.3953], 'leftElbow': [1112.9951, 621.42847], 'leftWrist': [1139.5532, 824.5737]},
'rightHand' : {'0': [871.04144, 862.4491], '1': [899.1766, 891.4918], '2': [915.5131, 921.44214], '3': [920.051, 955.0228], '4': [923.6814, 974.9897], '5': [897.3614, 950.4849], '6': [910.0676, 985.88074], '7': [915.5131, 1006.7552], '8': [921.8662, 1022.18414], '9': [879.2097, 953.20764], '10': [890.1007, 991.32623], '11': [899.1766, 1012.2007], '12': [905.52966, 1032.1676], '13': [869.22626, 948.66974], '14': [870.13385, 983.15796], '15': [879.2097, 1003.1249], '16': [887.378, 1014.92346], '17': [858.3352, 940.50146], '18': [858.3352, 970.4518], '19': [863.78076, 983.15796], '20': [866.5035, 992.2338]},
'leftHand' : {'0': [1139.1315, 841.50665], '1': [1125.7701, 867.3943], '2': [1119.0895, 901.6327], '3': [1119.0895, 934.201], '4': [1124.1, 959.2535], '5': [1150.8226, 921.67474], '6': [1147.4823, 960.92365], '7': [1133.2859, 976.7903], '8': [1119.9246, 987.64636], '9': [1158.3385, 921.67474], '10': [1152.4929, 960.92365], '11': [1138.2964, 975.9552], '12': [1123.2649, 985.1411], '13': [1158.3385, 919.1695], '14': [1157.5034, 950.06757], '15': [1139.1315, 968.43945], '16': [1126.6052, 975.9552], '17': [1154.1631, 913.32385], '18': [1153.328, 945.05707], '19': [1143.3069, 953.4079], '20': [1133.2859, 961.7587]}
}
import matplotlib.pyplot as plt
import math
import copy

width = 250
height = 250
# Finding the percentage of the length of each part of the arm
i = z
# if 0 not in [	
# 				i['body']['neck'][0],i['body']['neck'][1],
# 				i['body']['rightShoulder'][0],i['body']['rightElbow'][0],i['body']['rightWrist'][0],i['rightHand']['0'][0],i['rightHand']['9'][0],i['rightHand']['10'][0],i['rightHand']['11'][0],i['rightHand']['12'][0],
# 				i['body']['rightShoulder'][1],i['body']['rightElbow'][1],i['body']['rightWrist'][1],i['rightHand']['0'][1],i['rightHand']['9'][1],i['rightHand']['10'][1],i['rightHand']['11'][1],i['rightHand']['12'][1]
# 			]:
# 	gotBasis= True
# 	neckToShoulderWidth = abs(i['body']['neck'][0] - i['body']['rightShoulder'][0])
# 	neckToShoulderHeight = abs(i['body']['neck'][1] - i['body']['rightShoulder'][1])
# 	if neckToShoulderWidth == 0:
# 		neckToShoulder = neckToShoulderHeight
# 	elif neckToShoulderWidth == 0:
# 		neckToShoulder = neckToShoulderWidth
# 	else:
# 		neckToShoulder = math.sqrt(neckToShoulderWidth**2 + neckToShoulderHeight**2)
# 	shoulderToElbowWidth = abs(i['body']['rightShoulder'][0] - i['body']['rightElbow'][0])
# 	shoulderToElbowHeight = abs(i['body']['rightShoulder'][1] - i['body']['rightElbow'][1])
# 	if shoulderToElbowWidth == 0:
# 		shoulderToElbow = shoulderToElbowHeight
# 	elif shoulderToElbowHeight == 0:
# 		shoulderToElbow = shoulderToElbowWidth
# 	else:
# 		shoulderToElbow = math.sqrt( shoulderToElbowHeight**2 + shoulderToElbowWidth**2 )
# 	elbowToWristWidth = abs(i['body']['rightElbow'][0] - i['body']['rightWrist'][0])
# 	elbowToWristHeight = abs(i['body']['rightElbow'][1] - i['body']['rightWrist'][1])
# 	if elbowToWristWidth == 0:
# 		elbowToWrist = elbowToWristHeight
# 	elif elbowToWristHeight == 0:
# 		elbowToWrist = elbowToWristWidth
# 	else:
# 		elbowToWrist = math.sqrt( elbowToWristWidth**2+ elbowToWristHeight**2 )
# 	wristToHandWristWidth = abs(i['body']['rightWrist'][0] - i['rightHand']['0'][0])
# 	wristToHandWristHeight = abs(i['body']['rightWrist'][1] - i['rightHand']['0'][1])
# 	if wristToHandWristWidth == 0:
# 		wristToHandWrist = wristToHandWristHeight
# 	elif wristToHandWristHeight == 0:
# 		wristToHandWrist = wristToHandWristWidth
# 	else:
# 		wristToHandWrist = math.sqrt( wristToHandWristWidth**2 + wristToHandWristHeight**2 )
# 	HandWristToMFOneWidth = abs(i['rightHand']['0'][0] - i['rightHand']['9'][0])
# 	HandWristToMFOneHeight = abs(i['rightHand']['0'][1] - i['rightHand']['9'][1])
# 	if HandWristToMFOneWidth == 0:
# 		HandWristToMFOne = HandWristToMFOneHeight
# 	elif HandWristToMFOneHeight == 0:
# 		HandWristToMFOne = HandWristToMFOneWidth
# 	else:
# 		HandWristToMFOne = math.sqrt( HandWristToMFOneWidth**2 + HandWristToMFOneHeight**2 )
# 	MFOneToMFTwoWidth = abs(i['rightHand']['9'][0] - i['rightHand']['10'][0])
# 	MFOneToMFTwoHeight = abs(i['rightHand']['9'][1] - i['rightHand']['10'][1])
# 	if MFOneToMFTwoWidth == 0:
# 		MFOneToMFTwo = MFOneToMFTwoHeight
# 	elif MFOneToMFTwoHeight == 0:
# 		MFOneToMFTwo = MFOneToMFTwoWidth
# 	else:
# 		MFOneToMFTwo = math.sqrt( MFOneToMFTwoWidth**2+ MFOneToMFTwoHeight**2 )
# 	MFTwoToMGThreeWidth = abs(i['rightHand']['10'][0] - i['rightHand']['11'][0])
# 	MFTwoToMGThreeHeight = abs(i['rightHand']['10'][1] - i['rightHand']['11'][1])
# 	if MFTwoToMGThreeWidth == 0:
# 		MFTwoToMGThree = MFTwoToMGThreeHeight
# 	elif MFTwoToMGThreeHeight == 0:
# 		MFTwoToMGThree = MFTwoToMGThreeWidth
# 	else:
# 		MFTwoToMGThree = math.sqrt( MFTwoToMGThreeWidth**2 + MFTwoToMGThreeHeight**2 )
# 	MFThreeToMFFourWidth = abs(i['rightHand']['11'][0] - i['rightHand']['12'][0])
# 	MFThreeToMFFourHeight = abs(i['rightHand']['11'][1] - i['rightHand']['12'][1])
# 	if MFThreeToMFFourWidth == 0:
# 		MFThreeToMFFour = MFThreeToMFFourHeight
# 	elif MFThreeToMFFourHeight == 0:
# 		MFThreeToMFFour = MFThreeToMFFourWidth
# 	else:
# 		MFThreeToMFFour = math.sqrt( MFThreeToMFFourWidth**2 + MFThreeToMFFourHeight**2 )




if 0 not in 	[	
				i['body']['neck'][0],i['body']['neck'][1],
				i['body']['leftShoulder'][0],i['body']['leftElbow'][0],i['body']['leftWrist'][0],i['leftHand']['0'][0],i['leftHand']['9'][0],i['leftHand']['10'][0],i['leftHand']['11'][0],i['leftHand']['12'][0],
				i['body']['leftShoulder'][1],i['body']['leftElbow'][1],i['body']['leftWrist'][1],i['leftHand']['0'][1],i['leftHand']['9'][1],i['leftHand']['10'][1],i['leftHand']['11'][1],i['leftHand']['12'][1]
				]:
	gotBasis= True
	neckToShoulderWidth = round(abs(i['body']['neck'][0] - i['body']['leftShoulder'][0]),2)
	neckToShoulderHeight = round(abs(i['body']['neck'][1] - i['body']['leftShoulder'][1]),2)
	if neckToShoulderWidth == 0:
		neckToShoulder = round( neckToShoulderHeight,2)
	elif neckToShoulderWidth == 0:
		neckToShoulder = round(neckToShoulderWidth,2)
	else:
		neckToShoulder = round(math.sqrt(neckToShoulderWidth**2 + neckToShoulderHeight**2),2)
	shoulderToElbowWidth = round(abs(i['body']['leftShoulder'][0] - i['body']['leftElbow'][0]),2)
	shoulderToElbowHeight = round(abs(i['body']['leftShoulder'][1] - i['body']['leftElbow'][1]),2)
	if shoulderToElbowWidth == 0:
		shoulderToElbow = round(shoulderToElbowHeight,2)
	elif shoulderToElbowHeight == 0:
		shoulderToElbow = round(shoulderToElbowWidth,2)
	else:
		shoulderToElbow = round(math.sqrt( shoulderToElbowHeight**2 + shoulderToElbowWidth**2 ),2)
	elbowToWristWidth = round(abs(i['body']['leftElbow'][0] - i['body']['leftWrist'][0]),2)
	elbowToWristHeight = round(abs(i['body']['leftElbow'][1] - i['body']['leftWrist'][1]),2)
	if elbowToWristWidth == 0:
		elbowToWrist = round(elbowToWristHeight,2)
	elif elbowToWristHeight == 0:
		elbowToWrist = round(elbowToWristWidth,2)
	else:
		elbowToWrist = round(math.sqrt( elbowToWristWidth**2 + elbowToWristHeight**2 ),2)
	wristToHandWristWidth = round(abs(i['body']['leftWrist'][0] - i['leftHand']['0'][0]),2)
	wristToHandWristHeight = round(abs(i['body']['leftWrist'][1] - i['leftHand']['0'][1]),2)
	if wristToHandWristWidth == 0:
		wristToHandWrist = round(wristToHandWristHeight,2)
	elif wristToHandWristHeight == 0:
		wristToHandWrist = round(wristToHandWristWidth,2)
	else:
		wristToHandWrist =round( math.sqrt( wristToHandWristWidth**2 + wristToHandWristHeight**2 ),2)
	HandWristToMFOneWidth = round(abs(i['leftHand']['0'][0] - i['leftHand']['9'][0]),2)
	HandWristToMFOneHeight = round(abs(i['leftHand']['0'][1] - i['leftHand']['9'][1]),2)
	if HandWristToMFOneWidth == 0:
		HandWristToMFOne = round(HandWristToMFOneHeight,2)
	elif HandWristToMFOneHeight == 0:
		HandWristToMFOne = round(HandWristToMFOneWidth,2)
	else:
		HandWristToMFOne = round(math.sqrt( HandWristToMFOneWidth**2 + HandWristToMFOneHeight**2 ),2)
	MFOneToMFTwoWidth = round(abs(i['leftHand']['9'][0] - i['leftHand']['10'][0]),2)
	MFOneToMFTwoHeight = round(abs(i['leftHand']['9'][1] - i['leftHand']['10'][1]),2)
	if MFOneToMFTwoWidth == 0:
		MFOneToMFTwo = round(MFOneToMFTwoHeight,2)
	elif MFOneToMFTwoHeight == 0:
		MFOneToMFTwo = round(MFOneToMFTwoWidth,2)
	else:
		MFOneToMFTwo = round(math.sqrt( MFOneToMFTwoWidth**2 + MFOneToMFTwoHeight**2 ),2)
	MFTwoToMGThreeWidth = round(abs(i['leftHand']['10'][0] - i['leftHand']['11'][0]),2)
	MFTwoToMGThreeHeight = round(abs(i['leftHand']['10'][1] - i['leftHand']['11'][1]),2)
	if MFTwoToMGThreeWidth == 0:
		MFTwoToMGThree = round(MFTwoToMGThreeHeight,2)
	elif MFTwoToMGThreeHeight == 0:
		MFTwoToMGThree = round(MFTwoToMGThreeWidth,2)
	else:
		MFTwoToMGThree = round(math.sqrt( MFTwoToMGThreeWidth**2 + MFTwoToMGThreeHeight**2 ),2)
	MFThreeToMFFourWidth = round(abs(i['leftHand']['11'][0] - i['leftHand']['12'][0]),2)
	MFThreeToMFFourHeight = round(abs(i['leftHand']['11'][1] - i['leftHand']['12'][1]),2)
	if MFThreeToMFFourWidth == 0:
		MFThreeToMFFour = round(MFThreeToMFFourHeight,2)
	elif MFThreeToMFFourHeight == 0:
		MFThreeToMFFour = round(MFThreeToMFFourWidth,2)
	else:
		MFThreeToMFFour = round(math.sqrt( MFThreeToMFFourWidth**2 + MFThreeToMFFourHeight**2 ),2)



sampX = []
sampY = []

for i in z['body']:
	# print('\''+i+'\'', end = ' ')
	# print(z['body'][i])
	sampX.append(z['body'][i][0])
	sampY.append(abs(z['body'][i][1] - 1300))
for i in z['leftHand']:
	# print('\''+i+'\'', end = ' ')
	# print(z['leftHand'][i])
	sampX.append(z['leftHand'][i][0])
	sampY.append(abs(z['leftHand'][i][1] - 1300))
for i in z['rightHand']:
	# print('\''+i+'\'', end = ' ')
	# print( z['rightHand'][i])
	sampX.append( z['rightHand'][i][0])
	sampY.append(abs( z['rightHand'][i][1] - 1300))


newPose = {}
oldPose = {}
newFormattedPose = {}
if gotBasis:
	# Do Resizing Here
	print()
	armLength = neckToShoulder+shoulderToElbow+elbowToWrist+wristToHandWrist+HandWristToMFOne+MFOneToMFTwo+MFTwoToMGThree+MFThreeToMFFour
	print( neckToShoulder,shoulderToElbow,elbowToWrist,wristToHandWrist,HandWristToMFOne,MFOneToMFTwo,MFTwoToMGThree,MFThreeToMFFour)
	print("armLength = ",armLength)
	print()

	# Get Percentages
	neckToShoulderPercent 	= round((round(neckToShoulder,2) 		/	armLength),2)
	shoulderToElbowPercent 	= round((round(shoulderToElbow,2) 		/	armLength),2)
	elbowToWristPercent 	= round((round(elbowToWrist,2) 			/	armLength),2)
	wristToHandWristPercent = round((round(wristToHandWrist,2) 		/	armLength),2)
	HandWristToMFOnePercent = round((round(HandWristToMFOne,2) 		/	armLength),2)
	MFOneToMFTwoPercent 	= round((round(MFOneToMFTwo,2) 			/	armLength),2)
	MFTwoToMGThreePercent 	= round((round(MFTwoToMGThreeWidth,2)	/	armLength),2)
	MFThreeToMFFourPercent 	= round((round(MFThreeToMFFour,2) 		/	armLength),2)


	print(neckToShoulderPercent+shoulderToElbowPercent+elbowToWristPercent+wristToHandWristPercent+HandWristToMFOnePercent+MFOneToMFTwoPercent+MFTwoToMGThreePercent+MFThreeToMFFourPercent)
	print("=",neckToShoulderPercent,shoulderToElbowPercent,elbowToWristPercent,wristToHandWristPercent,HandWristToMFOnePercent,MFOneToMFTwoPercent,MFTwoToMGThreePercent,MFThreeToMFFourPercent)
	print()

	# Do Repositioning Here
	newNecktoShoulder 	= round((width/2) * neckToShoulderPercent,2)
	newShouldertoElbow 	= round((width/2) * shoulderToElbowPercent,2)
	newElbowtoWrist 	= round((width/2) * elbowToWristPercent,2)
	newWristtoHandWrist	= round((width/2) * wristToHandWristPercent,2)
	newHandWristToMFOne	= round((width/2) * HandWristToMFOnePercent,2)
	newMFOneToMFTwo		= round((width/2) * MFOneToMFTwoPercent,2)
	newMFTwoToMGThree	= round((width/2) * MFTwoToMGThreePercent,2)
	newMFThreeToMFFour	= round((width/2) * MFThreeToMFFourPercent,2)

	print(width)
	print(newNecktoShoulder+newShouldertoElbow+newElbowtoWrist+newWristtoHandWrist+newHandWristToMFOne+newMFOneToMFTwo+newMFTwoToMGThree+newMFThreeToMFFour)
	print("=",newNecktoShoulder,newShouldertoElbow,newElbowtoWrist,newWristtoHandWrist,newHandWristToMFOne,newMFOneToMFTwo,newMFTwoToMGThree,newMFThreeToMFFour)
	print()

	# create backups of original values
	
	oldPose = copy.deepcopy(z)
	newPose = copy.deepcopy(z)
	print(oldPose)
	print()
	print(newPose)
	print()

	# GUIDE ON WHAT TO DO
	# GET LENGTH OF SHORT BOTH X AND Y
	# RESIZE ACCORDING TO THE BASIS GET THE PERCENTAGE FIRST
	# 

	# neck
	oldPose['body']['neck']
	newPose['body']['neck'] = [width/2,height/2]
	newFormattedPose['neck'] = newPose['body']['neck']
	# neck to nose
	# x = oldPose['body']['nose']
	# y = oldPose['body']['nose']
	# h = 
	# xX = 
	# yY = 
	# hH =  
	# newPose['body']['nose'] = [width/2,height/2]
	# newFormattedPose['nose'] = newPose['body']['nose']
	# neck to midhip
	oldPose['body']['midhip']
	# neck to rightShoulder
	oldPose['body']['neck']
	oldPose['body']['rightShoulder']
	# 	rightElbow
	oldPose['body']['rightElbow']
	# 		rightWrist
	oldPose['body']['rightWrist']
	# 			rightHandHeel
	oldPose['rightHand']['0']
	# 				rightLFOne
	oldPose['rightHand']['17']
	# 					rightLFTwo
	oldPose['rightHand']['18']
	# 						rightLFThree
	oldPose['rightHand']['19']
	# 						 	rightLFFour
	oldPose['rightHand']['20']
	# 				rightRFOne
	oldPose['rightHand']['13']
	# 					rightRFTwo
	oldPose['rightHand']['14']
	# 						rightRFThree
	oldPose['rightHand']['15']
	# 						 	rightRFFour
	oldPose['rightHand']['16']
	# 				rightMFOne
	oldPose['rightHand']['9']
	# 					rightMFTwo
	oldPose['rightHand']['10']
	# 						rightMFThree
	oldPose['rightHand']['11']
	# 						 	rightMFFour
	oldPose['rightHand']['12']
	# 				rightPFOne
	oldPose['rightHand']['5']
	# 					rightPFTwo
	oldPose['rightHand']['6']
	# 						rightPFThree
	oldPose['rightHand']['7']
	# 						 	rightPFFour
	oldPose['rightHand']['8']
	# 				 rightTOne
	oldPose['rightHand']['1']
	# 					 rightTTwo
	oldPose['rightHand']['2']
	# 						 rightTThree
	oldPose['rightHand']['3']
	# 						 	rightTFour
	oldPose['rightHand']['4']
	# neck to leftShoulder
	x = oldPose['body']['leftShoulder'][0]
	y = oldPose['body']['leftShoulder'][1]
	h = neckToShoulder
	xX = oldPose['body']['neck'][0] 
	yY = oldPose['body']['neck'][1]
	hH = newNecktoShoulder
	newPose['body']['leftShoulder'] = [ (xX-x)-neckToShoulderPercent  , () ]
	newFormattedPose['leftShoulder'] = []
	# 	leftElbow
	oldPose['body']['leftElbow']
	# 		leftWrist
	oldPose['body']['leftWrist']
	# 			leftHandHeel
	oldPose['leftHand']['0']
	# 				leftLFOne
	oldPose['leftHand']['17']
	# 					leftLFTwo
	oldPose['leftHand']['18']
	# 						leftLFThree
	oldPose['leftHand']['19']
	# 							leftLFFourA
	oldPose['leftHand']['20']
	# 				leftRFOne
	oldPose['leftHand']['13']
	# 					leftRFTwo
	oldPose['leftHand']['14']
	#						leftRFThree
	oldPose['leftHand']['15']
	# 							leftRFFourA
	oldPose['leftHand']['16']
	# 				leftMFOne
	oldPose['leftHand']['9']
	# 					leftMFTwo
	oldPose['leftHand']['10']
	# 						leftLFMhree
	oldPose['leftHand']['11']
	# 							leftMFFourA
	oldPose['leftHand']['12']
	# 				leftPFOne
	oldPose['leftHand']['5']
	# 					leftPFTwo
	oldPose['leftHand']['6']
	# 						leftPFThree
	oldPose['leftHand']['7']
	# 							leftPFFour
	oldPose['leftHand']['8']
	# 				leftTOne
	oldPose['leftHand']['1']
	# 					leftTTwo
	oldPose['leftHand']['2']
	# 						leftTThree
	oldPose['leftHand']['3']
	# 							leftTFour
	oldPose['leftHand']['4']

	print(oldPose)
	print()
	print(newPose)

	# nose, neck, midHip, 
	# rightShoulder, rightElbow, rightWrist, rightHandHeel, rightLFOne, rightLFTwo, rightLFThree, rightLFFour, rightRFOne, rightRFTwo, tRFThree, rightRFFour, righMFOne, rightMFTwo, rightMFThree, rightMFFour, rightPFOne, rightPFTwo, rightPFThree, rightPFFour, rightTOne, rightTTwo, rightTThree, rightTFour
	# leftShoulder, leftElbow, leftWrist, leftHandHeel, leftLFOne, leftLFTwo, leftLFThree, leftLFFour, leftRFOne, leftRFTwo, leftRFThree, leftRFFour, leftMFOne, leftMFTwo, leftMFThree, leftMFFour, leftPFOne, leftPFTwo, leftPFThree, leftPFFour, leftTOne, leftTTwo, leftTThree, leftTFour

sampXnew = []
sampYnew = []
for i in newFormattedPose:
	sampXnew.append(newFormattedPose[i][0])
	sampYnew.append(abs(newFormattedPose[i][1] - 250))



# BEFORE RESIZING
plt.title('BEFORE')
plt.plot(sampX, sampY, 'ro')
plt.axis([650, 1250, 200, 1300])
plt.show()
# AFTER RESIZING
plt.title('AFTER')
plt.plot(sampXnew, sampYnew, 'ro')
plt.axis([0, 250, 0, 250])
plt.show()

# print("Nag Size og Position Change na!!!")