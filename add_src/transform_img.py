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

def transform_image(img_path, profile_id):

	profile_path = os.path.join('../data/add_image', str(profile_id))
	if not os.path.exists(profile_path):
		os.mkdir(profile_path)
	
	img = cv2.imread(img_path)
	'''saving image as it is'''
	
	cv2.imwrite(profile_path+'/'+str(profile_id)+'.jpg', img)

	con_img = convolve_image(img)
	#print con_img
	#cv2.imshow('tete', con_img)
	#cv2.waitKey()

	cv2.imwrite(profile_path + '/' + str(profile_id) + '_' + str('con_img') + '.jpg', con_img)

	return profile_path

def affine_transform(img, profile_path, name):
	#print profile_path, name
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
	

		#cv2.imshow('AFFINE', dst)
		#cv2.waitKey()
		cv2.imwrite(profile_path + '/' + name + '_+_' + str(x_rot) + '.jpg', dst)

	x_rot = 50
	y_rot = 200
	for x in range(2):
		pts1 = np.float32([[50,50],[200,50],[50,200]])

		x_rot = x_rot - 20
		y_rot = y_rot - 20

		pts2 = np.float32([[x_rot, x_rot],[200,50],[x_rot,y_rot]])
	
		M = cv2.getAffineTransform(pts1,pts2)

		dst = cv2.warpAffine(img,M,(cols,rows))
	

		#cv2.imshow(str(('AFFINE', x)), dst)
		#cv2.waitKey()
		cv2.imwrite(profile_path + '/' + name + '_-_' + str(x_rot) + '.jpg', dst)



def convolve_image(img):

	kernel = np.array([ [0,-1,0],
                    [-1,5,-1],
                    [0,-1,0] ],np.float32)

	new_img = cv2.filter2D(img,-1,kernel)
	return new_img

def cal_rep(profile_path, profile_id):
	#print profile_id
	image_list = os.listdir(profile_path)
	for x, y in enumerate(image_list):
		img_path = os.path.join(profile_path, y)
		#print img_path
		try:
			#getting rep of the images 
			img_rep = compare.getRep(img_path)
			store_rep(img_rep, profile_id)
		except:
			print 'Error, ERROR CODE - 1001'
			pass
		
	#print 'REP WRITTEN TO DISK'

def store_rep(img_rep, profile_id):

	rep_location = '../img_rep'
	rep_file = os.path.join(rep_location, str(profile_id)) + '.pkl'
	img_rep = list(img_rep)
	

	#writing rep to pkl file
	if os.path.isfile(rep_file):
		temp_list = []
		#temp = open(rep_file, 'rb')
		with open(rep_file, "rb") as temp:
			#print temp
			temp_rep = cPickle.load(temp)
		#print len(temp_rep)
		for x in range(len(temp_rep)):
			temp_list.append(temp_rep[x])
		
		temp_list.append(img_rep)

		f = open(rep_file, 'wb')
		cPickle.dump(temp_list, f, protocol=cPickle.HIGHEST_PROTOCOL)
		f.close()
	
	#creating new pkl file for new profile id
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
	

def main_fun(img_path, profile_id):
	profile_path = transform_image(img_path, profile_id)
	#print profile_path
	
	#function for rep calculation and storing
	cal_rep(profile_path, profile_id)
	
	#function for annoy creation and updation
	ann.create_annoy()
	update_status(profile_id)
	#print "DONE"
	return "DONE"


'''
if __name__ == '__main__':
	img_path = '../rahul_05.jpg'
	main_fun(img_path, 'new_rahul')
'''