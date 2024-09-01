import numpy as np
import cv2

myVideo = cv2.VideoCapture("../Video Database/Hello/ASL_Hello.mp4")
myImage = cv2.imread("../Video Database/COCO_val2014_000000000241.jpg")


# print(myImage[0])
# print(myVideo)

# cv2.imshow("IMAGE",myImage)
# cv2.imshow("IMAGE",myImage)

while(myVideo.isOpened()):
	ret, frame = myVideo.read()
	cv2.imshow("frame",frame)
	if cv2.waitKey(25)  & 0xFF == ord('q'):
		break;
cv2.waitKey(0)
cv2.destroyAllWindows()