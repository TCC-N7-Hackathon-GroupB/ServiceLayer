class Event:
    """A simple event class"""
    def __init__(self, id, metadata):
    	self.id = id
    	self.metadata = metadata

    def to_json(self):
    	return {
    		"id": self.id,
    		"metadata": self.metadata
    	}