from click import echo, style
import sqlalchemy as sa
from app import common, connection_ul, connection_fl, connection,data_sourses
from sqlalchemy import text
import datetime
import decimal
import json

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


def Data_Construct(csource:str, cparameters:str):
	source = json.loads(csource)
	#print(cparameters.replace("""'""",'"'))
	parameters = json.loads(cparameters)
	#prnt(source)
	prnt(parameters)
	print(type(parameters[0]))
	#for srow in source:
	#	prnt(srow)
	#print(parameters.keys())

	return ''
	print()
	val = json.loads(cparameters)
	print(type(val))
	print(json.loads(val[0]))
	return ''