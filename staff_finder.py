# staff_finder.py

import cv2
import numpy as np

input_path = 'input/'
output_path = 'output2/'

def findStaves():
	# Read source image and convert to grayscale then binary
	src = cv2.imread(input_path + 'first.jpg')
	gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

	cv2.imwrite(output_path + 'binary.png', binary)

	# Get width and height of image
	src_width = len(binary[0])
	src_height = len(binary)

	# Find horizontal lines
	horiz_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (src_width//5, 1))
	horiz_lines = cv2.erode(binary, horiz_struct)
	horiz_lines = cv2.dilate(horiz_lines, horiz_struct)

	cv2.imwrite(output_path + 'horiz_lines.png', horiz_lines)

	# Find the y coordinates of every white pixel down the center of the horizontal lines image
	y_vals = []
	for y in range(src_height):
		if horiz_lines[y][src_width//2]:
			y_vals.append(y)

	#print(y_vals)

	# Group values to find the average y coordinate of each line
	y_coords = []
	i = 0
	while i < len(y_vals):
		temp = []
		temp.append(y_vals[i])
		while i < len(y_vals) - 1 and y_vals[i] + 1 == y_vals[i+1]:
			temp.append(y_vals[i+1])
			i = i+1
		y_coords.append(int(np.mean(temp)))
		i = i+1

	#print("\n\n")
	#print(y_coords)

	#print(len(y_coords)/10)

	# Group nearest y coordinates to find boundaries of each staff
	staves = []
	i = 0
	while i < len(y_coords):
		temp = []
		for j in range(5):
			temp.append(y_coords[i])
			i = i+1
		while i < len(y_coords) and y_coords[i] - y_coords[i-1] < y_coords[i-4] - y_coords[i-5]:
			temp = temp[1:]
			temp.append(y_coords[i])
			i = i+1
		staves.append([y_coords[i-5], y_coords[i-1]])

	#print(staves)

	# Group nearest staves to find boundaries of each grand staff
	grand_staves = []
	i = 0
	while i < len(staves):
		temp = []
		for j in range(2):
			temp.append(staves[i])
			i = i+1
		while i < len(staves) and staves[i][0] - staves[i-1][1] < staves[i-1][0] - staves[i-2][1]:
			temp = temp[1:]
			temp.append(staves[i])
			i = i+1
		grand_staves.append([staves[i-2][0], staves[i-1][1]])

	# Find the x coordinates of the rectangle around each grand staff
	staff_rects = []
	for staff in grand_staves:
		left_x = 0
		while binary[staff[0]][left_x] == 0:
			left_x = left_x + 1
		right_x = src_width-1
		while binary[staff[0]][right_x] == 0:
			right_x = right_x - 1
		staff_rects.append([ [left_x, staff[0]], [right_x, staff[1]] ])

	# Extend the y coordinates of each rectangle to include dangling notes
	for rect in staff_rects:
		left_x = rect[0][0]
		right_x = rect[1][0]
		top_y = rect[0][1]
		bot_y = rect[1][1]
		while lineContainsWhitePixel(binary, left_x, right_x, top_y):
			top_y = top_y - 1
		while lineContainsWhitePixel(binary, left_x, right_x, bot_y):
			bot_y = bot_y + 1
		rect[0][1] = top_y + 1
		rect[1][1] = bot_y - 1

	# Draw the rectangles onto a copy of the source image
	staves_img = src.copy()
	for rect in staff_rects:
		cv2.rectangle(staves_img, (rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), (0, 0, 255), 2)

	cv2.imwrite(output_path + 'grand_staves.png', staves_img)

	# Return the coordinates of the bounding rectangles
	return staff_rects


def lineContainsWhitePixel(binary, x1, x2, y):
	for x in range(x1, x2):
		if binary[y][x]:
			return True
	return False


findStaves()