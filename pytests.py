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

		self


	#this should test the jaccard_distance function
	#expects two sparse 1xN matrices
	def test_jaccard_distance(self):
		true_result = (self.m01 + self.m10) / (self.m10 + self.m01 + self.m11 + 0.0)
		self.assertEqual(true_result,rec.jaccard_distance(self.row1.toarray(),self.row2.toarray()))

	def test_parse_array(self):
		fi = open('simple_filter_test')
		true_result = { 'justin':['car','boat','plane'],
						'diane':['boat','dress','shirt','pants'],
						'jiffy':['suit','dress','food','hat','watch'],
						'octo':['frills','seacreatures','watches','hats','bananas','glasses'],
						}
		ret_dict = rec.parse_array(fi.readlines())
		print ret_dict
		print sorted(ret_dict.keys())
		for k in sorted(ret_dict.keys()):
			self.assertEqual(true_result[k].sort(),ret_dict[k].sort())
		for k in sorted(true_result.keys()):
			self.assertEqual(true_result[k].sort(),ret_dict[k].sort())

if __name__ == '__main__':
	unittest.main()

