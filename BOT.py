# BOT: RUNESCAPE OLD SCHOOL
# Matheus Teixeira Alves

import cv2
import numpy as np 
from mss import mss
from PIL import Image
import matplotlib.pyplot as plt
from pynput.mouse import Button, Controller
import time

mouse = Controller()

bbox = {'top': 25, 'left': 1, 'width': 515, 'height': 345}
sct = mss()

template = cv2.imread('template.jpg', 0)
template2 = cv2.imread('name.jpg', 0)

w1, h1 = template.shape[::-1]
w2, h2 = template2.shape[::-1]
cX = 0
cY = 0

t_end = time.time() + 60*1
while time.time() < t_end:
	sct_img = sct.grab(bbox)
	output = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGR2GRAY)

	res = cv2.matchTemplate(output, template, cv2.TM_CCOEFF_NORMED)
	res2 = cv2.matchTemplate(output, template2, cv2.TM_CCOEFF_NORMED)

	threshold = 0.4
	threshold2 = 0.69
	loc = np.where(res >= threshold)
	loc2 = np.where(res2 >= threshold2)

	identificou = False;
	for pt in zip(*loc[::-1]):
		if pt is not None:
			identificou = True
			cX = int(pt[0]+w1/2)
			cY = int(pt[1]+h1/2)
		cv2.rectangle(output, pt, (pt[0]+w1, pt[1]+h1), (0, 255, 0), 2)

	em_combate = False
	for pt in zip(*loc2[::-1]):
		if pt is not None:
			em_combate = True 
		cv2.rectangle(output, pt, (pt[0]+w2, pt[1]+h2), (0, 255, 255), 2)

	if em_combate:
		print("Em combate.")
	else:
		print("Fora de combate.")
		if identificou:
			mouse.position = (cX, cY)
			mouse.click(Button.left, 1)


	cv2.imshow('screen', output)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
		