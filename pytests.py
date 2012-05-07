import unittest
import time
import recommend_ex as rec
import numpy as np
import scipy as sp
from scipy.sparse import coo_matrix
from scipy.sparse import lil_matrix
from numpy.random import randint
class test_recommend_base_functions(unittest.TestCase):

	#setup for Testcase
	def setUp(self):
		self.row1 = lil_matrix([0, 0, 1, 1, 0, 1, 0])
		self.row2 = lil_matrix([1, 1, 0, 0, 0, 1, 0])
		self.m00 = 1
		self.m01 = 2
		self.m10 = 2
		self.m11 = 1
		self.true_matrix = [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
							[0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
							[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
							[0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1],]
		self.jac_matrix = [np.array([[1],[0],[1],[0]]),
							np.array([[1],[1],[0],[0]]),
							np.array([[1],[0],[0],[0]]),
							np.array([[1],[0],[0],[0]]),
							np.array([[0],[1],[0],[0]]),
							np.array([[0],[1],[0],[0]]),
							np.array([[0],[1],[0],[1]]),
							np.array([[0],[1],[0],[1]]),
							np.array([[0],[0],[1],[0]]),
							np.array([[0],[0],[1],[0]]),
							np.array([[0],[0],[0],[1]]),
							np.array([[0],[0],[0],[1]]),
							np.array([[0],[0],[0],[1]]),
							np.array([[0],[0],[0],[1]])]

		self.true_parsed_customers = { 'justin':['car','boat','plane'],
						'diane':['boat','dress','shirt','pants'],
						'jiffy':['suit','dress','food','hat','watch'],
						'octo':['frills','seacreatures','watch','hat','bananas','glasses'],
						}
		self.used_coords = [(0,0),(0,1),(0,2),(0,3),(0,8),(0,9),(1,0),(1,1),(1,2),(1,3),(1,4),
							(1,5),(1,6),(1,7),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3),
							(4,1),(4,4),(4,5),(4,6),(4,7),(5,1),(5,4),(5,5),(5,6),(5,7),
							(6,1),(6,4),(6,5),(6,6),(6,7),(6,10),(6,11),(6,12),(6,13),
							(7,1),(7,4),(7,5),(7,6),(7,7),(7,10),(7,11),(7,12),(7,13),
							(8,0),(8,8),(8,9),(9,0),(9,8),(9,9),(10,6),(10,7),(10,10),
							(10,11),(10,12),(10,13),(11,6),(11,7),(11,10),(11,11),(11,12),
							(11,13),(12,6),(12,7),(12,10),(12,11),(12,12),(12,13),(13,6),
							(13,7),(13,10),(13,11),(13,12),(13,13)]

	#this should test the jaccard_distance function
	#expects two sparse 1xN matrices
	# TODO UPDATE THIS TEST 
	# [[ 1.]
 	#[ 0.]
 	#[ 1.]
 	#[ 0.]]
	#item 2
	#[[ 1.]
 	#[ 0.]
 	#[ 1.]
 	#[ 0.]]
#	def test_jaccard_distance(self):
#		true_result = (self.m01 + self.m10) / (self.m10 + self.m01 + self.m11 + 0.0)
#		self.assertEqual(true_result,rec.jaccard_distance(self.row1.toarray(),self.row2.toarray()))

	#tests parse_array
	def test_parse_array(self):
		fi = open('simple_filter_test')
		
		ret_dict = rec.parse_array(fi.readlines())
		print ret_dict
#		print sorted(ret_dict.keys())
		for k in sorted(ret_dict.keys()):
			self.assertEqual(self.true_parsed_customers[k].sort(),ret_dict[k].sort())
		for k in sorted(self.true_parsed_customers.keys()):
			self.assertEqual(self.true_parsed_customers[k].sort(),ret_dict[k].sort())

	#this needs to be improved but is ok for now
	def test_pre_process(self):
		after_octo = {'boat':0,'dress':1,'shirt':2,'pants':3,'suit':4,'food':5,'hat':6,'watch':7,'car':8,'plane':9,'frills':10,'seacreatures':11,'bananas':12,'glasses':13}
		
		#pass in 1 for it to be sorted
		user_pos,item_pos,item_user_dict,user_dict = rec.pre_process(self.true_parsed_customers,1)
		for k in after_octo:
			self.assertEqual(after_octo[k],item_pos[k])
		for k in item_pos:
			self.assertEqual(after_octo[k],item_pos[k])

	#next test_create_sparse_matrix
	def test_create_sparse_mat(self):
		user_pos,item_pos,item_user_dict,user_dict= rec.pre_process(self.true_parsed_customers,1)
		ret = rec.create_sparse_user_item_mat(item_user_dict,len(item_pos))
		self.assertTrue(np.array_equal(np.array(self.true_matrix),ret.toarray()))
		print ret.toarray()

	#test_build_recommender
	def test_build_recommender(self):
		fi = open('simple_filter_test').readlines()
		item_sim_mat,user_dict,item_pos,user_pos,item_dict = rec.build_recommender(rec.parse_array(fi),1)
		test_arr = []
		item_sim_mat = item_sim_mat.toarray()
		print 'item sim mat'
		print item_sim_mat
		for item1 in self.jac_matrix:
			temp = []
			for item2 in self.jac_matrix:
				temp.append(rec.jaccard_distance(item1,item2))
			test_arr.append(temp)
		for ent in self.used_coords:
			self.assertEqual(test_arr[ent[0]][ent[1]],item_sim_mat[ent[0]][ent[1]])
		for i in range(len(item_sim_mat)):
			for j in range(len(item_sim_mat)):
				if (i,j) in self.used_coords:
					self.assertEqual(test_arr[i][j],item_sim_mat[i][j])
				else:
#					print '(%d,%d)' %(i,j)
					self.assertEqual(item_sim_mat[i][j],0)	
	
		print item_pos
		print user_dict
		print user_pos 
		print item_dict
	#test_recommend

	#more to come!
	def test_speed_build_recommender(self):
		NUM_CUSTOMERS = 100
		NUM_ITEMS = 100
		NUM_ITEMS_PER_CUST = 10
		fi = {}
		for i in xrange(0,NUM_CUSTOMERS):
			i = str(i)
			fi[i] = randint(0,NUM_ITEMS,50)
			fi[i] = [str(x) for x in fi[i]]
		t3 = time.time()
		rec.build_naive_recommender(fi)
		t4 = time.time()
		print (t4-t3)/60.0

		t1 = time.time()
		rec.build_recommender(fi)
		t2 = time.time()

		print (t2-t1)/60.0


if __name__ == '__main__':
	unittest.main()

