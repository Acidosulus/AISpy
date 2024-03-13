from fastapi import FastAPI
from typing import List
from app import connection  # Подключение к базе данных, подразумевается, что оно уже сделано
from sqlalchemy import text
from click import echo, style
import sqlalchemy as sa
from app import common, connection_ul, connection_fl, connection
from sqlalchemy import text
import datetime
import decimal


app = FastAPI()


def get_queryresult_header_and_data(query_result):
	result = []
	
	for v in query_result:
		drow = {}
		for count, value in enumerate(v._fields):
			if isinstance(v[count], datetime.date):
				drow[value] = v[count].isoformat()
			else:
				if isinstance(v[count], decimal.Decimal):
					drow[value] = float(v[count])
				else:
					drow[value] = (v[count] if v[count]!=None else '')
			#print(v[count], '    ->    ', type(v[count]), )
		result.append(drow)
	
	headers = []
	if len(result)>0:
		headers = list(result[0].keys())
	return headers, result	



def get_reports_hierarchy(start_id:int) -> list:
	result, rez = [], []
	counter = 0
	while start_id is not None or start_id != -10:
		query_result = connection.execute(text(f"""--sql
														select name, parent, persistent_id as row_id  from page_items_list where persistent_id={start_id};
  														----------------------------------------------------------------------------------------------------------------------------------------------------
												;""")).fetchall()
		head, data = get_queryresult_header_and_data(query_result)
		try:
			start_id = data[0]['parent']
			result.append({'parent':data[0]['parent'], 'name':data[0]['name'], 'row_id':data[0]['row_id']})
			counter += 1
		except:
			break
	result = list(reversed(result))
	for i, row in enumerate(result):
		row['indent'] = '&nbsp;'*i*3
		row['counter'] = i
		rez.append(row)
	return rez

@app.get("/get_reports_hierarchy/")
async def read_root(start_id: int):
    return {"reports_hierarchy": get_reports_hierarchy(start_id)}

