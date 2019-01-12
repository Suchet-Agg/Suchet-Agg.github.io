# CSE 101 - IP HW2
# K-Map Minimization - Test Cases
# Name: Suchet Aggarwal
# Roll Number: 2018105
# Section: A
# Group: 1
# Date: 09.10.18


import unittest
from HW2_2018105 import minFunc



class testpoint(unittest.TestCase):
	def test_minFunc(self):
		#Test Case 1
		self.assertEqual(minFunc(4,'(0,1,2,4,5,6,8,9,12,13,14) d-'),"w'z' + xz' + y'")
		#Test Case 2
		self.assertEqual(minFunc(3,'(0) d-'),"w'x'y'")
		#Test Case 3
		self.assertEqual(minFunc(2,'(0,1) d(2)'),"w'")
		#Test Case 4
		self.assertEqual(minFunc(3,'(0,4,5) d(1,2,3)'),"x'")
		#Test Case 5
		self.assertEqual(minFunc(4,'(0,3,4,7,8,11,12,15) d(1,2,5,6,9,10,13,14)'),'1')
		#Test Case 6
		self.assertEqual(minFunc(4,'(1,3,7,11,15) d (0,2,5)'),"w'z + yz")
		#Test Case 7
		self.assertEqual(minFunc(2,'(0,1,2) d-'),"w' + x'")
		#Test Case 8
		self.assertEqual(minFunc(4,'(0,1,2,3,4,5,7,8,12) d-'),"w'x' + w'z + y'z'")
		
                
if __name__=='__main__':
	unittest.main()

