import unittest
import recommend_ex as rec
import numpy as np
import scipy as sp
from scipy.sparse import coo_matrix
from scipy.sparse import lil_matrix

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
		self.true_parsed_customers = { 'justin':['car','boat','plane'],
						'diane':['boat','dress','shirt','pants'],
						'jiffy':['suit','dress','food','hat','watch'],
						'octo':['frills','seacreatures','watch','hat','bananas','glasses'],
						}


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
		user_pos,item_pos,item_user_dict,user_dict = rec.pre_process(self.true_parsed_customers,1)
		ret = rec.create_sparse_user_item_mat(item_user_dict,len(item_pos))
		self.assertTrue(np.array_equal(np.array(self.true_matrix),ret.toarray()))
		print ret.toarray()

	#test_build_recommender
	def test_build_recommender(self):
		fi = open('simple_filter_test').readlines()
		item_sim_mat,customer_purchase_mat = rec.build_recommender(fi,1)

		print 'item_sim_mat'
		print item_sim_mat.toarray()
		print item_sim_mat.shape
		print 'customer_purchase_mat'
		print customer_purchase_mat.toarray()
		print customer_purchase_mat.shape
	#test_recommend

	#more to come!


if __name__ == '__main__':
	unittest.main()

