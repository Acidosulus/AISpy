from fastapi import FastAPI, Request, Response, HTTPException
from starlette.responses import PlainTextResponse

from typing import List
from sqlalchemy import text
from click import echo, style
import sqlalchemy as sa
from sqlalchemy import text
import datetime
import decimal
from starlette.requests import Request
from starlette.responses import PlainTextResponse

import os
basedir = os.path.abspath(os.path.dirname(__file__))
import configparser  # импортируем библиотеку
import pprint
from click import echo, style

printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

import data_sourses

from pydantic import BaseModel
from datetime import date

app = FastAPI()




@app.post("/Agreement_Data/")
async def Agreement_Data(row_id:int):
    return f'"data":{data_sourses.Agreement_Data(row_id)}'

@app.post("/Agreements_Search_Data/")
async def Agreements_Search_Data(search_string:str):
    return f'"data":{data_sourses.Agreements_Search_Data(search_string)}'


class DateRange(BaseModel):
    from_date: date
    to_date: date

@app.post("/Pays_from_date_to_date/")
async def Pays_from_date_to_date(date_range: DateRange):
	print( type(date_range)) 
	print( f'"data":{data_sourses.Pays_from_date_to_date(date_range)}')
	return ''





@app.route("/", include_in_schema=False)
async def default_handler(request: Request) -> Response:
    return PlainTextResponse("Hello from default handler")