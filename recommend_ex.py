import scipy as sp
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse import coo_matrix

#need to make this for use in a np.array as opposed to current
def jaccard_distance(item1,item2):
	m = np.zeros((2,2))
	for var1 in item1:
		for var2 in item2:
			m[var1][var2] += 1
	j_dist = (m[0][1]+m[1][0])/(m[0][1]+m[1][0]+m[1][1]+0.0)
	return j_dist

#this function is not side effect free
#this function will add to an item array new items
#this should update item_array and item_dict 
def pre_process_items(item_array,item_pos,user):
	for item in user:
		if item not in item_array:
			item_array.append(item)
			item_pos[item] = len(item_array)-1

#this will return a dict of users where the values are lists for item numbers 
def pre_process(fi):
	item_array = []
	item_pos = {}
	user_dict = {}
	user_array = []
	user_pos = {}
	item_user_dict = {}
	for user in fi:
		# add exception handling
		person,items = user.split('-')
		items = items.split(',')
		user_array.append(user)
		user_pos = len(user_array)-1
		pre_process_items(item_array,item_pos,items)
		for i in range(items):			
			items[i] = item_dict[items[i]]


	return user_dict,item_array,user_pos,item_pos,item_user_dict

#build sparse matrix
def create_sparse_mat(user_pos,item_pos,user_dict):
	MATRIX_SIZE = len(item_pos)
	sparse_item_matrix = lil_matrix((MATRIX_SIZE,MATRIX_SIZE))
	for user in user_dict:
		for item in user_dict[user]:
			sparse_item_matrix[user_pos[user],item_pos[item]] = 1
	return sparse_item_matrix


#should this take a file as input?
def build_recommender(file):
	fi = open(file)
	user_dict,item_array,user_pos,item_pos = pre_process(fi.readlines())
	sparse_item_matrix = create_sparse_mat(user_pos,item_pos,user_dict)

	item_sim_dict = {}
	sparse_coo = sparse_item_matrix.coo_matrix()
	#next is to actually implement the rest of the amazon algorithm can use getcol and getrow 
	customer_purchase_mat = coo_matrix(sparse_coo.shape())
	item_sim_mat = coo_matrix(sparse_coo.shape())
	for i in xrange(len(item_pos)):
		current_item = sparse_coo.getcol(i).nonzero()
		if len(current_item) > 0:
		#customer is bad var name replace
			for customer in current_item:
				customer_items = sparse_item_matrix.getrow(customer_items[0]).nonzero()
				for item in customer_items:
					customer_purchase_mat[i,item[1]] += 1
				item_sim_mat[i,item[1]] = jaccard_distance(sparse_coo.getcol(i).toarray(),sparse_coo.getcol(item[1]).toarray())
	return item_sim_mat,customer_purchase_mat


