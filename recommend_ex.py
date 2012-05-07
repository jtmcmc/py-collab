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
	for i in xrange(len(item1)):
		m[item1[i][0]][item2[i][0]] += 1
	j_dist = (m[0][1]+m[1][0])/(m[0][1]+m[1][0]+m[1][1]+0.0)
	return 1-j_dist

#this function is not side effect free
#this function will add to an item array new items
#this should update item_array and item_pos
#I should probably remove item_array I could just use len(item_pos) 
#don't know if i'll need it later but duly noted
def pre_process_items(item_pos,user):
	ret_li = []
	for item in user:
		if item not in item_pos:
			item_pos[item] = len(item_pos)
		ret_li.append(item_pos[item])
	return ret_li

#this expects a dict where keys are customer strings and values are lists of 
#item strings
#and a 1/0 value (default 0) that determines whether it should sort 
# (used only for testing purposes)
#this will return a dict of users where the values are lists for item numbers 
def pre_process(fi,s=0):
	item_array = []
	item_pos = {}
	user_dict = {}
	user_array = []
	# user_pos
	user_pos = {}
	# user_pos : [list of item_pos]
	item_user_dict = {}
	if s == 1:
		for user in sorted(fi.keys()):
			user_pos[user] = len(user_pos)
			user_dict[user_pos[user]] = user
			item_user_dict[user_pos[user]] = pre_process_items(item_pos,fi[user])
	else:
		for user in fi:
			user_pos[user] = len(user_pos)
			user_dict[user_pos[user]] = user
			item_user_dict[user_pos[user]] = pre_process_items(item_pos,fi[user])
	return user_pos,item_pos,item_user_dict,user_dict

#build sparse matrix where rows are customers and columns are items
def create_sparse_user_item_mat(item_user_dict,n):
	ROWS = len(item_user_dict)
	COLS = n
	sparse_item_matrix = lil_matrix((ROWS,COLS))
	for user in item_user_dict:
		for item in item_user_dict[user]:
			sparse_item_matrix[user,item] = 1
	return sparse_item_matrix




#This expects an array of strings input and s a 1 or 0 indicating whether it 
#should sort things, this is only used for testing
def build_recommender(input,s=0):
	user_pos,item_pos,item_user_dict,user_dict = pre_process(input,s)
	item_dict = dict(reversed(item) for item in item_pos.items())
	sparse_item_matrix = create_sparse_user_item_mat(item_user_dict,len(item_pos))
	MATRIX_SIZE = sparse_item_matrix.shape[1]

	item_sim_dict = {}
	#next is to actually implement the rest of the amazon algorithm can use getcol and getrow 
	customer_purchase_mat = lil_matrix(np.zeros((MATRIX_SIZE,MATRIX_SIZE)))
	item_sim_mat = lil_matrix(np.zeros((MATRIX_SIZE,MATRIX_SIZE)))

	#this should iterate over all the items
	for i in xrange(len(item_pos)):

		if i % 10 == 0:
			print i
		#this is taking all the customers that have selected this item
		test = sparse_item_matrix.getcol(i)
		current_item = sparse_item_matrix.getcol(i).nonzero()
		#if any players have selected this item
		if len(current_item) > 0:
			#look at all the customers that have selected this item
			for customer in current_item[0]:
				#get all the items this customer has also selected
				customer_items = sparse_item_matrix.getrow(customer).nonzero()
				#this should become C or Cython and parallelized
				#for each item this person has selected
				for item in customer_items[1]:
					#note that item i and item have been selected together
				#	customer_purchase_mat[i,item] += 1
					#store the jaccard distance between i and item 
					item_sim_mat[i,item] = jaccard_distance(sparse_item_matrix.getcol(i).toarray(),
												sparse_item_matrix.getcol(item).toarray())
#	print 'item sim mat'
#	print item_sim_mat.toarray()
	#should return item-item similarity matrix, item-item purchase matrix
	#also dict mappings  	
	return item_sim_mat,user_dict,item_pos,user_pos,item_dict

def build_naive_recommender(input,s=0):
	user_pos,item_pos,item_user_dict,user_dict = pre_process(input,s)
	item_dict = dict(reversed(item) for item in item_pos.items())
	sparse_item_matrix = create_sparse_user_item_mat(item_user_dict,len(item_pos))
	MATRIX_SIZE = sparse_item_matrix.shape[1]

	item_sim_dict = {}
	#next is to actually implement the rest of the amazon algorithm can use getcol and getrow 
	customer_purchase_mat = lil_matrix(np.zeros((MATRIX_SIZE,MATRIX_SIZE)))
	item_sim_mat = lil_matrix(np.zeros((MATRIX_SIZE,MATRIX_SIZE)))

	#this should iterate over all the items
	for i in xrange(len(item_pos)):
		if i % 10 == 0:
			print i
		for j in xrange(len(item_pos)):
			item_sim_mat[i,j] = jaccard_distance(sparse_item_matrix.getcol(i).toarray(),
												sparse_item_matrix.getcol(j).toarray())
	return item_sim_mat,user_dict,item_pos,user_pos,item_dict


#build the recommender
#it's going to expect a list of items coordinates purchased by a customer and 
#it will return the N highest matching items 
#couple of considerations - don't consider the item that is the same as the one passed in

#takes in item_sim_mat, customer,user_dict,user_pos,item_dict,item_pos,N (n items)
#customer is expected to be in {'customer':['item1','item2']} format
def recommend(item_sim_mat, customer,item_dict,item_pos,N):
	# one product the customer has purchased
	items_hash = {}
	for item in customer.values():
		# all the items that have been purchased by customers including 'item'
		position = item_pos[item]
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


