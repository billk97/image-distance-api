from imutils import paths
import numpy as np
import imutils
import cv2
import os

# https://math.stackexchange.com/questions/2993190/need-a-simple-equation-for-distance-from-camera-for-an-object-of-known-size
# https://zone.biblio.laurentian.ca/bitstream/10219/2458/1/Peyman%20Alizadeh%20MSc.%20Thesis%20Corrected_2_2.pdf
# https://medium.com/@saikanamjoaddar/measuring-distance-from-an-object-using-one-camera-fee163da1cd

def find_marker(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 125)
	cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	return (knownWidth * focalLength) / perWidth


KNOWN_DISTANCE_IN_CM = 450
KNOWN_WIDTH_IN_CM = 60

trainImage = "images/450cm-1-60-ab.jpg"
image = cv2.imread(trainImage)
print('dimantions: ', image.shape)
trainImagePixel = image.shape[0]
# 35.96/image.shape[0] -
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE_IN_CM) / KNOWN_WIDTH_IN_CM
print('trainig :', trainImage)
print('focalLength', focalLength )

for imagePath in sorted(paths.list_images("images")):
	image = cv2.imread(imagePath)
	if trainImagePixel != image.shape[0]:
		continue
	marker = find_marker(image)
	meters = distance_to_camera(KNOWN_WIDTH_IN_CM, focalLength, marker[1][0])
	#print('dimantions: ', image.shape)
	print(imagePath, 'dist in cm: ', round(meters, 0), " : " ,image.shape)

	box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	cv2.putText(image, "%.2fm" % meters , (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
	dim = (500, 800)
	recized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	cv2.imshow("image", recized)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.waitKey(1)