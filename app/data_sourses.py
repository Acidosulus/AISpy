from app import app, db, models,connection_fl, connnection_ul, dialogs
from click import echo, style
import sqlalchemy as sa
from common import RowToDict, RowsToDictList

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

def Points_WithOut_Displays(year, month:int):
	print(RowsToDictList(connnection_ul.execute("""select Номер from stack.[Договор];""").fetchall()))
	pass