# Imports
from event import Event
from range import Range, Interval
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
	metadata = {
		"start_date": start_date,
		"end_date": end_date
	}

	yield Event(id, metadata)

def weather_event(json_data):
	"""
	"""
	id = 2

	precip_values = json_data['precip-mm']['median']
	available_n_values = json_data['available-n-g_m2']['median']

	day_range = 10

	start_index = 0
	end_index = start_index + day_range
	max_index = min(len(precip_values), len(available_n_values))

	interval_range = Range()

	while(end_index < max_index):
		n_loss = available_n_values[end_index] - available_n_values[start_index]
		precip_sum = sum(precip_values[start_index:end_index])

		if n_loss > 5 and precip_sum > .5:
			interval_range.insert(Interval(start_index, end_index))

		start_index += 1
		end_index += 1

	current_interval = interval_range.head
	while current_interval:
		metadata = {
			"n_loss": available_n_values[current_interval.end] - available_n_values[current_interval.start],
			"precip_sum": sum(precip_values[current_interval.start:current_interval.end]),
			"start_day": current_interval.start,
			"end_day": current_interval.end
		}

		yield Event(id, metadata)
		current_interval = current_interval.next


def stress(json_data):
	"""
	"""
	id = 3
	stress_values = json_data['crop-n-stress-_']['median']

	index = 0

	while index < len(stress_values):
		if stress_values[index] < .5:
			days_of_stress = 0
			index += 1
			while index < len(stress_values) and stress_values[index] < .5:
				days_of_stress += 1
				index += 1

			if days_of_stress > 6:
				metadata = {
					"start_day": index - days_of_stress - 1,
					"end_day": index - 1
				}

				yield Event(id, metadata)
		index += 1


_rules = [sidedress_window, weather_event, stress]

def run_rules(json_data):
	"""
	"""
	events = {'events': []}
	for rule in _rules:
		for event in rule(json_data):
			events['events'].append(event.to_json())

	return events