import unittest
from collections import deque
import temps

class tester(unittest.TestCase):
	
	def test_buildup(self):
		weights = [0,2,2,1]
		deck = deque([20,20,20,20], maxlen=4)
		target = 10
		
		temp=20
		#test returned queue - should return vector mult of
		# weights * deck = [0,2,2,1] * [20, 20, 20, 20] = 100
		new_deck, buildup = temps.update_buildup(deck, weights, temp, target)		
		self.assertEqual(buildup, 50)
		#deck should remain unchanged
		self.assertEqual(new_deck, deque([20, 20, 20, 20]))
		
		for i in [1,2,3,4]:
			temp=i
			new_deck, buildup = temps.update_buildup(deck, weights, temp, target)
		self.assertEqual(new_deck, deque([1, 2, 3, 4]))
		
	def test_weights(self):
		#test production of a vector of length window.  First third are old, second mid, last recent
		window = 9
		old = 1
		mid = 2
		new = 3
		weights = temps.build_weights(old, mid, new, window)
		self.assertEqual(weights, [1,1,1,2,2,2,3,3,3])
		
		#test if it handles a not-cleanly-divisible window (most recent takes up slacek)
		window = 10
		weights = temps.build_weights(old, mid, new, window)
		self.assertEqual(weights, [1,1,1,2,2,2,3,3,3,3])		
		
if __name__=='__main__':		
	unittest.main()