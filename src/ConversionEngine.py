# Imports
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

import re
import copy

### Unit converstion

def mm_to_inches_unit(value):
	# create a unit'ed object from the raw value
	mm_value = value * ureg.millimeter

	# perform the conversion and return
	return mm_value.to(ureg.inch).magnitude

def gram_meter_squared_to_lbs_acre_unit(value):
	# create a unit'ed object from the raw value
	g_m2_value = value * ureg('gram/meter**2')

	# preform the conversion and return
	return g_m2_value.to('pound/acre').magnitude

### Data Conversion functions

def mm_to_inch(json_data):
	"""
	"""
	for variable in json_data.keys():
		if re.match(".*-mm", variable):
			# All keys that indicate variables in mm to be converted to inches
			sections = ['lower', 'mean', 'median', 'upper']
			for section in sections:
				mm_values = json_data[variable][section]
				inches_values = [ mm_to_inches_unit(mm_value) for mm_value in mm_values]
				json_data[variable][section] = inches_values


def gram_meter_squared_to_lbs_acre(json_data):
	"""
	"""
	for variable in json_data.keys():
		if re.match(".*g_m2.*", variable):
			# All keys that indicate variables in grams per meter^2 to be converted
			sections = ['lower', 'mean', 'median', 'upper']
			for section in sections:
				g_m2_values = json_data[variable][section]
				lbs_acre_values = [ gram_meter_squared_to_lbs_acre_unit(g_m2_value) for g_m2_value in g_m2_values]
				json_data[variable][section] = lbs_acre_values


_conversions = [gram_meter_squared_to_lbs_acre, mm_to_inch]

def convert(json_data):
	"""
	"""
	json_data_copy = copy.deepcopy(json_data)
	for conversion in _conversions:
		conversion(json_data_copy)

	return json_data_copy