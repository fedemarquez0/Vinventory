import cv2
from pyzbar.pyzbar import decode

def bar_code_scanner():
	cap = cv2.VideoCapture(0)
	cap.set (3, 640)
	cap.set (4, 480)

	while True:
		success, frame = cap.read()

		for code in decode(frame):
			codigo = code.data.decode('utf—8')
			# print("El codigo de barras es: " + codigo)
			return codigo

		cv2.imshow('Escaner codigo de barras',frame)
		cv2.waitKey(1)