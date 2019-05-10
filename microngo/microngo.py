from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.command_cursor import CommandCursor
from microngo.pagination import Pagination

class Microngo(object):
	def __init__(self, *args, **kwargs):
		'''
		:param str db: Database name. This param is optional, you can use :func:`~microngo.Microngo.database` to set current database.
		:type db: str or None
		'''

		self.collection	= None
		self._db_name	= None
		self.db			= None

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
		'''Set current database

		:param str database: Database name
		:return: :class:`~microngo.Microngo`
		'''

		self.db = self.client[database]
		return self

	def _collection(self, collection):
		if self.db:
			self.collection = self.db[collection]
			return self.collection 
		else:
			raise Exception("database not found, please set database name.")

	def query(self, collection):
		'''Create query object

		:param str collection: Collection name
		:return: :class:`~microngo.Query`
		'''

		return Query(self._collection(collection))
	
	def insert(self, collection):
		'''Insert into collection

		:param str collection: Collection name
		:return: :class:`~microngo.Document`
		'''

		return Document(self._collection(collection))

class Document(object):
	def __init__(self, collection, data=None):
		'''
		:param obj collection: PyMongo collection object
		:param str data: Data for document
		:type data: dict or None
		'''

		# Variables
		self._microngo_collection	= collection
		self._microngo_payloads		= []
		self._microngo_document_id	= None

		# Dict data
		if data:
			if isinstance(data, dict):
				# Set documen id if exist
				if data.get("_id"):
					self._microngo_document_id = data.get("_id")
				# Update data
				self.__dict__.update(data)

	def __getattr__(self, name):
		return None

	def _get_payloads(self):
		# Get self variable in dictionary
		payloads = dict(self.__dict__)

		# Remove internal variables and return data
		del payloads['_microngo_collection']
		del payloads['_microngo_payloads']
		del payloads['_microngo_document_id']
		return payloads

	def _clear_payloads(self):
		# Cache variable
		cache_collection	= self._microngo_collection
		cache_payloads		= self._microngo_payloads
		cache_document_id	= self._microngo_document_id
		
		# Clear self variables
		payloads = self.__dict__
		payloads.clear()
		
		# Reasign internal variables from cache
		payloads['_microngo_collection']	= cache_collection
		payloads['_microngo_payloads']		= cache_payloads
		payloads['_microngo_document_id']	= cache_document_id
		return self

	def add(self):
		'''
		Add document to list, then insert to collection with insert_many function.
		'''

		if not self._microngo_document_id:
			# Get payloads
			payloads = self._get_payloads()

			# Append to cache
			self._microngo_payloads.append(payloads)

			# Clear previous payload and return
			self._clear_payloads()
			return self

	def raw(self):
		'''
		Get raw data or dict from document.

		:return: dict
		'''

		return self._get_payloads()

	def save(self):
		'''
		Save document to collection.

		:return: list of OjectId or single ObjectId
		'''

		if self._microngo_document_id:
			# Update
			self._microngo_collection.update_one(
				{'_id': self._microngo_document_id},
				{'$set': self._get_payloads()},
				upsert=False
			)
			return self._microngo_document_id
		else:
			# Insert
			if len(self._microngo_payloads) > 0:
				data = self._microngo_payloads
				return self._microngo_collection.insert_many(data).inserted_ids
			else:
				data	= self._get_payloads()
				doc_id	= self._microngo_collection.insert_one(data).inserted_id
				self._microngo_document_id = doc_id
				return doc_id

	def remove(self):
		'''
		Remove document from collection.
		'''

		if self._microngo_document_id:
			# Delete
			self._microngo_collection.delete_one({'_id': self._microngo_document_id})

class Query(object):
	def __init__(self, collection, cursor=None):
		'''
		:param obj collection: PyMongo collection object
		:param obj cursor: PyMongo cursor object
		:type cursor: obj or None
		'''

		self.collection = collection
		self.cursor		= cursor

	def __getattr__(self, name):
		# Handle pymongo collection's method
		def method(*args, **kwargs):
			if self._cursor_iterable():
				func = getattr(self.cursor, name)
			else:
				func = getattr(self.collection, name)
			
			self.cursor = func(*args, **kwargs)
			return self

		return method

	def _cursor_iterable(self):
		# Is cursor iterable
		return isinstance(self.cursor, Cursor) \
			or isinstance(self.cursor, CommandCursor)

	def _document(self, data):
		# Create document object
		return Document(self.collection, data)

	def find_by(self, **kwargs):
		'''
		:return: :class:`~microngo.Query`
		'''

		self.cursor = self.collection.find(kwargs)
		return self

	def raw(self):
		'''
		Get raw result.

		:return: raw result from PyMongo
		'''
		return self.cursor

	def one(self):
		'''
		Get single document.
		
		:return: :class:`~microngo.Document` or None
		:raises Exception: if the result type isn't dict
		'''

		if isinstance(self.cursor, dict):
			return self._document(self.cursor)

		elif self.cursor == None:
			return {}

		else:
			raise Exception("cursor type is '%s'" % (type(self.cursor)))
	
	def first(self):
		'''
		Get first document from list or from single document result.
		
		:return: :class:`~microngo.Document` or None
		:raises Exception: if the result type isn't dict and not iterable
		'''

		if self._cursor_iterable():
			data = list(self.cursor)
			if len(data) > 0:
				return self._document(data[0])
			else:
				return {}

		elif isinstance(self.cursor, dict):
			return self.one()

		elif self.cursor == None:
			return {}

		else:
			raise Exception("cursor type is '%s'" % (type(self.cursor)))

	def all(self):
		'''
		Get all document in list.
		
		:return: list of :class:`~microngo.Document` or []
		:raises Exception: if the result is not iterable
		'''

		documents = []
		if self._cursor_iterable():
			for i in self.cursor:
				documents.append(self._document(i))

		elif self.cursor == None:
			return []

		else:
			raise Exception("cursor type is '%s'" % (type(self.cursor)))

		return documents

	def paginate(self, page, per_page=20):
		'''
		Crate pagination query
		
		:return: :class:`~microngo.Pagination` or None
		'''
		if page < 1:
			return None

		total = self.cursor.count()
		items = self.skip((page - 1) * per_page).limit(per_page).all()

		if len(items) < 1 and page != 1:
			return None

		return Pagination(self, page, per_page, total, items)