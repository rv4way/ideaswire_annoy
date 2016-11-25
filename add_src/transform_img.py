import os
import cv2
import numpy as np
import pandas as pd
#from scipy.misc import imresize
#from pylab import array, plot, show, axis, arange, figure, uint8 
import random
from scipy import ndimage
import scipy
import compare
import cPickle
import update_annoy as ann

def transform_image(img, profile_id):

	img_rep = compare.getSearchRep(img)
	store_rep(img_rep, profile_id)
	con_img = convolve_image(img)
	img_rep = compare.getSearchRep(con_img)
	store_rep(img_rep, profile_id)
	affine_transform(img, profile_id)

	ann.create_annoy()
	update_status(profile_id)
	#print "DONE"
	return "DONE"

def affine_transform(img, profile_id):
	rows,cols,ch = img.shape

	x_rot = 50
	y_rot = 200
	for x in range(2):
		pts1 = np.float32([[50,50],[200,50],[50,200]])

		x_rot = x_rot + 10
		y_rot = y_rot + 10

		pts2 = np.float32([[x_rot, x_rot],[200,50],[x_rot,y_rot]])	
		M = cv2.getAffineTransform(pts1,pts2)
		dst = cv2.warpAffine(img,M,(cols,rows))
		
		img_rep = compare.getSearchRep(dst)
		store_rep(img_rep, profile_id)

	x_rot = 50
	y_rot = 200
	for x in range(2):
		pts1 = np.float32([[50,50],[200,50],[50,200]])

		x_rot = x_rot - 10
		y_rot = y_rot - 10

		pts2 = np.float32([[x_rot, x_rot],[200,50],[x_rot,y_rot]])	
		M = cv2.getAffineTransform(pts1,pts2)
		dst = cv2.warpAffine(img,M,(cols,rows))

		img_rep = compare.getSearchRep(dst)
		store_rep(img_rep, profile_id)

def convolve_image(img):

	kernel = np.array([ [0,-1,0],
                    [-1,5,-1],
                    [0,-1,0] ],np.float32)

	new_img = cv2.filter2D(img,-1,kernel)
	return new_img

def store_rep(img_rep, profile_id):

	rep_location = '../img_rep'
	rep_file = os.path.join(rep_location, str(profile_id)) + '.pkl'
	img_rep = list(img_rep)

	if os.path.isfile(rep_file):
		temp_list = []
		with open(rep_file, "rb") as temp:
			temp_rep = cPickle.load(temp)
		for x in range(len(temp_rep)):
			temp_list.append(temp_rep[x])
		
		temp_list.append(img_rep)

		f = open(rep_file, 'wb')
		cPickle.dump(temp_list, f, protocol=cPickle.HIGHEST_PROTOCOL)
		f.close()
	else:
		f = open(rep_file, 'wb')
		#print [img_rep]
		cPickle.dump([img_rep], f, protocol=cPickle.HIGHEST_PROTOCOL)
		f.close()

def update_status(profile_id):

	'''updating status file of the id'''
	status_path = '../status.csv'
	status_file = pd.read_csv(status_path, sep = ',', header = None)
	status_file = np.asarray(status_file)
	if profile_id in status_file:
		pass
	else:
		temp_status_file = open(status_path, 'a')
		temp_status_file.write(str(profile_id))
		temp_status_file.write('\n')
		temp_status_file.close()
		#print '\t\tSTATUS UPDATED'