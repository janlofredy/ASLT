#Import Required modules
import sys
import cv2
import os
from sys import platform
import argparse
import math
import copy
import matplotlib.pyplot as plt
import json
import numpy
import tkinter as tk
from PIL import ImageTk, Image

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

#import OpenPose
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    if platform == "win32":
        sys.path.append(dir_path + '/openpose/build/python/openpose/Release')
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/openpose/build/x64/Release;' + dir_path + '/openpose/build/bin;'
        import pyopenpose as op
    else:
        sys.path.append('openpose/build/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print("Error importint Openpose, Make sure Openpose is compiled Properly")
    raise e

class getKeyPoints():


	def __init__(self, *args, **kwargs):
		self.args = args
		self.flags = argparse.ArgumentParser()

	def compensateSizePosition(self):
		if self.label == None:
			print('Resizing Keypoints')
		else:
			self.label['text'] = "Resizing Keypoints"
		#Create A 250x250 Bounding box to put the keypoints in for size and position compensation
		width = 250
		height = 250
		top = width/2
		right = width/2
		left = 0-(width/2)
		bottom = 0-(width/2)

		xCenter = right-(width/2)
		yCenter = top-(width/2)

		gotBasis = False
		neckToShoulder = 0
		shoulderToElbow = 0
		elbowToWrist = 0
		wristToHandWrist = 0
		HandWristToMFOne = 0
		MFOneToMFTwo = 0
		MFTwoToMGThree = 0
		MFThreeToMFFour = 0

		self.allNewPoses = []

		# Search for a frame with complete arm keypoints then get basis for changes

		# Shoulder to Elbow									2 - 3 or 5 - 6		Body to Body

		# Elbow to Wrist									3 - 4 or 6 - 7		Body to Body

		# Wrist to Hand's Wrist								4 - 0 or 7 - 0		Body to Left/Right Hand

		# Hands's Wrist to first Middle Finger				0 - 9				Left/Right Hand to Left/Right Hand

		# First Middle Finger to Second Middle Finger		9 - 10				Left/Right Hand to Left/Right Hand

		# Second Middle Finger to Third Middle Finger		10 - 11				Left/Right Hand to Left/Right Hand

		# Third Middle Finger to Fourth Middle Finger		11 - 12				Left/Right Hand to Left/Right Hand

		# Finding the percentage of the length of each part of the arm
		for i in self.keypoints:
			if 0 not in [	
							i['body']['neck'][0],i['body']['neck'][1],
							i['body']['rightShoulder'][0],i['body']['rightElbow'][0],i['body']['rightWrist'][0],i['rightHand']['0'][0],i['rightHand']['9'][0],i['rightHand']['10'][0],i['rightHand']['11'][0],i['rightHand']['12'][0],
							i['body']['rightShoulder'][1],i['body']['rightElbow'][1],i['body']['rightWrist'][1],i['rightHand']['0'][1],i['rightHand']['9'][1],i['rightHand']['10'][1],i['rightHand']['11'][1],i['rightHand']['12'][1]
						]:
				gotBasis= True
				basis = 'rightShoulder'
				neckToShoulderWidth = abs(i['body']['neck'][0] - i['body']['rightShoulder'][0])
				neckToShoulderHeight = abs(i['body']['neck'][1] - i['body']['rightShoulder'][1])
				if neckToShoulderWidth == 0:
					neckToShoulder = neckToShoulderHeight
				elif neckToShoulderWidth == 0:
					neckToShoulder = neckToShoulderWidth
				else:
					neckToShoulder = math.sqrt(neckToShoulderWidth**2 + neckToShoulderHeight**2)
				shoulderToElbowWidth = abs(i['body']['rightShoulder'][0] - i['body']['rightElbow'][0])
				shoulderToElbowHeight = abs(i['body']['rightShoulder'][1] - i['body']['rightElbow'][1])
				if shoulderToElbowWidth == 0:
					shoulderToElbow = shoulderToElbowHeight
				elif shoulderToElbowHeight == 0:
					shoulderToElbow = shoulderToElbowWidth
				else:
					shoulderToElbow = math.sqrt( shoulderToElbowHeight**2 + shoulderToElbowWidth**2 )
				elbowToWristWidth = abs(i['body']['rightElbow'][0] - i['body']['rightWrist'][0])
				elbowToWristHeight = abs(i['body']['rightElbow'][1] - i['body']['rightWrist'][1])
				if elbowToWristWidth == 0:
					elbowToWrist = elbowToWristHeight
				elif elbowToWristHeight == 0:
					elbowToWrist = elbowToWristWidth
				else:
					elbowToWrist = math.sqrt( elbowToWristWidth**2+ elbowToWristHeight**2 )
				wristToHandWristWidth = abs(i['body']['rightWrist'][0] - i['rightHand']['0'][0])
				wristToHandWristHeight = abs(i['body']['rightWrist'][1] - i['rightHand']['0'][1])
				if wristToHandWristWidth == 0:
					wristToHandWrist = wristToHandWristHeight
				elif wristToHandWristHeight == 0:
					wristToHandWrist = wristToHandWristWidth
				else:
					wristToHandWrist = math.sqrt( wristToHandWristWidth**2 + wristToHandWristHeight**2 )
				HandWristToMFOneWidth = abs(i['rightHand']['0'][0] - i['rightHand']['9'][0])
				HandWristToMFOneHeight = abs(i['rightHand']['0'][1] - i['rightHand']['9'][1])
				if HandWristToMFOneWidth == 0:
					HandWristToMFOne = HandWristToMFOneHeight
				elif HandWristToMFOneHeight == 0:
					HandWristToMFOne = HandWristToMFOneWidth
				else:
					HandWristToMFOne = math.sqrt( HandWristToMFOneWidth**2 + HandWristToMFOneHeight**2 )
				MFOneToMFTwoWidth = abs(i['rightHand']['9'][0] - i['rightHand']['10'][0])
				MFOneToMFTwoHeight = abs(i['rightHand']['9'][1] - i['rightHand']['10'][1])
				if MFOneToMFTwoWidth == 0:
					MFOneToMFTwo = MFOneToMFTwoHeight
				elif MFOneToMFTwoHeight == 0:
					MFOneToMFTwo = MFOneToMFTwoWidth
				else:
					MFOneToMFTwo = math.sqrt( MFOneToMFTwoWidth**2+ MFOneToMFTwoHeight**2 )
				MFTwoToMGThreeWidth = abs(i['rightHand']['10'][0] - i['rightHand']['11'][0])
				MFTwoToMGThreeHeight = abs(i['rightHand']['10'][1] - i['rightHand']['11'][1])
				if MFTwoToMGThreeWidth == 0:
					MFTwoToMGThree = MFTwoToMGThreeHeight
				elif MFTwoToMGThreeHeight == 0:
					MFTwoToMGThree = MFTwoToMGThreeWidth
				else:
					MFTwoToMGThree = math.sqrt( MFTwoToMGThreeWidth**2 + MFTwoToMGThreeHeight**2 )
				MFThreeToMFFourWidth = abs(i['rightHand']['11'][0] - i['rightHand']['12'][0])
				MFThreeToMFFourHeight = abs(i['rightHand']['11'][1] - i['rightHand']['12'][1])
				if MFThreeToMFFourWidth == 0:
					MFThreeToMFFour = MFThreeToMFFourHeight
				elif MFThreeToMFFourHeight == 0:
					MFThreeToMFFour = MFThreeToMFFourWidth
				else:
					MFThreeToMFFour = math.sqrt( MFThreeToMFFourWidth**2 + MFThreeToMFFourHeight**2 )


				break


			elif 0 not in 	[	
							i['body']['neck'][0],i['body']['neck'][1],
							i['body']['leftShoulder'][0],i['body']['leftElbow'][0],i['body']['leftWrist'][0],i['leftHand']['0'][0],i['leftHand']['9'][0],i['leftHand']['10'][0],i['leftHand']['11'][0],i['leftHand']['12'][0],
							i['body']['leftShoulder'][1],i['body']['leftElbow'][1],i['body']['leftWrist'][1],i['leftHand']['0'][1],i['leftHand']['9'][1],i['leftHand']['10'][1],i['leftHand']['11'][1],i['leftHand']['12'][1]
							]:
				basis = 'leftShoulder'
				gotBasis= True
				neckToShoulderWidth = abs(i['body']['neck'][0] - i['body']['leftShoulder'][0])
				neckToShoulderHeight = abs(i['body']['neck'][1] - i['body']['leftShoulder'][1])
				if neckToShoulderWidth == 0:
					neckToShoulder = neckToShoulderHeight
				elif neckToShoulderWidth == 0:
					neckToShoulder = neckToShoulderWidth
				else:
					neckToShoulder = math.sqrt(neckToShoulderWidth**2 + neckToShoulderHeight**2)
				shoulderToElbowWidth = abs(i['body']['leftShoulder'][0] - i['body']['leftElbow'][0])
				shoulderToElbowHeight = abs(i['body']['leftShoulder'][1] - i['body']['leftElbow'][1])
				if shoulderToElbowWidth == 0:
					shoulderToElbow = shoulderToElbowHeight
				elif shoulderToElbowHeight == 0:
					shoulderToElbow = shoulderToElbowWidth
				else:
					shoulderToElbow = math.sqrt( shoulderToElbowHeight**2 + shoulderToElbowWidth**2 )
				elbowToWristWidth = abs(i['body']['leftElbow'][0] - i['body']['leftWrist'][0])
				elbowToWristHeight = abs(i['body']['leftElbow'][1] - i['body']['leftWrist'][1])
				if elbowToWristWidth == 0:
					elbowToWrist = elbowToWristHeight
				elif elbowToWristHeight == 0:
					elbowToWrist = elbowToWristWidth
				else:
					elbowToWrist = math.sqrt( elbowToWristWidth**2 + elbowToWristHeight**2 )
				wristToHandWristWidth = abs(i['body']['leftWrist'][0] - i['leftHand']['0'][0])
				wristToHandWristHeight = abs(i['body']['leftWrist'][1] - i['leftHand']['0'][1])
				if wristToHandWristWidth == 0:
					wristToHandWrist = wristToHandWristHeight
				elif wristToHandWristHeight == 0:
					wristToHandWrist = wristToHandWristWidth
				else:
					wristToHandWrist = math.sqrt( wristToHandWristWidth**2 + wristToHandWristHeight**2 )
				HandWristToMFOneWidth = abs(i['leftHand']['0'][0] - i['leftHand']['9'][0])
				HandWristToMFOneHeight = abs(i['leftHand']['0'][1] - i['leftHand']['9'][1])
				if HandWristToMFOneWidth == 0:
					HandWristToMFOne = HandWristToMFOneHeight
				elif HandWristToMFOneHeight == 0:
					HandWristToMFOne = HandWristToMFOneWidth
				else:
					HandWristToMFOne = math.sqrt( HandWristToMFOneWidth**2 + HandWristToMFOneHeight**2 )
				MFOneToMFTwoWidth = abs(i['leftHand']['9'][0] - i['leftHand']['10'][0])
				MFOneToMFTwoHeight = abs(i['leftHand']['9'][1] - i['leftHand']['10'][1])
				if MFOneToMFTwoWidth == 0:
					MFOneToMFTwo = MFOneToMFTwoHeight
				elif MFOneToMFTwoHeight == 0:
					MFOneToMFTwo = MFOneToMFTwoWidth
				else:
					MFOneToMFTwo = math.sqrt( MFOneToMFTwoWidth**2 + MFOneToMFTwoHeight**2 )
				MFTwoToMGThreeWidth = abs(i['leftHand']['10'][0] - i['leftHand']['11'][0])
				MFTwoToMGThreeHeight = abs(i['leftHand']['10'][1] - i['leftHand']['11'][1])
				if MFTwoToMGThreeWidth == 0:
					MFTwoToMGThree = MFTwoToMGThreeHeight
				elif MFTwoToMGThreeHeight == 0:
					MFTwoToMGThree = MFTwoToMGThreeWidth
				else:
					MFTwoToMGThree = math.sqrt( MFTwoToMGThreeWidth**2 + MFTwoToMGThreeHeight**2 )
				MFThreeToMFFourWidth = abs(i['leftHand']['11'][0] - i['leftHand']['12'][0])
				MFThreeToMFFourHeight = abs(i['leftHand']['11'][1] - i['leftHand']['12'][1])
				if MFThreeToMFFourWidth == 0:
					MFThreeToMFFour = MFThreeToMFFourHeight
				elif MFThreeToMFFourHeight == 0:
					MFThreeToMFFour = MFThreeToMFFourWidth
				else:
					MFThreeToMFFour = math.sqrt( MFThreeToMFFourWidth**2 + MFThreeToMFFourHeight**2 )

				break

		# Resize the body pose given the ratio of lengths of the arm

		newPose = {}
		oldPose = {}
		newFormattedPose = {}
		oldFormattedPose = {}
		if gotBasis:
			# Do Resizing Here
			armLength = neckToShoulder+shoulderToElbow+elbowToWrist+wristToHandWrist+HandWristToMFOne+MFOneToMFTwo+MFTwoToMGThree+MFThreeToMFFour
			# print( neckToShoulder,shoulderToElbow,elbowToWrist,wristToHandWrist,HandWristToMFOne,MFOneToMFTwo,MFTwoToMGThree,MFThreeToMFFour)
			# print("armLength = ",armLength)

			# Get Percentages
			neckToShoulderPercent 	= round((round(neckToShoulder,2) 			/ armLength), 2)
			shoulderToElbowPercent 	= round((round(shoulderToElbow,2) 			/ armLength), 2)
			elbowToWristPercent 	= round((round(elbowToWrist,2) 			/ armLength), 2)
			wristToHandWristPercent = round((round(wristToHandWrist,2) 		/ armLength), 2)
			HandWristToMFOnePercent = round((round(HandWristToMFOne,2) 		/ armLength), 2)
			MFOneToMFTwoPercent 	= round((round(MFOneToMFTwo,2) 			/ armLength), 2)
			MFTwoToMGThreePercent 	= round((round(MFTwoToMGThreeWidth,2)		/ armLength), 2)
			MFThreeToMFFourPercent 	= round((round(MFThreeToMFFour,2) 			/ armLength), 2)


			# Test plot in matplot lib the frames
			# for z in range(len(self.keypoints)):
			# 	sampX = []
			# 	sampY = []
			# 	for i in self.keypoints[z]['body']:
			# 		print(i, end = ' ')
			# 		print(self.keypoints[z]['body'][i])
			# 		sampX.append(self.keypoints[z]['body'][i][0])
			# 		sampY.append(abs(self.keypoints[z]['body'][i][1] - 1300))
			# 	for i in self.keypoints[z]['leftHand']:
			# 		print(i, end = ' ')
			# 		print(self.keypoints[z]['leftHand'][i])
			# 		sampX.append(self.keypoints[z]['leftHand'][i][0])
			# 		sampY.append(abs(self.keypoints[z]['leftHand'][i][1] - 1300))
			# 	for i in self.keypoints[z]['rightHand']:
			# 		print(i, end = ' ')
			# 		print(self.keypoints[z]['rightHand'][i])
			# 		sampX.append(self.keypoints[z]['rightHand'][i][0])
			# 		sampY.append(abs(self.keypoints[z]['rightHand'][i][1] - 1300))
			# 	plt.title('BEFORE')
			# 	plt.plot(sampX, sampY, 'ro')
			# 	plt.axis([0, 2000, 0, 2000])
			# 	plt.show()

			for i in self.keypoints:
				oldPose = copy.deepcopy(i)
				newPose = copy.deepcopy(i)
				# Change format of Dataset
				oldFormattedPose['neck'] = oldPose['body']['neck']
				# neck to nose
				oldFormattedPose['nose'] = oldPose['body']['nose']
				# neck to midhip
				oldFormattedPose['midHip'] = oldPose['body']['midhip']
				# neck to rightShoulder
				oldFormattedPose['rightShoulder'] = oldPose['body']['rightShoulder']
				# 	rightElbow
				oldFormattedPose['rightElbow'] = oldPose['body']['rightElbow']
				# 		rightWrist
				oldFormattedPose['rightWrist'] = oldPose['body']['rightWrist']
				# 			rightHandHeel
				oldFormattedPose['rightHandHeel'] = oldPose['rightHand']['0']
				# 				rightLFOne
				oldFormattedPose['rightLFOne'] = oldPose['rightHand']['17']
				# 					rightLFTwo
				oldFormattedPose['rightLFTwo'] = oldPose['rightHand']['18']
				# 						rightLFThree
				oldFormattedPose['rightLFThree'] = oldPose['rightHand']['19']
				# 						 	rightLFFour
				oldFormattedPose['rightLFFour'] = oldPose['rightHand']['20']
				# 				rightRFOne
				oldFormattedPose['rightRFOne'] = oldPose['rightHand']['13']
				# 					rightRFTwo
				oldFormattedPose['rightRFTwo'] = oldPose['rightHand']['14']
				# 						rightRFThree
				oldFormattedPose['rightRFThree'] = oldPose['rightHand']['15']
				# 						 	rightRFFour
				oldFormattedPose['rightRFFour'] = oldPose['rightHand']['16']
				# 				rightMFOne
				oldFormattedPose['rightMFOne'] = oldPose['rightHand']['9']
				# 					rightMFTwo
				oldFormattedPose['rightMFTwo'] = oldPose['rightHand']['10']
				# 						rightMFThree
				oldFormattedPose['rightMFThree'] = oldPose['rightHand']['11']
				# 						 	rightMFFour
				oldFormattedPose['rightMFFour'] = oldPose['rightHand']['12']
				# 				rightPFOne
				oldFormattedPose['rightPFOne'] = oldPose['rightHand']['5']
				# 					rightPFTwo
				oldFormattedPose['rightPFTwo'] = oldPose['rightHand']['6']
				# 						rightPFThree
				oldFormattedPose['rightPFThree'] = oldPose['rightHand']['7']
				# 						 	rightPFFour
				oldFormattedPose['rightPFFour'] = oldPose['rightHand']['8']
				# 				 rightTOne
				oldFormattedPose['rightTOne'] = oldPose['rightHand']['1']
				# 					 rightTTwo
				oldFormattedPose['rightTTwo'] = oldPose['rightHand']['2']
				# 						 rightTThree
				oldFormattedPose['rightTThree'] = oldPose['rightHand']['3']
				# 						 	rightTFour
				oldFormattedPose['rightTFour'] = oldPose['rightHand']['4']
				# neck to leftShoulder
				oldFormattedPose['leftShoulder'] = oldPose['body']['leftShoulder']
				# 	leftElbow
				oldFormattedPose['leftElbow'] = oldPose['body']['leftElbow']
				# 		leftWrist
				oldFormattedPose['leftWrist'] = oldPose['body']['leftWrist']
				# 			leftHandHeel
				oldFormattedPose['leftHandHeel'] = oldPose['leftHand']['0']
				# 				leftLFOne
				oldFormattedPose['leftLFOne'] = oldPose['leftHand']['17']
				# 					leftLFTwo
				oldFormattedPose['leftLFTwo'] = oldPose['leftHand']['18']
				# 						leftLFThree
				oldFormattedPose['leftLFThree'] = oldPose['leftHand']['19']
				# 							leftLFFour
				oldFormattedPose['leftLFFour'] = oldPose['leftHand']['20']
				# 				leftRFOne
				oldFormattedPose['leftRFOne'] = oldPose['leftHand']['13']
				# 					leftRFTwo
				oldFormattedPose['leftRFTwo'] = oldPose['leftHand']['14']
				#						leftRFThree
				oldFormattedPose['leftRFThree'] = oldPose['leftHand']['15']
				# 							leftRFFour
				oldFormattedPose['leftRFFour'] = oldPose['leftHand']['16']
				# 				leftMFOne
				oldFormattedPose['leftMFOne'] = oldPose['leftHand']['9']
				# 					leftMFTwo
				oldFormattedPose['leftMFTwo'] = oldPose['leftHand']['10']
				# 						leftMFThree
				oldFormattedPose['leftMFThree'] = oldPose['leftHand']['11']
				# 							leftMFFour
				oldFormattedPose['leftMFFour'] = oldPose['leftHand']['12']
				# 				leftPFOne
				oldFormattedPose['leftPFOne'] = oldPose['leftHand']['5']
				# 					leftPFTwo
				oldFormattedPose['leftPFTwo'] = oldPose['leftHand']['6']
				# 						leftPFThree
				oldFormattedPose['leftPFThree'] = oldPose['leftHand']['7']
				# 							leftPFFour
				oldFormattedPose['leftPFFour'] = oldPose['leftHand']['8']
				# 				leftTOne
				oldFormattedPose['leftTOne'] = oldPose['leftHand']['1']
				# 					leftTTwo
				oldFormattedPose['leftTTwo'] = oldPose['leftHand']['2']
				# 						leftTThree
				oldFormattedPose['leftTThree'] = oldPose['leftHand']['3']
				# 							leftTFour
				oldFormattedPose['leftTFour'] = oldPose['leftHand']['4']

				# Do Repositioning Here
				reference = oldFormattedPose['neck']
				xR = reference[0]
				yR = reference[1]
				newFormattedPose['neck'] = [0, 0]
				# GET CHANGE RATE/PERCENTAGE
				newNecktoShoulder 	= round((width/2) * neckToShoulderPercent,2)
				changePercent = newNecktoShoulder/neckToShoulder

				# MOVE ALL POINTS EXCEPT NECK AND SELECTED SHOULDER
				for i,j in oldFormattedPose.items():
					# if i not in ['neck', shouldSelected]:
					# 	print(i, j)
					if i != 'neck':
						# print(i, j)
						newX = 0 + ( xR - j[0] ) * changePercent
						newY = 0 + ( yR - j[1] ) * changePercent
						newFormattedPose[i] = [newX, newY]
				# print("leftTFour",newFormattedPose['leftTFour'])
				# print('allNewPoses TYPE: ', type(self.allNewPoses))
				# print('newFormattedPose TYPE:', type(newFormattedPose))
				self.allNewPoses.append(copy.deepcopy(newFormattedPose))
				# print(len(self.allNewPoses))

			# Test Plot for the Pose befor Size and Position Compensation
				# sampX = []
				# sampY = []
				# for k,v in oldFormattedPose.items():
				# 	sampX.append(v[0])
				# 	sampY.append(v[1])
				# plt.title('BEFORE')
				# plt.plot(sampX, sampY, 'ro')
				# plt.axis([0, 2000, 0, 2000])
				# plt.show()

			# Test Plot for the Pose after Size and Position Compensation
				# sampXnew = []
				# sampYnew = []
				# for k,v in newFormattedPose.items():
				# 	# print(k,v)
				# 	sampXnew.append(v[0])
				# 	sampYnew.append(v[1])
				# plt.title('AFTER')
				# plt.plot(sampXnew, sampYnew, 'ro')
				# plt.axis([0-width/2, 0+width/2, 0-width/2, 0+width/2])
				# plt.show()

			self.keypoints = self.allNewPoses
		if self.label == None:
			print('Finished Resizing!')
		else:
			self.label['text'] = "Finished Resizing!"

	def removeUselessFrames(self):
		if self.label == None:
			print('Removing Duplicate Frames...')
		else:
			self.label['text'] = "Removing Duplicate Frames..."
		# print("Removing Duplicate Frames...")
		numFrames = len(self.keypoints)
		if self.label == None:
			print('Total Frames:', numFrames)
		else:
			self.label['text'] = 'Total Frames:', numFrames
		framesToRemove = []
		framesRemoved = []
		newFrames = []
		for i in range(numFrames-1):
			currentFrame = self.keypoints[i]
			nextFrame = self.keypoints[i+1]
			difX = 0
			difY = 0
			for k,v in currentFrame.items():
				difX+=abs(v[0]-nextFrame[k][0])
				difY+=abs(v[1]-nextFrame[k][1])
				# print(v[0], end=" - ")
				# print(nextFrame[k][0])
				# print(v[1], end=" - ")
				# print(nextFrame[k][1])
			# print(difX, difY)
			# print()
			if difY+difX<50:
				framesToRemove.append(i+1)
			# print(len(frame.keys()))
			# for k,v in frame.items():
			# 	print(k)
		for i in range(numFrames):
			if i not in framesToRemove:
				newFrames.append(self.keypoints[i])
			else:
				framesRemoved.append(self.keypoints[i])
		self.keypoints = newFrames
		numFrames = len(self.keypoints)
		if self.label == None:
			print("Finished Discarding Duplicates.", numFrames, "Frames now remaining.")
		else:
			self.label['text'] = "Finished Discarding Duplicates.", numFrames, "Frames now remaining."

	def learn(self, videoLocation, showDisplay=True, label = None,vFrame=None, scrSize=None):
		self.label = label
		self.vFrame = vFrame
		self.flags = argparse.ArgumentParser()
		self.flags.add_argument("--video", default = videoLocation, help="Set the video")
		self.flags.add_argument("--no_display", default = not(showDisplay), help="Set to True to Disable Display")		
		self.args = self.flags.parse_known_args()

		self.params = dict()
		self.params["model_folder"] = "openpose/models/"
		self.params["hand"] = True
		self.params["number_people_max"] = 1

		for i in range(0, len(self.args[1])):
			self.curr_item = self.args[1][i]
			if i != len(self.args[1])-1: next_item = args[1][i+1]
			else: next_item = "1"
			if "--" in curr_item and "--" in next_item:
				key = curr_item.replace('-','')
				if key not in self.params: self.params[key] = "1"
			elif "--" in curr_item and "--" not in next_item:
				key = curr_item.replace('-','')
				if key not in self.params: self.params[key] = next_item


		self.opWrapper = op.WrapperPython()
		self.opWrapper.configure(self.params)
		self.opWrapper.start()
		self.keypoints = []
		self.keypointsUnprocessed = []
		self.posedVideo = []
		videoToProcess = cv2.VideoCapture(self.args[0].video)
		if self.label == None:
			print('Processing Video(Collecting Keypoints)... \nPlease Wait')
		else:
			self.label['text'] = "Processing Video(Collecting Keypoints)... Please Wait"
		while(videoToProcess.isOpened()):
			keys = {"body":[], "rightHand":[], "leftHand":[]}
			datum = op.Datum()
			ret, frame = videoToProcess.read()
			# print("frame======"+str(frame))
			# print("RET====="+str(ret))
			if type(frame) == type(None):
				break
			datum.cvInputData = frame
			self.opWrapper.emplaceAndPop([datum])

			# print("Body keypoints: \n" + str(datum.handKeypoints[1]))
			keys["body"] = {
				"nose" :			[datum.poseKeypoints[0][0][0],	datum.poseKeypoints[0][0][1]],
				"neck" :			[datum.poseKeypoints[0][1][0],	datum.poseKeypoints[0][1][1]],
				"midhip" :			[datum.poseKeypoints[0][8][0],	datum.poseKeypoints[0][8][1]],
				"rightShoulder" :	[datum.poseKeypoints[0][2][0],	datum.poseKeypoints[0][2][1]],
				"rightElbow" :		[datum.poseKeypoints[0][3][0],	datum.poseKeypoints[0][3][1]],
				"rightWrist" :		[datum.poseKeypoints[0][4][0],	datum.poseKeypoints[0][4][1]],
				"leftShoulder" :	[datum.poseKeypoints[0][5][0],	datum.poseKeypoints[0][5][1]],
				"leftElbow" :		[datum.poseKeypoints[0][6][0],	datum.poseKeypoints[0][6][1]],
				"leftWrist" :		[datum.poseKeypoints[0][7][0],	datum.poseKeypoints[0][7][1]],
				}
			keys["leftHand"] = {
				"0" : [datum.handKeypoints[0][0][0][0],datum.handKeypoints[0][0][0][1]],
				"1" : [datum.handKeypoints[0][0][1][0],datum.handKeypoints[0][0][1][1]],
				"2" : [datum.handKeypoints[0][0][2][0],datum.handKeypoints[0][0][2][1]],
				"3" : [datum.handKeypoints[0][0][3][0],datum.handKeypoints[0][0][3][1]],
				"4" : [datum.handKeypoints[0][0][4][0],datum.handKeypoints[0][0][4][1]],
				"5" : [datum.handKeypoints[0][0][5][0],datum.handKeypoints[0][0][5][1]],
				"6" : [datum.handKeypoints[0][0][6][0],datum.handKeypoints[0][0][6][1]],
				"7" : [datum.handKeypoints[0][0][7][0],datum.handKeypoints[0][0][7][1]],
				"8" : [datum.handKeypoints[0][0][8][0],datum.handKeypoints[0][0][8][1]],
				"9" : [datum.handKeypoints[0][0][9][0],datum.handKeypoints[0][0][9][1]],
				"10" : [datum.handKeypoints[0][0][10][0],datum.handKeypoints[0][0][10][1]],
				"11" : [datum.handKeypoints[0][0][11][0],datum.handKeypoints[0][0][11][1]],
				"12" : [datum.handKeypoints[0][0][12][0],datum.handKeypoints[0][0][12][1]],
				"13" : [datum.handKeypoints[0][0][13][0],datum.handKeypoints[0][0][13][1]],
				"14" : [datum.handKeypoints[0][0][14][0],datum.handKeypoints[0][0][14][1]],
				"15" : [datum.handKeypoints[0][0][15][0],datum.handKeypoints[0][0][15][1]],
				"16" : [datum.handKeypoints[0][0][16][0],datum.handKeypoints[0][0][16][1]],
				"17" : [datum.handKeypoints[0][0][17][0],datum.handKeypoints[0][0][17][1]],
				"18" : [datum.handKeypoints[0][0][18][0],datum.handKeypoints[0][0][18][1]],
				"19" : [datum.handKeypoints[0][0][19][0],datum.handKeypoints[0][0][19][1]],
				"20" : [datum.handKeypoints[0][0][20][0],datum.handKeypoints[0][0][20][1]]
			}

			keys["rightHand"] = {
				"0" : [datum.handKeypoints[1][0][0][0],datum.handKeypoints[1][0][0][1]],
				"1" : [datum.handKeypoints[1][0][1][0],datum.handKeypoints[1][0][1][1]],
				"2" : [datum.handKeypoints[1][0][2][0],datum.handKeypoints[1][0][2][1]],
				"3" : [datum.handKeypoints[1][0][3][0],datum.handKeypoints[1][0][3][1]],
				"4" : [datum.handKeypoints[1][0][4][0],datum.handKeypoints[1][0][4][1]],
				"5" : [datum.handKeypoints[1][0][5][0],datum.handKeypoints[1][0][5][1]],
				"6" : [datum.handKeypoints[1][0][6][0],datum.handKeypoints[1][0][6][1]],
				"7" : [datum.handKeypoints[1][0][7][0],datum.handKeypoints[1][0][7][1]],
				"8" : [datum.handKeypoints[1][0][8][0],datum.handKeypoints[1][0][8][1]],
				"9" : [datum.handKeypoints[1][0][9][0],datum.handKeypoints[1][0][9][1]],
				"10" : [datum.handKeypoints[1][0][10][0],datum.handKeypoints[1][0][10][1]],
				"11" : [datum.handKeypoints[1][0][11][0],datum.handKeypoints[1][0][11][1]],
				"12" : [datum.handKeypoints[1][0][12][0],datum.handKeypoints[1][0][12][1]],
				"13" : [datum.handKeypoints[1][0][13][0],datum.handKeypoints[1][0][13][1]],
				"14" : [datum.handKeypoints[1][0][14][0],datum.handKeypoints[1][0][14][1]],
				"15" : [datum.handKeypoints[1][0][15][0],datum.handKeypoints[1][0][15][1]],
				"16" : [datum.handKeypoints[1][0][16][0],datum.handKeypoints[1][0][16][1]],
				"17" : [datum.handKeypoints[1][0][17][0],datum.handKeypoints[1][0][17][1]],
				"18" : [datum.handKeypoints[1][0][18][0],datum.handKeypoints[1][0][18][1]],
				"19" : [datum.handKeypoints[1][0][19][0],datum.handKeypoints[1][0][19][1]],
				"20" : [datum.handKeypoints[1][0][20][0],datum.handKeypoints[1][0][20][1]]
			}

			self.keypoints.append(keys),
			self.keypointsUnprocessed.append({"Body":datum.poseKeypoints,"Left Hand": datum.handKeypoints[0],"Right Hand":datum.handKeypoints[1]})
			self.posedVideo.append(datum.cvOutputData)
			if not self.args[0].no_display:
				cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", datum.cvOutputData)
				key = cv2.waitKey(15)
				if key == 27: break

			if self.vFrame != None:
				try:
					frame = datum.cvOutputData
					cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
					img = Image.fromarray(cv2image)
					imgtk = ImageTk.PhotoImage(img.resize((scrSize.winfo_width(),scrSize.winfo_height())))
					self.vFrame.imgtk = imgtk
					self.vFrame.configure(image=imgtk)
					key = cv2.waitKey(15)
					if key == 27: break
				except Exception as e:
					raise
		if self.label == None:
			print('Finished Processing')
		else:
			self.label['text'] = 'Finished Processing'
		self.compensateSizePosition()
		self.removeUselessFrames()
		# return self.keypoints

	def writeJSON(self,word):
		f = open("dataset.json",'r')
		for line in f:
			strJSON = line
		f.close()
		dataset = json.loads(strJSON)
		if word.lower() not in dataset.keys():
			dataset[word.lower()] = [self.keypoints]
		else:
			dataset[word.lower()].append(self.keypoints)

		datasetString = json.dumps(dataset, cls=MyEncoder)

		f = open('dataset.json','w')
		f.write(datasetString)
		f.close()

	def getPosedVideo(self):
		return self.posedVideo

	def getKeyPoints(self):
		return self.keypoints
