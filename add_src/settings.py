'''Setting file contains all settings of the code,
	on which output depends, it nothing but some variable which control the,
	system.
'''

#ann_search.py settings
#number of result from annoy
ann_depth = 20

#minimun diatance of rep
min_dist = float(0.2)

#maximum distance of rep
max_dist = float(0.9)

#avgrage distance of rep may be identifyied or not
avg_dist = float(0.5)

#maximum distance between top1 and top2 results
top_dist = float(1.7)


#transform_img.py settings
#degree by which image rottate (affine trtansformation)
rot = 10

#update_annoy.py settings

# number of tree build during annoy
n_tree = 1000