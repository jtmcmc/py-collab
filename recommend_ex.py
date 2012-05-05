import scipy as sp
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse import coo_matrix

#array parsing function expects format of customer-item1,item2,item3 expects list of strings
def parse_array(in_list):
	cust_item_dict = {}
	for li in in_list:
		li = li.split('-')
		li[1] = li[1].split(',')
		li[1] = [l.strip() for l in li[1]]
		cust_item_dict[li[0]] = li[1]
	return cust_item_dict

#this expects two arrays with a structure (1,N) done by calling sparse_matrix.toarray() if they were originally sparse
def jaccard_distance(item1,item2):
	m = np.zeros((2,2))
	# assumption here is vectors are same length since they are toarray this should be true
	for i in xrange(len(item1[0])):
		m[item1[0][i]][item2[0][i]] += 1
	j_dist = (m[0][1]+m[1][0])/(m[0][1]+m[1][0]+m[1][1]+0.0)
	return j_dist

#this function is not side effect free
#this function will add to an item array new items
#this should update item_array and item_pos
#I should probably remove item_array I could just use len(item_pos) 
#don't know if i'll need it later but duly noted
def pre_process_items(item_array,item_pos,user):
	for item in user:
		if item not in item_pos:
			item_array.append(item)
			item_pos[item] = len(item_array)-1

#this will return a dict of users where the values are lists for item numbers 
def pre_process(fi,s=0):
	item_array = []
	item_pos = {}
	user_dict = {}
	user_array = []
	user_pos = {}
	item_user_dict = {}
	if s == 1:
		for user in sorted(fi.keys()):
			user_array.append(user)
			user_pos[user] = len(user_array)-1
			pre_process_items(item_array,item_pos,fi[user])
	else:
		for user in fi:
			user_array.append(user)
			user_pos[user] = len(user_array)-1
			pre_process_items(item_array,item_pos,fi[user])
	return user_pos,item_pos

#build sparse matrix
def create_sparse_mat(user_pos,item_pos,user_dict):
	MATRIX_SIZE = len(item_pos)
	sparse_item_matrix = lil_matrix((MATRIX_SIZE,MATRIX_SIZE))
	for user in user_dict:
		for item in user_dict[user]:
			sparse_item_matrix[user_pos[user],item_pos[item]] = 1
	return sparse_item_matrix


#should this take a file as input?
#this should not take a file as input and it should not take a line 
#it should expect a string and an array of strings
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
#this should become C or Cython and parallelized
				for item in customer_items:
					customer_purchase_mat[i,item[1]] += 1
				item_sim_mat[i,item[1]] = jaccard_distance(sparse_item_matrix.getcol(i).toarray(),sparse_item_matrix.getcol(item[1]).toarray())
	return item_sim_mat,customer_purchase_mat

#build the recommender
#it's going to expect a list of items coordinates purchased by a customer and 
#it will return the N highest matching items 
def recommend(customer,N,item_sim,customer_mat):
	# one product the customer has purchased
	items_hash = {}
	for item in customer:
		# all the items that have been purchased by customers including 'item'
		purchased_also = customer_mat.getcol(item).nonzero()
		for pair in purchased_also:
			items_hash[(pair[0],pair[1])] = item_sim[pair[0]][pair[1]]
		
	# sort dict by values and then take the top N values


# still to build lots of pre-process functions
# a function to take a file handle and process the file
# a function to take an input of a customer with a name and a list of items 
# it's purchased (a string and array of strings). and map that array to a list 
# of locations in the item matrices this can be done via the 

#Should I make this all part of a class 
#the class takes as input either a file or array
#can add lines via an add_customer function
#would then call the build_recommender function which would create the various
#data structures, the item_dict and the item_sim and customer_purchase_mat 
#most especially 
#those will need to be instance variables of the class 


#if I really wanted to parallelize this I would need to probably turn to hadoop 
#or something like that


