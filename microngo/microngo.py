from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.command_cursor import CommandCursor

class Microngo():
	def __init__(self, *args, **kwargs):
		# Variables
		self.collection	= None
		self._db_name	= None

		# Get database name and remove it
		database = kwargs.get("db")
		if database:
			del kwargs["db"]
			self._db_name = database

		# New mongo client
		self.client	= MongoClient(*args, **kwargs)

		# Database
		if self._db_name:
			self.db = self.client[self._db_name]

	def database(self, database):
		# Set database
		self.db = self.client[database]
		return self

	def _collection(self, collection):
		if self.db:
			self.collection = self.db[collection]
			return self.collection 
		else:
			raise Exception("Database not found, please set database first.")

	def query(self, collection):
		return Query(self._collection(collection))
	
	def insert(self, collection):
		return Document(self._collection(collection))

class Document():
	def __init__(self, collection, data=None):
		# Variables
		self.microngo_collection	= collection
		self.microngo_payloads		= []
		self.microngo_document_id	= None

		# Dict data
		if data:
			if isinstance(data, dict):
				# Set documen id if exist
				if data.get("_id"):
					self.microngo_document_id = data.get("_id")
				# Update data
				self.__dict__.update(data)
			else:
				raise Exception("zzz")

	def __getattr__(self, name):
		return None

	def _get_payloads(self):
		# Get self variable in dictionary
		payloads = dict(self.__dict__)

		# Remove internal variables and return data
		del payloads['microngo_collection']
		del payloads['microngo_payloads']
		del payloads['microngo_document_id']
		return payloads

	def _clear_payloads(self):
		# Cache variable
		cache_collection	= self.microngo_collection
		cache_payloads		= self.microngo_payloads
		
		# Clear self variables
		payloads = self.__dict__
		payloads.clear()
		
		# Reasign internal variables from cache
		payloads['microngo_collection']	= cache_collection
		payloads['microngo_payloads']	= cache_payloads
		return self

	def add(self):
		if not self.microngo_document_id:
			# Get payloads
			payloads = self._get_payloads()

			# Append to cache
			self.microngo_payloads.append(payloads)

			# Clear previous payload and return
			self._clear_payloads()
			return self

	def raw(self):
		# Get raw data
		return self._get_payloads()

	def save(self):
		if self.microngo_document_id:
			# Update
			self.microngo_collection.update_one(
				{'_id': self.microngo_document_id},
				{'$set': self._get_payloads()},
				upsert=False
			)
		else:
			# Insert
			if len(self.microngo_payloads) > 0:
				data = self.microngo_payloads
				return self.microngo_collection.insert_many(data).inserted_ids
			else:
				data = self._get_payloads()
				return self.microngo_collection.insert_one(data).inserted_id

	def remove(self):
		if self.microngo_document_id:
			# Delete
			self.microngo_collection.delete_one({'_id': self.microngo_document_id})

class Query():
	def __init__(self, collection, cursor=None):
		self.collection = collection
		self.cursor		= cursor

	def __getattr__(self, name):
		def method(*args, **kwargs):
			func = getattr(self.collection, name)
			self.cursor = func(*args, **kwargs)
			return self

		return method

	def _cursor_iterable(self):
		return isinstance(self.cursor, Cursor) \
			or isinstance(self.cursor, CommandCursor)

	def _document(self, data):
		return Document(self.collection, data)

	def find_by(self, **kwargs):
		self.cursor = self.collection.find(kwargs)
		return self

	def raw(self):
		return self.cursor

	def one(self):
		if isinstance(self.cursor, dict):
			return self._document(self.cursor)

		elif self.cursor == None:
			return {}

		else:
			raise Exception("return type is not 'dict'")
	
	def first(self):
		if self._cursor_iterable():
			return self._document(list(self.cursor)[0])

		elif isinstance(self.cursor, dict):
			return self.one()

		elif self.cursor == None:
			return {}

		else:
			raise Exception("return type is '%s'" %s (type(self.cursor)))

	def all(self):
		documents = []
		if self._cursor_iterable():
			for i in self.cursor:
				documents.append(self._document(i))

		elif self.cursor == None:
			return []

		else:
			raise Exception("return type is '%s'" % (type(self.cursor)))
			
		return documents