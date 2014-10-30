# Imports
from event import Event
import re

### Helper functions


### Rules functions

def sidedress_window(json_data):
	"""
	"""
	id = 1
	phenology = json_data['phenology']
	start_date = phenology['r5']
	end_date = phenology['r5.5']
	metadata = [start_date, end_date]

	yield Event(id, metadata)


_rules = [sidedress_window]

def run_rules(json_data):
	"""
	"""
	events = {'events': []}
	for rule in _rules:
		for event in rule(json_data):
			events['events'].append(event.to_json())

	return events