# read_notes.py

import cv2
import numpy as np
import copy

input_path = 'input/'
output_path = 'output/'

def removeLines():
	src = cv2.imread(input_path + 'first.jpg')

	gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

	bw = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

	horiz = copy.copy(bw)
	verti = copy.copy(bw)

	print(len(horiz), len(horiz[0]))


	horiz_size = len(horiz) // 80
	horiz_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (horiz_size, 1))

	horiz = cv2.erode(horiz, horiz_struct)
	horiz = cv2.dilate(horiz, horiz_struct)


	verti_size = len(horiz[0]) // 200
	verti_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verti_size))

	verti = cv2.erode(verti, verti_struct)
	verti = cv2.dilate(verti, verti_struct)

	new_img = bw - horiz

	cv2.imwrite(output_path + 'horiz.png', horiz)
	cv2.imwrite(output_path + 'verti.png', verti)
	cv2.imwrite(output_path + 'new.png', new_img)



	for x in range(len(bw[0])):
		for y in range(len(bw)):
			if horiz[y][x] and not bw[y+1][x] and not bw[y-1][x]:
				bw[y][x] = 0

	cv2.imwrite(output_path + 'ex.png', bw)




removeLines()
