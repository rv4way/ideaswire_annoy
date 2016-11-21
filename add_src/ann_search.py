import os
import numpy as np
import pandas as pd
import cPickle
import compare
from annoy import AnnoyIndex


def search_img(img_path):
	
	#calculation rep of the image
	search_rep = compare.getRep(img_path)
	search_rep_test = list(search_rep)
	ann_location = '../annoy/face_module.ann'

	t = AnnoyIndex(128, metric = 'eucledian')
	t.load(ann_location)
	n = t.get_nns_by_vector(search_rep_test, 10, -1, True)
	ann_rep = n[0]
	dis_rep = n[1]
	#print ann_rep
	#print dis_rep
	response, top1_dist, top2_dist = response_logic(ann_rep, dis_rep)
	print response, top1_dist, top2_dist
	return response

def annoy_distance(ann_rep, dis_rep):

	label_id = '../annoy/label_id.csv'

	label_data = pd.read_csv(label_id, sep = ',', header = None)
	label_data = np.asarray(label_data)

	print ann_rep
	print dis_rep
	top1 = ann_rep[0]
	top2 = ann_rep[1]

	top1_dist = dis_rep[0]
	top2_dist = dis_rep[1]

	response = []
	distance = []
	if top1 == top2-1 or top1 == top2+1:
		top1_id = ((str(str(label_data[top1]).split(','))).split("'"))[1]
		top2_id = ((str(str(label_data[top2]).split(','))).split("'"))[1]
		print top1_id, top2_id
		if top1_id == top2_id:
			#response.append(top1_id)
			#response.append(top2_id)

			#distance.append(top1_dist)
			#distance.append(top2_dist)

			#print 'RESP', response
			#print 'DIST', distance
			top2 = ann_rep[2]
			top2_id = ((str(str(label_data[top2]).split(','))).split("'"))[1]
			print top2_id




def response_logic(ann_rep, dis_rep):	

	rep_result_list = {}
	temp_rep_list_temp = []

	response =[]

	label_id = '../annoy/label_id.csv'

	top1_dist = float(dis_rep[0])
	top2_dist = float(dis_rep[2])
	#print top1_dist
	#print top2_dist

	label_data = pd.read_csv(label_id, sep = ',', header = None)
	label_data = np.asarray(label_data)

	id_identifyied_1 = label_data[ann_rep[0]]
	id_identifyied_1 = str(id_identifyied_1)
	id_identifyied_1 = ((str(id_identifyied_1.split(',')).split("'"))[1])
	#print id_identifyied_1
	#id_identifyied_1 = id_identifyied_1[1][:-2]


	id_identifyied_2 = label_data[ann_rep[2]]
	id_identifyied_2 = str(id_identifyied_2)
	id_identifyied_2 = ((str(id_identifyied_2.split(',')).split("'"))[1])
	#id_identifyied_2 = id_identifyied_2[1][:-2]
	#print id_identifyied_2
	print id_identifyied_1
	print id_identifyied_2


	if top1_dist < float(0.2) or top1_dist == float(0.2):
		response.append(id_identifyied_1)
	elif top1_dist > float(0.8):
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