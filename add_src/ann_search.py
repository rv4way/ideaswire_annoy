import os
import numpy as np
import pandas as pd
import cPickle
import compare
from annoy import AnnoyIndex
import cv2
from collections import Counter


def search_img(img_path):

	face = compare.face_dlib(img_path)
	if face:
		
		search_rep = compare.getSearchRep(img_path)
		search_rep_test = list(search_rep)

		ann_location = '../annoy/face_module.ann'

		t = AnnoyIndex(128, metric = 'eucledian')
		t.load(ann_location)
		n = t.get_nns_by_vector(search_rep_test, 20, -1, True)
		ann_rep = n[0]
		dis_rep = n[1]
		#print ann_rep
		#print dis_rep
		response, top1_dist, top2_dist = response_logic(ann_rep, dis_rep)
		print response, top1_dist, top2_dist
		stat = 1
		return response, stat
	
	else :
		response = "FACE NOT FOUND"
		stat = 0
		return response, stat


def response_logic(ann_rep, dis_rep):
	
	id_identifyied_1, id_identifyied_2, top1_dist, top2_dist = find_top(ann_rep, dis_rep)
	response =[]
	#print id_identifyied_1, id_identifyied_2, top1_dist, top2_dist

	if top1_dist < float(0.2) or top1_dist == float(0.2):
		response.append(id_identifyied_1)
	elif top1_dist > float(0.9):
		#print response
		return response, top1_dist, top2_dist
	else:
		div_dist = top2_dist/top1_dist
		#print div_dist
		if div_dist < float(1.7):
			response.append(id_identifyied_1)
			response.append(id_identifyied_2)
		elif top1_dist < float(0.5):
			response.append(id_identifyied_1)

	#print response, top1_dist, top2_dist
	return response, top1_dist, top2_dist
	#print response
	#return response


def find_top(ann_rep, dis_rep):

	label_id = '../annoy/label_id.csv'

	profile = []
	label_data = pd.read_csv(label_id, sep = ',', header = None)
	label_data = np.asarray(label_data)

	for x, y in enumerate(ann_rep):
		temp = (label_data[y])[1]
		profile.append(temp)

	top_1 = profile[0]
	top1_dist = dis_rep[0]
	for x, y in enumerate(profile):
		if y == profile[x+1]:
			pass
		elif y != profile[x+1]:
			top_2 = profile[x+1]
			top2_dist = dis_rep[x+1]
			break

	return top_1, top_2, top1_dist, top2_dist