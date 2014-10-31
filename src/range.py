class Range:
	""" Simple linked-list class to aggregate intervals """
	def __init__(self):
		self.head = None
		self.tail = None

	def insert(self, interval):
		""" simple since we are only adding 'increased' intervals """
		if not self.head and not self.tail:
			self.head = interval
			self.tail = interval
		elif interval.start <= (self.tail.end + 1):
			self.tail.end = interval.end
		else:
			self.tail.next = interval
			self.tail = interval

class Interval:
	""" Simple class as linked-list node for interval """
	def __init__(self, start, end):
		self.start = start # start day (int)
		self.end = end # end day (int)
		self.next = None # Next Interval node

