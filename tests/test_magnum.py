import magnum
import unittest

class MagnumTest(unittest.TestCase):
	def setUp(self):
		class Test(magnum.Model):
			name = magnum.StringField()

		self.Test = Test

	def test_string_save(self):
		test = self.Test(name='1234')
		#self.assertEqual(self.Test[0].name, '1234')
