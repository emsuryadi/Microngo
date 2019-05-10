from math import ceil

class Pagination(object):
	def __init__(self, query, page, per_page, total, items):
		self.query		= query
		self.page		= page
		self.per_page	= per_page
		self.total		= total
		self.items		= items

	@property
	def pages(self):
		'''The total number of pages'''
		return int(ceil(self.total / float(self.per_page)))

	@property
	def next_num(self):
		'''The next page number.'''
		return self.page + 1

	def has_next(self):
		'''Returns ``True`` if a next page exists.'''
		return self.page < self.pages

	@property
	def prev_num(self):
		'''The previous page number.'''
		return self.page - 1

	def has_prev(self):
		'''Returns ``True`` if a previous page exists.'''
		return self.page > 1