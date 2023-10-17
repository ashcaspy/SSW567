# -*- coding: utf-8 -*-
"""
Updated Jan 21, 2018
The primary goal of this file is to demonstrate a simple unittest implementation

@author: jrr
@author: rk

Updated 2023-10-16 by Ashley Foglia
"""

import unittest

from Triangle import classifyTriangle

# This code implements the unit test functionality
# https://docs.python.org/3/library/unittest.html has a nice description of the framework

class TestTriangles(unittest.TestCase):
    # define multiple sets of tests as functions with names that begin

    def testRightTriangle(self): 
        self.assertEqual(classifyTriangle(3,4,5),'Right','3,4,5 should be a Right triangle')
        self.assertEqual(classifyTriangle(5,3,4),'Right','5,3,4 should be a Right triangle')  
        self.assertEqual(classifyTriangle(4,5,3),'Right','4,5,3 should be a Right triangle')        
    def testEquilateralTriangle(self): 
        self.assertEqual(classifyTriangle(1,1,1),'Equilateral','1,1,1 should be Equilateral')
    def testScaleneTriangle(self): 
        self.assertEqual(classifyTriangle(2,3,4),'Scalene','2,3,4 should be Scalene')
        self.assertEqual(classifyTriangle(4,2,3),'Scalene','4,2,3 should be Scalene')
        self.assertEqual(classifyTriangle(3,4,2),'Scalene','3,4,2 should be Scalene')
    def testIsoscelesTriangle(self): 
        self.assertEqual(classifyTriangle(5,5,9),'Isosceles','5,5,9 should be Isosceles')
        self.assertEqual(classifyTriangle(5,9,5),'Isosceles','5,9,5 should be Isosceles')
        self.assertEqual(classifyTriangle(9,5,5),'Isosceles','9,5,5 should be Isosceles')
    def testNotATriangle(self): 
        self.assertEqual(classifyTriangle(1,2,3),'NotATriangle','1,2,3 should be NotATriangle')
        self.assertEqual(classifyTriangle(3,1,2),'NotATriangle','3,1,2 should be NotATriangle')
        self.assertEqual(classifyTriangle(2,3,1),'NotATriangle','2,3,1 should be NotATriangle')
        self.assertEqual(classifyTriangle(3,10,14),'NotATriangle','3,10,14 should be NotATriangle')
        self.assertEqual(classifyTriangle(14,3,10),'NotATriangle','14,3,10 should be NotATriangle')
        self.assertEqual(classifyTriangle(10,14,3),'NotATriangle','10,14,3 should be NotATriangle')
    def testEq200Inputs(self): 
        self.assertEqual(classifyTriangle(200, 200, 200),'Equilateral','200, 200, 200 should be Equilateral')

    # Test invalid values
    def testEq0Inputs(self): 
        self.assertEqual(classifyTriangle(0, 5, 10),'InvalidInput','0, 5, 10 should be InvalidInput')
        self.assertEqual(classifyTriangle(5, 0, 10),'InvalidInput','5, 0, 10 should be InvalidInput')
        self.assertEqual(classifyTriangle(10, 5, 0),'InvalidInput','10, 5, 0 should be InvalidInput')
        self.assertEqual(classifyTriangle(0, 0, 0),'InvalidInput','0, 0, 0 should be InvalidInput')
    def testLt0Inputs(self): 
        self.assertEqual(classifyTriangle(-1, 5, 10),'InvalidInput','-1, 5, 10 should be InvalidInput')
        self.assertEqual(classifyTriangle(5, -1, 10),'InvalidInput','5, -1, 10 should be InvalidInput')
        self.assertEqual(classifyTriangle(10, 5, -1),'InvalidInput','10, 5, -1 should be InvalidInput')
        self.assertEqual(classifyTriangle(-1, -1, -1),'InvalidInput','-1, -1, -1 should be InvalidInput')
    def testGt200Inputs(self): 
        self.assertEqual(classifyTriangle(201, 200, 200),'InvalidInput','201, 200, 200 should be InvalidInput')
        self.assertEqual(classifyTriangle(200, 201, 200),'InvalidInput','200, 201, 200 should be InvalidInput')
        self.assertEqual(classifyTriangle(200, 200, 201),'InvalidInput','200, 200, 201 should be InvalidInput')
        self.assertEqual(classifyTriangle(201, 201, 201),'InvalidInput','201, 201, 201 should be InvalidInput')

    # Test common invalid input types -- string, float, none
    def testFloatInputs(self): 
        self.assertEqual(classifyTriangle(5.5, 3, 4),'InvalidInput','5.5, 3, 4 should be InvalidInput')
        self.assertEqual(classifyTriangle(5, 3.6, 4),'InvalidInput','5, 3.6, 4 should be InvalidInput')
        self.assertEqual(classifyTriangle(5, 3, 4.7),'InvalidInput','5, 3, 4.7 should be InvalidInput')
        self.assertEqual(classifyTriangle(5.5, 3.6, 4.7),'InvalidInput','5.5, 3.6, 4.7 should be InvalidInput')

    def testStringInputs(self): 
        with self.assertRaises(TypeError) : classifyTriangle("15",11,9)
        with self.assertRaises(TypeError) : classifyTriangle(15,"11",9)
        with self.assertRaises(TypeError) : classifyTriangle(15,11,"9")
        with self.assertRaises(TypeError) : classifyTriangle("15","11","9")

    def testNoneInputs(self): 
        with self.assertRaises(TypeError) : classifyTriangle(None, 7, 8)
        with self.assertRaises(TypeError) : classifyTriangle(8, None, 7)
        with self.assertRaises(TypeError) : classifyTriangle(7, 8, None)
        with self.assertRaises(TypeError) : classifyTriangle(None,None,None)


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()

