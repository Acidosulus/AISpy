from click import echo, style
import sqlalchemy as sa
from app import common, connection_ul, connection_fl
from sqlalchemy import text

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

def Points_WithOut_Displays(year, month:int):
	print((connection_ul.execute(text("""select row_id as row_id from stack.[Договор];""")).fetchall()))
	pass