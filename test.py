from microngo import Microngo, Query, Document
from datetime import datetime
from bson.objectid import ObjectId
from random import randrange
from pymongo import ASCENDING
from pymongo.cursor import Cursor
import unittest

class TestCase(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestCase, self).__init__(*args, **kwargs)

		# Database
		self.db		= Microngo('localhost', 27017, db="microngo_test")
		self.db2	= Microngo('localhost', 27017)

	@classmethod
	def setUpClass(cls):
		pass

	@classmethod
	def tearDownClass(cls):
		pass

	def setUp(self):
		pass

	def tearDown(self):
		pass

	#
	# Begin test
	#

	def test_01_insert_one(self):
		document			= self.db.insert("collection_one")
		document.String		= "ABCDEabcde12345"
		document.Integer	= 321
		document.Float		= 321.123
		document.Datetime	= datetime.utcnow()
		document.List		= ["One", 2, 3.0]
		document.Dict		= {
			"A": "John",
			"B": "Doe",
			"C": {
				"A": "B"
			},
			"D": ["One", 2, 3.0]
		}
		document_id = document.save()
		self.assertEqual(type(document_id), ObjectId)

	def test_02_insert_many(self):
		documents = self.db.insert("collection_two")
		for i in range(0, 10):
			documents.No	= i
			documents.Rand	= randrange(1000, 9999)
			# Add
			documents.add()
		# Save
		result = documents.save()
		self.assertEqual(type(result), list)
		# Check per item
		for i in result:
			self.assertEqual(type(i), ObjectId)

	def test_03_find_one(self):
		document = self.db.query("collection_two").find_one({"No": 5}).one()
		self.assertEqual(type(document), Document)
		self.assertEqual(document.No, 5)

	def test_04_find_first(self):
		document = self.db.query("collection_two").find({"No": 5}) \
			.sort('No', ASCENDING) \
			.skip(0).limit(5).first()
		self.assertEqual(type(document), Document)
		self.assertEqual(document.No, 5)
		self.assertEqual(document.Empty, None)

		# Find all empty cursor
		documents_2 = self.db.query("collection_two").find({"XYZ": 2}).first()
		self.assertEqual(type(documents_2), {})

	def test_05_find_all(self):
		documents = self.db.query("collection_two").find().all()
		self.assertEqual(type(documents), list)
		# Check per item
		for i in documents:
			self.assertEqual(type(i.No), int)

	def test_06_raw(self):
		document	= self.db.query("collection_two").find_by()
		raw_query	= document.raw()
		docs		= document.first()
		raw_docs	= docs.raw()
		self.assertEqual(type(raw_query), Cursor)
		self.assertEqual(type(docs), Document)
		self.assertEqual(type(raw_docs), dict)
		
	def test_07_update(self):
		documents = self.db.query("collection_two").find().all()
		self.assertEqual(type(documents), list)
		# Check per item
		for i in documents:
			self.assertEqual(type(i.No), int)
			i.Rand = 0
			result = i.save()
			self.assertEqual(type(result), ObjectId)
	
	def test_08_error_test(self):
		# Test db error
		with self.assertRaises(Exception) as ctx:
			self.db2.query("collection_two").find().all()
		
		# Set database
		self.db2.database("microngo_test")

		# One
		doc_one_a = self.db.query("collection_one").find_one({"XYZ": 22}).one()
		self.assertEqual(type(doc_one_a), dict)

		with self.assertRaises(Exception) as ctx:
			doc_one_b = self.db.query("collection_one").find().one()

		# First
		doc_first_a = self.db.query("collection_one").find_one({"XYZ": 22}).first()
		self.assertEqual(type(doc_first_a), dict)

		doc_first_b = self.db.query("collection_one").find_one().first()
		self.assertEqual(type(doc_first_b), Document)

		with self.assertRaises(Exception) as ctx:
			doc_first_c = self.db.query("collection_one").count_documents({}).first()

		# All
		doc_all_a = self.db.query("collection_one").find_one({"XYZ": 22}).all()
		self.assertEqual(type(doc_all_a), list)
		with self.assertRaises(Exception) as ctx:
			doc_all_b = self.db.query("collection_one").find_one().all()
		
	def test_09_delete(self):
		# Delete one
		document = self.db.query("collection_one").find_one().one()
		self.assertEqual(type(document), Document)
		document.remove()

		# Delete many
		documents = self.db.query("collection_two").find().all()
		self.assertEqual(type(documents), list)
		# Check per item
		for i in documents:
			self.assertEqual(type(i.No), int)
			i.remove()

if __name__ == '__main__':
	unittest.main()