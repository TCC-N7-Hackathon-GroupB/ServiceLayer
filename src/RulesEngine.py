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

	while(end_index < max_index):
		n_loss = available_n_values[end_index] - available_n_values[start_index]
		precip_sum = sum(precip_values[start_index:end_index])

		if n_loss > 5 and precip_sum > .5:
			metadata = {
				"n_loss": n_loss,
				"precip_sum": precip_sum,
				"start_index": start_index,
				"end_index": end_index
			}

			yield Event(id, metadata)

		start_index += 1
		end_index += 1


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
					"stress_start": index - days_of_stress - 1,
					"stress_end": index - 1
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