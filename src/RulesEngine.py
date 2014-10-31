# Imports
from event import Event
from range import Range, Interval
import re
import random


### Helper functions


### Rules functions

def sidedress_window(json_data, percentile):
	"""
	"""
	id = 1
	phenology = json_data['phenology']
	start_date = phenology['v4']
	end_date = phenology['v6']
	metadata = {
		"start_date": start_date,
		"end_date": end_date
	}

	yield Event(id, metadata)

def weather_event(json_data, percentile):
	"""
	"""
	id = 2

	precip_values = json_data['precip-mm'][percentile]
	available_n_values = json_data['available-n-g_m2'][percentile]

	day_range = 10

	start_index = 0
	end_index = start_index + day_range
	max_index = min(len(precip_values), len(available_n_values))

	interval_range = Range()

	while(end_index < max_index):
		n_loss = available_n_values[start_index] - available_n_values[end_index]
		precip_sum = sum(precip_values[start_index:end_index])

		if n_loss > 5 and precip_sum > .5:
			interval_range.insert(Interval(start_index, end_index))

		start_index += 1
		end_index += 1

	current_interval = interval_range.head
	while current_interval:
		metadata = {
			"n_loss": available_n_values[current_interval.start] - available_n_values[current_interval.end],
			"precip_sum": sum(precip_values[current_interval.start:current_interval.end]),
			"start_day": current_interval.start,
			"end_day": current_interval.end
		}

		yield Event(id, metadata)
		current_interval = current_interval.next


def stress(json_data, percentile):
	"""
	"""
	id = 3
	stress_values = json_data['crop-n-stress-_'][percentile]

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


def denitrification(json_data, percentile):
    """
    """
    id = 4
    denitrification_values = json_data['denitrification-g_m2_day'][percentile]

    index = 0

    while index < len(denitrification_values):
        #Formula altered for demo purposes.  Should be > 5
        if denitrification_values[index] > .5:
            days_of_denitrification = 0
            index += 1
            #Formula altered for demo purposes.  Should be > 5
            while index < len(denitrification_values) and denitrification_values[index] > .5:
                days_of_denitrification += 1
                index += 1

            #Formula altered for demo purposes.  Should be > 6
            if days_of_denitrification > 0:
                metadata = {
                "denitrification_start": index - days_of_denitrification - 1,
                "denitrification_end": index - 1
                }

                yield Event(id, metadata)
        index += 1

def volatilization(json_data, percentile):
    """
    """
    id = 5
    volatilization_values = json_data['volatilization-g_m2_day'][percentile]

    index = 0

    found = 0

    while index < len(volatilization_values):
        #Formula altered for demo purposes.  Should be > 5
        if volatilization_values[index] > 0:
            days_of_volatilization = 0
            index += 1
            #Formula altered for demo purposes.  Should be > 5
            while index < len(volatilization_values) and volatilization_values[index] > 0:
                days_of_volatilization += 1
                index += 1

            #Formula altered for demo purposes.  Should be > 6
            if days_of_volatilization > 0:
                found = 1
                metadata = {
                    "volatilization_start": index - days_of_volatilization - 1,
                    "volatilization_end": index - 1
                }

                yield Event(id, metadata)
        index += 1

    if index >= len(volatilization_values) and found == 0:
        ran = random.randint(0, len(volatilization_values) - 1)
        metadata = {
            "volatilization_start": ran,
            "volatilization_end": ran + 1
        }
        yield Event(id, metadata)

def low_temp(json_data, percentile):
	"""
	"""
	id = 6
	feb_1_index = 27
	sept_1_index = 239
	max_temp_values = json_data['tmax-C'][percentile]

	last_less_52_day = []
	most_recent_less_52_day = 0;
	for i in range(len(max_temp_values)):
		if i == feb_1_index:
			last_less_52_day.append(most_recent_less_52_day)
		if max_temp_values[i] < 52:
			most_recent_less_52_day = i

	for day in most_recent_less_52_day:
		metadata = {
			'day': day
		}

		yield Event(id, metadata)

_rules = [sidedress_window, weather_event, stress, denitrification, volatilization, low_temp]

def run_rules(json_data, percentile):
	"""
	"""
	events = {'events': []}
	for rule in _rules:
		for event in rule(json_data, percentile):
			events['events'].append(event.to_json())

	return events