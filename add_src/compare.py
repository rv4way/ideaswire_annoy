
import cv2
import itertools
import os

import numpy as np
np.set_printoptions(precision=2)

import openface


align = openface.AlignDlib('../model/shape_predictor_68_face_landmarks.dat')
net = openface.TorchNeuralNet('../model/nn4.small2.v1.t7')



def getRep(imgPath):

	bgrImg = cv2.imread(imgPath)

	rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

	bb = align.getLargestFaceBoundingBox(rgbImg)

	imgDim = 96
	alignedFace = align.align(imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

	rep = net.forward(alignedFace)

	return rep