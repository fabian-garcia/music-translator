# read_notes.py

import cv2
import numpy as np
import copy

input_path = 'input/'
output_path = 'output/'

def removeLines():
	src = cv2.imread(input_path + 'first.jpg')
	gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

	#bw = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
	ret, bw = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

	sq_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
	bw = cv2.erode(bw, sq_struct)
	bw = cv2.dilate(bw, sq_struct)

	horiz = copy.copy(bw)
	verti = copy.copy(bw)

	horiz_size = len(horiz) // 80
	horiz_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))

	horiz = cv2.erode(horiz, horiz_struct)
	horiz = cv2.dilate(horiz, horiz_struct)


	# # perform a vertical erosion and dilation on horizontal image
	# ###############################################
	# verti_size = len(horiz[0]) // 200
	# verti_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verti_size))

	# horiz = cv2.erode(horiz, verti_struct)
	# horiz = cv2.dilate(horiz, verti_struct)
	# ################################################


	# verti_size = len(verti[0]) // 200
	# verti_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verti_size))

	# verti = cv2.erode(verti, verti_struct)
	# verti = cv2.dilate(verti, verti_struct)

	# # new_img = bw - horiz

	# cv2.imwrite(output_path + 'horiz.png', horiz)
	# cv2.imwrite(output_path + 'verti.png', verti)
	# # cv2.imwrite(output_path + 'new.png', new_img)

	ex = bw.copy()

	for x in range(len(bw[0])):
		for y in range(len(bw)):
			if horiz[y][x]:
				if not (bw[y-1][x] and bw[y-2][x]) or not (bw[y+1][x] and bw[y+2][x]):
					ex[y][x] = 0

	cv2.imwrite(output_path + 'bw.png', bw)

	contours = cv2.findContours(ex, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	new_src = src.copy()

	# cv2.drawContours(new_src, contours[1], -1, (0, 0, 255), 3)

	# for each contour obtained, produce an image of the contour to erode and dilate to remove vertical lines
	# then ovelay a bounding rectangle to what is left and save into the image
	for contour in contours[1]:
		x, y, w, h = cv2.boundingRect(contour)
		horiz_struct = cv2.getStructuringElement(cv2.MORPH_RECT, (10 , 1))

		cnt_img = ex[y:y+h, x:x+w]

		cnt_img = cv2.erode(cnt_img, horiz_struct)
		cnt_img = cv2.dilate(cnt_img, horiz_struct)

		new_contours = cv2.findContours(cnt_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		for nc in new_contours[1]:
			nx, ny, nw, nh = cv2.boundingRect(nc)

			cv2.rectangle(new_src, (x+nx, y+ny), (x+nx+nw, y+ny+nh), (0, 0, 255), 2)

	# for c in contours[1]:
	# 	x, y, w, h = cv2.boundingRect(c)
	# 	cv2.rectangle(new_src, (x, y), (x+w, y+h), (0, 0, 255), 2)

	cv2.imwrite(output_path + 'contours.png', new_src)


removeLines()
