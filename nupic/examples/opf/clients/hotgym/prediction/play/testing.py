'''
Created on Jan 5, 2015

@author: jstanish
'''
import unittest
from adder import adder_errors


class Test(unittest.TestCase):


    def test_adder_errors(self):
        "Tests insuring that errors in data cause validation failures"
        self.assertRaises(TypeError, adder_errors(4.7,2))
        self.assertRaises(TypeError, adder_errors(2,4.7))
        
    def xtest_adder_successes(self):
        "Tests insuring that valid data passes"
        self.assertEqual(9, adder_errors(5,4), "Not accepting two integers")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
