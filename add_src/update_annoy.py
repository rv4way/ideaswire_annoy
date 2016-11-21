import os
import numpy as np
import pandas as pd
import cPickle
from annoy import AnnoyIndex
import os


def create_annoy():
	t = AnnoyIndex(128, metric = 'eucledian')
	count = 0
	annoy_path = '../annoy/face_module.ann'

	label_id = '../annoy/label_id.csv'
	label_data = open(label_id, 'wb')

	rep_location = '../img_rep'
	rep_list = os.listdir(rep_location)
	for x, y in enumerate(rep_list):
		#print x, y
		profile_id = y.split('.')
		profile_id = profile_id[0]
		#print profile_id
		rep_file = os.path.join(rep_location, y)
		with open(rep_file, 'rb') as data:
			rep = cPickle.load(data)
		for z in rep:
			#print z
			t.add_item(count, z)
			line = str(count) + ',' + str(profile_id) + '\n'
			label_data.write(line)
			count += 1

	t.build(1000)
	t.save(annoy_path)

	label_data.close()
	#print '*****ANNOY AND LABEL_ID FILE UPDATED*****'