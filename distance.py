from imutils import paths
import numpy as np
import imutils
import cv2
import os

KNOWN_DISTANCE_IN_CM = 150
KNOWN_WIDTH_IN_CM = 30

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

def calculate_distance():
	trainImage = "upload/200cm-2-30.jpg"
	image = cv2.imread(trainImage)
	trainImagePixel = image.shape[0]
	marker = find_marker(image)
	focalLength = (marker[1][0] * KNOWN_DISTANCE_IN_CM) / KNOWN_WIDTH_IN_CM
	list_of_distances = []
	i = 0
	for imagePath in sorted(paths.list_images("upload")):
		print(i)
		i = i +1
		image = cv2.imread(imagePath)
		if imagePath == trainImage:
			continue
		if trainImagePixel != image.shape[0]:
			continue
		marker = find_marker(image)
		meters = distance_to_camera(KNOWN_WIDTH_IN_CM, focalLength, marker[1][0])
		# print('dimantions: ', image.shape)
		# print(imagePath, 'dist in cm: ', round(meters, 0), " : " ,image.shape)
		list_of_distances.append(round(meters, 0))
	return list_of_distances

if __name__ == '__main__':
	calculate_distance()