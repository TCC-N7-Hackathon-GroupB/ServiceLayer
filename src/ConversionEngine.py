# Imports
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

import re

### Unit converstion

def gram_meter_squared_to_lbs_acre_unit(value):
	# create a unit'ed object from the raw value
	g_m2_value = value * ureg('gram/meter**2')

	# preform the conversion and return
	return g_m2_value.to('pound/acre').magnitude

### Data Conversion functions

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


_conversions = [gram_meter_squared_to_lbs_acre]

def convert(json_data):
	"""
	"""
	for conversion in _conversions:
		conversion(json_data)

	return json_data