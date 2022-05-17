import dlib
import cv2
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

class Lip_Detection:

    def __init__(self, param):

        self.confThreshRed = param["confThreshRed"]
        self.confThreshGreen = param["confThreshGreen"]
        self.confThreshBlue = param["confThreshBlue"]

    def createBox(self, img, points, scale=5, masked=False, cropped=True):
        if masked:
            mask = np.zeros_like(img)
            mask = cv2.fillPoly(mask, [points], (255, 255, 255))
            img = cv2.bitwise_and(img, mask)

        if cropped:
            bbox = cv2.boundingRect(points)
            x, y, w, h = bbox
            imgCrop = img[y:y + h, x:x + w]
            imgCrop = cv2.resize(imgCrop, (0, 0), None, scale, scale)
            return imgCrop
        else:
            return mask

    def run(self, img):
        img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
        imgOriginal = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(imgGray)

        # This can handle video (multiple faces) as well.
        for face in faces:
            landmarks = predictor(imgGray, face)
            myPoints = []
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                myPoints.append([x, y])

            imgLips = self.createBox(img, np.array(myPoints)[48:61], 8, masked=True, cropped=False)

            imgColorLips = np.zeros_like(imgLips)
            imgColorLips[:] = self.confThreshBlue, self.confThreshGreen, self.confThreshRed
            imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
            imgColorLips = cv2.GaussianBlur(imgColorLips, (7, 7), 10)
            imgColorLips = cv2.addWeighted(imgOriginal, 1, imgColorLips, 0.4, 0)

        return imgColorLips