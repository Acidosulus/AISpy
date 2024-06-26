print(f'data_sourses imported to {__name__}')
from common import connection_ul, connection, session, session_ul
from click import echo, style
import sqlalchemy as sa
import datetime
from sqlalchemy import text
import datetime
import decimal
import json
import pandas
import os
import models
import time
import asyncio




import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint





from click import echo, style
import sqlalchemy as sa
from sqlalchemy import text
import datetime
import decimal



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

import configparser  # импортируем библиотеку
import pprint
from click import echo, style

printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

if __name__ == '__main__':
	pass
# else:
	# from app import connection_ul

# module init for cases it work without flask server
def init():
	global connection
	try:
		from app import connection
		print('import connection from app success')
	except:
		print('import connection from app failed')
	echo(style(text = 'Force init of data_sourses module', bg='red', fg='bright_yellow'))
	global basedir, config, connection_url_fl, connection_url_ul, connection_fl, connection_ul, engine_ul, engine_fl
	basedir = os.path.abspath(os.path.dirname(__file__))
	config = configparser.ConfigParser()
	config.read("settings.ini", encoding='UTF-8')

	from sqlalchemy.engine import URL
	connection_url_fl = URL.create(
		config['login_fl']['ENGINE'],
		username=config['login_fl']['USERNAME'],
		password=config['login_fl']['PASSWORD'],
		host=config['login_fl']['SERVER'],
		port=config['login_fl']['PORT'],
		database=config['login_fl']['DATABASE'],
		query={
			"driver": config['login_fl']['DRIVER'],
			"TrustServerCertificate": "yes",
			"extra_params": "MARS_Connection=Yes"	},
	)
	connection_url_ul = URL.create(
		config['login_ul']['ENGINE'],
		username=config['login_ul']['USERNAME'],
		password=config['login_ul']['PASSWORD'],
		host=config['login_ul']['SERVER'],
		port=config['login_ul']['PORT'],
		database=config['login_ul']['DATABASE'],
		query={
			"driver": config['login_ul']['DRIVER'],
			"TrustServerCertificate": "yes",
			"extra_params": "MARS_Connection=Yes"	},
	)

	from sqlalchemy import create_engine
	engine_ul = create_engine(connection_url_ul)
	engine_fl = create_engine(connection_url_fl)
	connection_ul = engine_ul.connect()
	connection_fl = engine_fl.connect()




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
			#print(v[count], '	->	', type(v[count]), )
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

def get_addresses_hierarchy(start_id:int) -> list:
	result, rez = [], []
	counter = 0
	while start_id is not None and start_id>0:
		query_result = connection_fl.execute(text(f"""--sql
														select stack.[AddrLs](row_id,0) as name, [Счета] as parent, row_id  from stack.[Лицевые счета] where [row_id]={start_id};
  														----------------------------------------------------------------------------------------------------------------------------------------------------
												;""")).fetchall()
		head, data = get_queryresult_header_and_data(query_result)
		print('get_addresses_hierarchy ')
		print('start_id:', start_id)
		print(data)
		start_id = data[0]['parent']
		result.append({'parent':data[0]['parent'], 'name':data[0]['name'], 'row_id':data[0]['row_id']})
		counter += 1
	result = list(reversed(result))
	for i, row in enumerate(result):
		row['indent'] = '&nbsp;'*i*3
		row['counter'] = i
		rez.append(row)
	print(rez)
	return rez

def get_agreements_hierarchy(start_id:int) -> list:
	result, rez = [], []
	counter = 0
	while start_id is not None and start_id>0:
		query_result = session_ul.execute(text(f"""--sql
										   				select [Папки] as parent, [Примечание] as name, row_id as row_id, [Номер] from stack.[Договор] where row_id = {start_id}
  														----------------------------------------------------------------------------------------------------------------------------------------------------
												;""")).fetchall()
		head, data = get_queryresult_header_and_data(query_result)
		print(data)
		start_id = data[0]['parent']
		# for agreement number name must be number
		if len(str(data[0]['Номер']))==10:
			data[0]['name']=data[0]['Номер']
		result.append({'parent':data[0]['parent'], 'name':data[0]['name'], 'row_id':data[0]['row_id']})
		counter += 1
	result = list(reversed(result))
	for i, row in enumerate(result):
		row['indent'] = '&nbsp;'*i*3
		row['counter'] = i
		rez.append(row)
	print(rez)
	return rez


def Data_For_Addresses_List(parent_id:int) -> list:
	query_result = connection_fl.execute(text(f"""--sql
											select 	stack.[AddrLs](ls.row_id,0) as address,
														ls.row_id,
														trim(str(ls.Номер)) as number,
														CASE
															when len(ls.[Номер])<10
								  								then coalesce((select sum(1) from stack.[Лицевые счета] as lss where ls.row_id=lss.[Счета]),0)
															else 0
														END as descendants_count
												from stack.[Лицевые счета] as ls
												where ls.[Счета]={parent_id};
  ----------------------------------------------------------------------------------------------------------------------------------------------------
;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def Data_For_Agreements_List(parent_id:int) -> list:
	query_result = session_ul.execute(text(f"""--sql
												select *
													from (
																	select
																		agr.row_id,
																		agr.[Папки] as folder_id,
																		case
																			when len(agr.[Номер])<10 then ''
																			else agr.[Номер]
																		end as number,
																		CASE
																			when len(agr.[Номер])<10 then coalesce((select sum(1) from stack.[Договор] as agrs where agr.row_id=agrs.[Папки]),0)
																			else 0
																		END as descendants_count,
																		case
																			when len(agr.[Номер])<10 then agr.[Примечание]
																			else trim(org.[Наименование]) + trim(agr.[Примечание])
																		end as name,
																		org.[ИНН] as inn,
																		org.[КПП] as kpp
																	from stack.[Договор] as agr
																	left join stack.[Организации] as org on org.row_id = agr.[Грузополучатель]
																	where agr.[Папки]={parent_id})
															as ct
													order by number, name;
												----------------------------------------------------------------------------------------------------------------------------------------------------
												;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def Points_WithOut_Displays(parameters:dict):
	year = parameters['year']
	month = parameters['month']
	query_result = session_ul.execute(text(f"""--sql
DECLARE @dateendofmonth datetime = EOMONTH('{year}-{month}-01')
select
	statuses.status as [Состояние ПУ],
	lo.[ЗаводскойНомер] as [ЗаводскойНомер],
	nk.[Наименование] as [Тип ПУ],
	ls.[Номер] as [Номер ТУ],
	ls.[АдресЛС] as [Адрес ТУ],
	ls.[Примечание] as [Название ТУ],
	agr.[Номер] as [Номер договора],
	agr.[Тема] as [Доп. номер договора],
	org.[Название],
	staff1.[ФИО],
	statuses.status as [Статус ПУ],
	folders.folder as [Участок], folders.area as [Отделение]
  from   stack.[Список объектов] as lo
  inner join (select pus.*,
	  case
			  when pus.[Состояние]=0 then 'Не используется'
			  when pus.[Состояние]=1 then 'Работает'
			  when pus.[Состояние]=2 then 'По среднему'
			  when pus.[Состояние]=3 then 'Отключен ввод'
			  else ''
   end as status
  from stack.[Состояние счетчика] as  pus where (getdate() between pus.[ДатНач] and pus.[ДатКнц])) as statuses on statuses.[Объект-Состояние]=lo.row_id
  inner join (select * from stack.[Номенклатура]) as nk on nk.row_id = lo.[Номенклатура-Объекты]
  inner join stack.[Лицевые счета] as ls on ls.row_id = lo.[Объекты-Счет]
  inner join (select * from stack.[Лицевые договора] where getdate() between [ДатНач] and [ДатКнц]) as ld on  ls.row_id = ld.Лицевой
  inner join stack.[Договор] as agr on agr.row_id = ld.[Договор]
  inner join stack.[Организации] as org on org.row_id = agr.[Грузополучатель]
  left join stack.[Сотрудники] as staff1 on staff1.ROW_ID = agr.Сотрудник1
  left join (select *
				from stack.[Показания счетчиков]
				where
								[Показания-Услуга]=14
						and 	month([Расчетный месяц]) = month(@dateendofmonth)
						and 	year([Расчетный месяц]) = year(@dateendofmonth)
						and 	[Дата]=@dateendofmonth) as lastdisplays on lastdisplays.[Показания-счет] = ls.row_id
	left join (		select  stack.[Договор].[Номер] as nc, folders.[Примечание] as folder, folders.area
			from stack.[Договор]
			left join (select sp.row_id, sp.Папки, sp.Примечание, COALESCE (pp.[Примечание], sp.[Примечание]) as area
							from stack.[Договор] sp
							left join (select *
											from stack.[Договор]
											where [Папки] = 80540
										) as pp on pp.row_id = sp.[Папки]
			where (sp.Папки_ADD=0 and sp.Заказчик>0) or sp.Папки=-10 ) as folders
			on folders.[row_id] = stack.[Договор].Иерархия2
			where len(stack.[Договор].[Номер])>=10) as folders on folders.nc = agr.[Номер]
  where lastdisplays.[Показание] is  null;
  ----------------------------------------------------------------------------------------------------------------------------------------------------
;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Points_with_Constant_Consuming(parameters:dict):
	year = parameters['year']
	month = parameters['month']
	query_result = session_ul.execute(text(f"""--sql
	declare 	@datn date = '{year}-{month}-01' ,	@datk date = EOMONTH('{year}-{month}-01')
					 Select distinct * from (
									   select 	left(dog.Номер,10) as [Номер договора],
									   			left(org.Название,250) as [Название договора],
											  	ls.Номер as [ТУ],
												left(ls.[Примечание],250) as [Название ТУ],
												'"'+left(nom.Наименование,250) as [ПУ],
											  	left(so.ЗаводскойНомер,50) as [Заводской номер],
											  	ps.Показание as [Показание],
												left(d.Отделение,50) as [Отделение],
												left(d.Участок,50) as [Участок],
												so.Тарифность as [Тарифность],
											  	left(staff1.ФИО, 70) as [ФИО отвественного],
												networkowner.name as [Сетевая организация]
									   from stack.contracts(-1) d
									   join stack.Договор dog on dog.ROW_ID=d.Договор
												 and dog.[Начало договора]<=@datk
												 and dog.[Окончание]>=@datn
									   left join stack.[Сотрудники] as staff1 on staff1.ROW_ID = dog.Сотрудник1
									   join stack.Организации org on org.ROW_ID = dog.Плательщик
									   join stack.[Лицевые договора] ld on ld.Договор = d.Договор
									   		  and (ld.ДатНач<=@datk or ld.ДатНач is null)
													 and (ld.ДатКнц>=@datn or ld.ДатКнц is null)
									   join stack.[Лицевые счета] ls on ls.ROW_ID = ld.Лицевой
									   join stack.[Список объектов] so on so.[Объекты-Счет] = ld.Лицевой
												 and (so.ДатНач<=@datk or so.ДатНач is null)
												 and (so.ДатКнц>=@datn or so.ДатКнц is null)
												 and so.ЗаводскойНомер = 'прасход'
									   join stack.Номенклатура nom on nom.ROW_ID = so.[Номенклатура-Объекты] and nom.Идентификатор=0
									   left join stack.[Показания счетчиков] ps on ps.[Объект-Показания] = so.ROW_ID
												 and ps.тип=1
												 and ps.[Расчетный месяц] between @datn and @datk
										left join (select left(ls.Номер,10) as num_point, left(org.Название,250) as name
														from stack.[Лицевые счета] ls
															left join stack.[Поставщики]  ps on ps.[Счет-Список поставщиков] = ls.ROW_ID  and (@datk between ps.ДатНач and ps.ДатКнц) and ps.[Услуги-Список поставщиков] = 14
															left join stack.[Организации] org on ps.[Поставщики-Список] = org.ROW_ID) networkowner on networkowner.num_point = ls.Номер
										) ct
							order by [Номер договора], [ТУ] ;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Pays_from_date_to_date(parameters):
	query_result = session_ul.execute(text(f"""--sql
		select 	left(agr.Номер,10) as [Договор],
				left(org.Название,250) as [Название договора],
				left(staff1.ФИО,50) as [Расчеты],
				left(staff3.ФИО,50) as [Менеджер],
				left(doc.Примечание,250) as [Назначение платежа],
				doc.ПлатежС as [С],
				doc.ПлатежПо as [По],
				left(doc.Аналитика,20) as [Тип],
				doc.Дата as [Дата платежа],
				doc.Номер as [Номер п.п.],
				doc.Сумма as [Сумма]
			from stack.Документ doc
			left join stack.Договор  as agr on agr.ROW_ID  = doc.[Документы-Договор]
			left join stack.Организации as org on org.ROW_ID  = agr.Грузополучатель
			left join stack.[Сотрудники] as staff1 on staff1.ROW_ID = agr.Сотрудник1
			left join stack.[Сотрудники] as staff3 on staff3.ROW_ID = agr.Сотрудник3
			where 	doc.[Тип документа] = 21 AND
					(doc.Дата between convert(datetime,'{parameters['from']}',21) and convert(datetime,'{parameters['to']}',21)) and
					(agr.Номер is not null);""")).fetchall()
	# with open('Pays_from_date_to_date.txt', 'w') as file:
	# 	file.write(pprint.pformat(get_queryresult_header_and_data(query_result)))
	return get_queryresult_header_and_data(query_result)


def Agreement_Documents_List(row_id:int):
	query_result = session_ul.execute(text(f"""--sql
												SELECT 	doc.ROW_ID as row_id,
														doc.[Тип документа] as document_type,
														FORMAT(doc.[Дата], 'yyyy-MM-dd') as date,
														doc.Сумма as total_money,
														doc.Примечание as note,
														doc.[Полный номер] as number
												FROM stack.[Документ] as doc
												WHERE doc.[Тип документа] = 100 and doc.[Документы-Договор]={row_id};"""))
	return get_queryresult_header_and_data(query_result)


def Agreement_Data(row_id:int):
	query_result = session_ul.execute(text(f"""--sql
																	select
																			agr.row_id as agreement_id,
										   									agr.[Номер] as number,
																			agr.[Грузополучатель] as gr_row_id,
																			gr.[Наименование] as gr_name,
										   									gr.[Телефон] as phone,
										   									gr.[Адрес] as address,
										   									agr.[Адрес доставки] as address_delivery,
																			agr.[Плательщик] as pl_row_id,
																			pl.[Наименование] as pl_name,
																			agr.[Примечание] as note,
										   									agr.[Тип договора] as agr_type,
																			case agr.[Тип договора]
																				when 1 then 'договор энергоснабжения'
																				when 2 then 'договор купли-продажи'
																				when 3 then 'договор население (квитанции)'
																				when 4 then 'договор хозяйственные нужды'
																				when 5 then 'компенсация потерь сетевых компания'
																				when 6 then 'договор оказания услуг по передаче электрической энергии'
																				when 7 then 'договор купли-продажи в целях компенсации фактических потерь, возникающих в электрических сетях'
																				when 8 then 'договор купли-продажи электричкой энергии в целях компенсации потерь электрической энергии в электрических сетях'
																				else ''
																			end as agr_type_name,
																			CONVERT(date, agr.[Начало договора], 1 ) as agr_begin,
																			CONVERT(date, agr.[Окончание], 1 )  as agr_end,
																			CONVERT(date, agr.[Дата подписания], 1 )  as agr_sign_begin,
																			CONVERT(date, agr.[Дата расторжения], 1 )  as agr_sign_end,
										   									AgrTypes.[Название] as agr_VD_name,
										   									agr.[СправочникВД-Договоры] as agr_VD_id,
										   									category.[Название] as agr_category_name,
										   									agr.[Категория-Договоры] as agr_category_row_id,
										   									AgrOKVED.[Название] as agr_OKVED_name,
										   									budgets.name as agr_budget_name,
										   									agr.[Бюджет-Договоры] as ager_budget_row_id,
										   									municipalformation.name as municipalformation_name,
										   									municipalformation.row_id as municipalformation_row_id
																	from stack.[Договор] as agr
																		left join stack.[Организации] as gr on gr.row_id = agr.[Грузополучатель]
																		left join stack.[Организации] as pl on pl.row_id = agr.[Плательщик]
										   								left join (select row_id, [Название] from stack.[Классификаторы] where [Тип]=129) as AgrTypes on AgrTypes.row_id = agr.[СправочникВД-Договоры]
										   								left join stack.[Категории договоров] as category on category.row_id = agr.[Категория-Договоры]
										   								left join (select row_id, [Название] from stack.[Классификаторы]) as AgrOKVED on AgrOKVED.row_id = agr.[Отрасль-Договоры]
										   								left join (select 	row_id,
																							[Папки] as folder,
																							[Код] as code,
																							[Название] as name
																						from stack.[Классификаторы]
																						where 	[Папки] in (select row_id
																												from stack.[Классификаторы]
																												where	[Папки] in (select 	row_id
																																	from stack.[Классификаторы]
																																	where 	[Папки]=682)
																														or [Папки]=682 )
																								or [Папки]=682)
										   											as budgets on budgets.row_id = agr.[Бюджет-Договоры]
																		left join (	SELECT 	row_id,
										   													[Код] as code,
										   													[Название] as name
										   											FROM stack.[Классификаторы]
										   											WHERE [Папки] = (select top 1 row_id
										   																from stack.[Классификаторы]
										   																where [Тип]=128 and [Папки]<0))
										   											as municipalformation on municipalformation.row_id = agr.[СправочникМО-Договоры]
																	where agr.row_id={row_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Agreements_Search_Data(substring:str):
	query_result = session_ul.execute(text(f"""--sql
											select *
												from (
														select
															agr.row_id,
															agr.[Папки] as folder_id,
															case
																when len(agr.[Номер])<10 then ''
																else agr.[Номер]
															end as number,
															CASE
																when len(agr.[Номер])<10 then coalesce((select sum(1) from stack.[Договор] as agrs where agr.row_id=agrs.[Папки]),0)
																else 0
															END as descendants_count,
															case
																when len(agr.[Номер])<10 then agr.[Примечание]
																else trim(org.[Наименование]) + trim(agr.[Примечание])
															end as name,
															org.[ИНН] as inn,
															org.[КПП] as kpp
														from stack.[Договор] as agr
														left join stack.[Организации] as org on org.row_id = agr.[Грузополучатель]
														where 		agr.[Номер] like '%{substring}%'
																or	org.[Наименование] like '%{substring}%')
												as ct
										order by number, name
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def Agreement_Types_Data():
	query_result = session_ul.execute(text(f"""--sql
																	select 	row_id,
										   									[Название] as name
										   								from stack.[Классификаторы]
										   								where [Тип]=129 and [Код]>0
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Agreement_Parameters_Data(agreement_id:int):
	query_result = session_ul.execute(text(f"""--sql
													select	kinds.[Наименование] as name,
															options.[Значение] as value,
															options.[Примечание] as text,
															(case when GETDATE() between options.[ДатНач] and options.[ДатКнц] then 1 else 0 end) as active,
															convert(date, options.[ДатНач], 1) as date_begin,
															convert(date, options.[ДатКнц], 1) as date_end
														from stack.[Свойства] as options
														left join stack.[Виды параметров] as kinds on kinds.row_id = options.[Виды-Параметры]
														where 		options.[Параметры-Договор] = {agreement_id}
													;
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)




def Agreement_Payments_Schedule(agreement_id:int):
	query_result = session_ul.execute(text(f"""--sql
													select  convert(date, [Месяц], 1 ) as date_begin,
															convert(date, [МесяцПо],1) as date_end,
															[День платежа] as day ,
															[процентДоговорнойВеличины] as procent,
															(case when GETDATE() between [Месяц] and [МесяцПо] then 1 else 0 end) as active
														from stack.[График оплаты договора] as gr
														where [График-Договор]={agreement_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Budgets():
	query_result = session_ul.execute(text(f"""--sql
													select 	row_id,
															[Папки] as folder,
															[Код] as code,
															[Название] as name
														from stack.[Классификаторы]
														where 	[Папки] in (select row_id
																				from stack.[Классификаторы]
																				where	[Папки] in (select 	row_id
																									from stack.[Классификаторы]
																									where 	[Папки]=682)
																						or [Папки]=682 )
																or [Папки]=682;
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Ref_Agreement_Types():
	return ['row_id', 'name'], [	{'row_id':0, 'name':''},
									{'row_id':1, 'name':'договор энергоснабжения'},
									{'row_id':2, 'name':'договор купли-продажи'},
									{'row_id':3, 'name':'договор население (квитанции)'},
									{'row_id':4, 'name':'договор хозяйственные нужды'},
									{'row_id':5, 'name':'компенсация потерь сетевых компания'},
									{'row_id':6, 'name':'договор оказания услуг по передаче электрической энергии'},
									{'row_id':7, 'name':'договор купли-продажи в целях компенсации фактических потерь, возникающих в электрических сетях'},
									{'row_id':8, 'name':'договор купли-продажи электричкой энергии в целях компенсации потерь электрической энергии в электрических сетях'}]


def Ref_Organizaion_Vid():
	return ['row_id', 'name'], [	{'row_id':0, 'name':''},
									{'row_id':1, 'name':'Бюджет'},
									{'row_id':2, 'name':'Малый бизнес'},
									{'row_id':3, 'name':'Средний бизнес'},
									{'row_id':4, 'name':'Крупный бизнес'},
									{'row_id':5, 'name':'Микропредприятия'}	]

def Ref_Organizaion_Type():
	return ['row_id', 'name'], [	{'row_id':0, 'name':'ЮЛ'},
									{'row_id':1, 'name':'Физ.лицо'},
									{'row_id':2, 'name':'ИП'}	]

def Ref_Organizaion_NDS():
	return ['row_id', 'name'], [	{'row_id':0, 'name':'Плательщик'},
									{'row_id':1, 'name':'Не облагается'}	]

def Ref_Organizaion_Debtor_Category():
	return ['row_id', 'name'], [	{'row_id':0, 'name':'Прочие потребители/покупатели ЭЭ'},
									{'row_id':1, 'name':'ЖК, ТСЖ, ЖСК и прочие собственники помещений в МКД'},
									{'row_id':2, 'name':'УК, тепло- и водо- снабжающие организации'},
									{'row_id':3, 'name':'Бюджет'}	]





def Points_Data(agreement_row_id:int):
	query_result = session_ul.execute(text(f"""--sql
														select	ls.row_id,
																ls.[Номер] as number,
										   						ls.[Примечание] as name,
																ls.[АдресЛС] as address,
																voltages.service,
																netowners.name as netowner,
																pu.pu_number as pu_number,
																pu.pu_type_name as pu_type_name,
																categories.category_name,
																la.[Название] as anal_name
															from stack.[Лицевые счета] as ls
															left join ( select	stack.[Лицевые счета].row_id,
																			replace(left(service.[Услуга],3),':','') AS service
																		from  stack.[Лицевые счета]
																		LEFT JOIN (SELECT stack.[Список услуг].[Счет-Услуги],stack.[Типы услуг].[Название] AS [Услуга]
																			FROM stack.[Список услуг]
																			LEFT JOIN stack.[Типы услуг] ON stack.[Типы услуг].row_id = stack.[Список услуг].[Вид-Услуги]
																			WHERE (getdate() BETWEEN ДатНач AND ДатКнц) AND ДатНач >= convert(datetime,'2022-09-01',21)) service ON service.[Счет-Услуги] = stack.[Лицевые счета].row_id)
																			as voltages on voltages.row_id = ls.row_id
															left join (select ls.row_id, left(org.Название,250) as name
																		from stack.[Лицевые счета] ls
																		left join stack.[Поставщики] ps on ps.[Счет-Список поставщиков] = ls.ROW_ID  and ( getdate() between ps.ДатНач and ps.ДатКнц) and ps.[Услуги-Список поставщиков] = 14
																		left join stack.[Организации] org on ps.[Поставщики-Список] = org.ROW_ID )
																		as netowners on netowners.row_id = ls.row_id
															left join ( select obj.[Объекты-Счет] as point_id,
																				obj.[ЗаводскойНомер] as pu_number,
																				nm.[Наименование] as pu_type_name
																			from stack.[Список объектов] as obj
																			left join stack.[Номенклатура] as nm on nm.ROW_ID = obj.[Номенклатура-Объекты]
																			where 		nm.[Номенклатура-НСИ]>0
																					and getdate() between obj.[ДатНач] and obj.[ДатКнц]
																					and obj.[Объект-Услуга] = 14)
																		as pu on pu.point_id = ls.row_id
															left join (
																		select 	ls.row_id as point_id,
																				pr.Значение + 1 as category,
																				case pr.Значение
																					when 0 then 'Первая'
																					when 1 then 'Вторая'
																					when 2 then 'Третья'
																					when 3 then 'Четвертая'
																					when 4 then 'Пятая'
																					when 5 then 'Шестая'
																					ELSE ''
																				end as category_name
																			from
																			(select * from stack.[Свойства] where (getdate() between ДатНач and ДатКнц) and [Виды-Параметры] = (select row_id from stack.[Виды параметров] where [Название]='СОСТОЯНИЕ') and [Значение]=0) as used,
																			stack.[Лицевые счета] ls
																			left join (select * from stack.[Свойства] where (getdate() between ДатНач and ДатКнц) and [Виды-Параметры] = (select row_id from stack.[Виды параметров] where [Название]='ЦКАТЕГОРИЯ')) as pr on pr.[Счет-Параметры] = ls.row_id
																			where
																			ls.row_id = used.[Счет-Параметры] and
																			(pr.Значение is not null))
																		as categories on categories.point_id = ls.row_id
															left join stack.[Лицевых аналитики] as la on la.row_id = ls.[Счет-Аналитика1]
															where ls.ROW_ID  in (select ld.[Лицевой]
																					FROM stack.[Лицевые договора] as ld
																					where 	ld.[Договор]={agreement_row_id}
																						AND	getdate() between ld.[ДатНач] and ld.[ДатКнц]);
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Calc_Data(agreement_row_id:int, period:str):
	query_result = session_ul.execute(text(f"""--sql
													select 	dr.[Договор] as agr_id,
															dr.[Лицевой] as point_id,
															ls.[Номер] as point_number,
															ls.[Примечание] as point_name,
															tu.[Номер услуги] as usl_number,
															tu.[Наименование] as usl_name,
															dr.[Кол_во] as consuming,
															dr.[Тариф] as tariff,
															dr.[СуммаБезНДС] as money_withoutnds,
															dr.[Сумма] as money
														from stack.[Лицевые счета] as ls
														left join (select 	*
																from stack.[Детализация расчета]
																WHERE  		[Номер услуги]<=1999
										   								and	[Месяц] = '{period}-01'
										   								and [Месяц]=[ЗаМесяц])
															as dr on dr.[Лицевой] = ls.ROW_ID
														left join stack.[Типы услуг]
															as tu on tu.[Номер услуги]  = dr.[Номер услуги]
										   				where dr.[Договор]={agreement_row_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def All_Agreement_Numbers():
	query_result = session_ul.execute(text(f"""--sql
											select 	agr.[Номер] as agreement,
										   			'		  ' as point
												from stack.[Договор] as agr
												where len(agr.[Номер])=10
												order by agreement
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Opened_Agreement_Numbers():
	query_result = session_ul.execute(text(f"""--sql
											select 	agr.[Номер] as agreement,
										   			'		  ' as point
												from stack.[Договор] as agr
												where 		len(agr.[Номер])=10 and
															(Окончание is null or (getdate()<=Окончание)) and
															([Дата расторжения] is null or (getdate()<=[Дата расторжения]))
												order by agreement
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def Point_Numbers_of_Opened_Agreements():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															convert(varchar, ls.[Номер]) as point
														from (select * from stack.[Лицевые договора] where getdate() between [ДатНач] and [ДатКнц]) ld
														inner join (select * from stack.[Договор] where (Окончание is null or (getdate()<=Окончание)) and ([Дата расторжения] is null or (getdate()<=[Дата расторжения]))) as agr  on agr.row_id = ld.[Договор]
														inner join stack.[Лицевые счета] as ls on ls.row_id = ld.[Лицевой]
														order by point
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def All_Point_Numbers():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															convert(varchar, ls.[Номер]) as point
														from (select * from stack.[Лицевые договора] where getdate() between [ДатНач] and [ДатКнц]) ld
														inner join stack.[Договор] as agr on agr.row_id = ld.[Договор]
														inner join stack.[Лицевые счета] as ls on ls.row_id = ld.[Лицевой]
														order by point
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_Names():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[Название] as name
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_FSK():
	query_result = session_ul.execute(text(f"""--sql
														select 	agr.[Номер] as agreement,
																fsk.nc as agreement_fsk
															from stack.[Договор] as agr
															left join (select distinct left(agr.[Номер],10) as nc
																			from	stack.[Лицевые счета] ls,
																					stack.[Лицевые договора] ld,
																					stack.[Договор] agr
																			where   ls.ROW_ID  in (
																									select [Счет-Параметры]
																										from stack.[Свойства]
																										where   [Виды-Параметры] = (select row_id from stack.[Виды параметров] where [Название]='ФСК') AND
																										(getdate() between [ДатНач] and [ДатКнц])) and
																					(getdate()  between ld.ДатНач and ld.ДатКнц) and
																					agr.ROW_ID  = ld.[Договор] and
																					ls.row_id = ld.[Лицевой]) as fsk
															on fsk.nc = agr.Номер
															order by agreement
														;""")).fetchall()
	return get_queryresult_header_and_data(query_result)




def Get_Agreement_Id():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															agr.row_id as agreement_row_id
														from stack.[Договор] as agr
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_Address_gr():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[Адрес] as address_gr
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Address_Fact_gr():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[ФактАдрес] as address_fact_gr
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Address_pl():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[Адрес] as address_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Плательщик] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Address_Fact_pl():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[ФактАдрес] as address_fact_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Плательщик] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_Date_Begin():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															convert(date, agr.[Начало договора],1) as date_begin
														from stack.[Договор] as agr
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Date_Begin_Sign():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															convert(date, agr.[Дата подписания],1) as date_begin_sign
														from stack.[Договор] as agr
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Date_End():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															convert(date, agr.[Окончание],1) as date_end
														from stack.[Договор] as agr
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Date_End_Sign():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															convert(date, agr.[Дата расторжения],1) as date_end_sign
														from stack.[Договор] as agr
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def Get_Agreement_Phone_gr():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[Телефон] as phone_gr
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Phone_pl():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[Телефон] as phone_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Плательщик] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_INN_pl():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[ИНН] as inn_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Плательщик] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_KPP_pl():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[КПП] as kpp_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Плательщик] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_ORGN_pl():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[ОГРН] as ogrn_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Плательщик] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_INN_gr():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[ИНН] as inn_gr
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_KPP_gr():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[КПП] as kpp_gr
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_ORGN_gr():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															org.[ОГРН] as ogrn_gr
														from stack.[Договор] as agr
														inner join stack.[Организации] as org on agr.[Грузополучатель] = org.row_id
														order by agreement
										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)



def Get_Agreement_FIO():
	query_result = session_ul.execute(text(f"""--sql
														select
																				left(stack.[Договор].Номер,10) as agreement,
																				staff1.ФИО as fio1,
																				staff2.ФИО as fio2,
																				staff3.ФИО as fio3,
																				staff4.ФИО as fio4
																	from
																			stack.[Договор]
																	left join stack.[Сотрудники] as staff1 on staff1.ROW_ID = stack.[Договор].Сотрудник1
																	left join stack.[Сотрудники] as staff2 on staff2.ROW_ID = stack.[Договор].Сотрудник2
																	left join stack.[Сотрудники] as staff3 on staff3.ROW_ID = stack.[Договор].Сотрудник3
																	left join stack.[Сотрудники] as staff4 on staff4.ROW_ID = stack.[Договор].Сотрудник4
										   										   			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Folders():
	query_result = session_ul.execute(text(f"""--sql
														select  stack.[Договор].[Номер] as agreement, folders.[Примечание] as folder, folders.area
															from stack.[Договор]
															left join (select sp.row_id, sp.Папки, sp.Примечание, COALESCE (pp.[Примечание], sp.[Примечание]) as area
																			from stack.[Договор] sp
																			left join (select *
																							from stack.[Договор]
																							where [Папки] = 80540
																						) as pp on pp.row_id = sp.[Папки]
															where (sp.Папки_ADD=0 and sp.Заказчик>0) or sp.Папки=-10 ) as folders
															on folders.[row_id] = stack.[Договор].Иерархия2
															where len(stack.[Договор].[Номер])>=10
												;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_Organization_Type():
	query_result = session_ul.execute(text(f"""--sql
													select
															agr.[Номер] as agreement,
															case 	when orggr.[Отрасль] = 0 then 'ЮЛ'
																	when orggr.[Отрасль] = 0 then 'Физ.лицо'
										   							when orggr.[Отрасль] = 0 then 'ИП'
										   						else ''
										   					end as org_type_gr,
															case 	when orgpl.[Отрасль] = 0 then 'ЮЛ'
																	when orgpl.[Отрасль] = 0 then 'Физ.лицо'
										   							when orgpl.[Отрасль] = 0 then 'ИП'
										   						else ''
										   					end as org_type_pl
														from stack.[Договор] as agr
														inner join stack.[Организации] as orggr on agr.[Грузополучатель] = orggr.row_id
														inner join stack.[Организации] as orgpl on agr.[Плательщик] = orgpl.row_id
														order by agreement
										   ;""")).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Budget():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
															class01.Код as kod_budget,
															class01.Название as name_budget,
															class02.Название as name_budget_head
														from stack.[Договор] as agr
															left join stack.[Классификаторы] as class01 on class01.ROW_ID = agr.[Бюджет-Договоры]
															left join (select * from stack.[Классификаторы] where [Папки]=682) as class02 on class02.ROW_ID = class01.[Папки]
														where class02.Название is not null
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Vid():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
															class01.[Код] as vd_kod,
															class01.[Название] as vd_name
														from stack.[Договор] as agr
														left join stack.[Классификаторы] as class01 on class01.ROW_ID = agr.[СправочникВД-Договоры]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Otrasl():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
															class01.[Код] as ot_kod,
															class01.[Название] as ot_name,
															class01.МакетаКод10112 as ot_kod10112
														from stack.[Договор] as agr
														left join stack.[Классификаторы] as class01 on class01.ROW_ID = agr.[Отрасль-Договоры]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Category():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
															categories.[Код] as category_kod,
															categories.[Название] as category_name
														from stack.[Договор] as agr
														left join stack.[Категории договоров] as categories on categories.ROW_ID = agr.[Категория-Договоры]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Organization_Vid_gr():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
																	vid_org_gr =   CASE
																					when org.[Бюджет] = 1 then 'Бюджет'
																					when org.[Бюджет] = 2 then 'Малый бизнес'
																					when org.[Бюджет] = 3 then 'Средний бизнес'
																					when org.[Бюджет] = 4 then 'Крупный бизнес'
																					when org.[Бюджет] = 5 then 'Микропредприятия'
																					else ''
																				END
														from stack.[Договор] as agr
														left join stack.[Организации] as org on org.ROW_ID = agr.[Грузополучатель]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Organization_Vid_pl():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
																	vid_org_pl =   CASE
																					when org.[Бюджет] = 1 then 'Бюджет'
																					when org.[Бюджет] = 2 then 'Малый бизнес'
																					when org.[Бюджет] = 3 then 'Средний бизнес'
																					when org.[Бюджет] = 4 then 'Крупный бизнес'
																					when org.[Бюджет] = 5 then 'Микропредприятия'
																					else ''
																				END
														from stack.[Договор] as agr
														left join stack.[Организации] as org on org.ROW_ID = agr.[Плательщик]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)

def Get_Agreement_Organization_email():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
															orggr.email as email_gr,
															orgpl.email as email_pl
														from stack.[Договор] as agr
														left join stack.[Организации] as orggr on orggr.ROW_ID = agr.[Грузополучатель]
														left join stack.[Организации] as orgpl on orgpl.ROW_ID = agr.[Плательщик]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_LK():
	query_result = session_ul.execute(text(f"""--sql
														select
															agr.[Номер] as agreement,
															lk.lk
														from stack.[Договор] as agr
														left join ( select distinct left(agrin.[Номер],10) as nc,
																					'ЛК' as lk
																	   from stack.[Пароли привязка] pp, stack.[Договор] agrin
																	   where	   agrin.row_id = pp.[Привязка-Договор]
																			   and pp.[Состояние] > 0 ) as lk on lk.nc = agr.[Номер]
														order by agreement;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_Payments_Shedule():
	query_result = session_ul.execute(text(f"""--sql
														select 	agr.[Номер] as agreement,
																day1 		= (select top 1 [День платежа] from stack.[График оплаты договора] where [График-договор]=agr.row_id and [День платежа]=1 and (GETDATE() between [Месяц] and [МесяцПо])),
																procent1 	= (select top 1 [процентДоговорнойВеличины] from stack.[График оплаты договора] where [График-договор]=agr.row_id and [День платежа]=1 and (GETDATE() between [Месяц] and [МесяцПо])),
																day10 		= (select top 1 [День платежа] from stack.[График оплаты договора] where [График-договор]=agr.row_id and [День платежа]=10 and (GETDATE() between [Месяц] and [МесяцПо])),
																procent10 	= (select top 1 [процентДоговорнойВеличины] from stack.[График оплаты договора] where [График-договор]=agr.row_id and [День платежа]=10 and (GETDATE() between [Месяц] and [МесяцПо])),
																day25 		= (select top 1 [День платежа] from stack.[График оплаты договора] where [График-договор]=agr.row_id and [День платежа]=25 and (GETDATE() between [Месяц] and [МесяцПо])),
																procent25 	= (select top 1 [процентДоговорнойВеличины] from stack.[График оплаты договора] where [График-договор]=agr.row_id and [День платежа]=25 and (GETDATE() between [Месяц] and [МесяцПо]))
															from stack.[Договор] as agr
															order by agreement
															;
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Agreement_Reconcilation_Acts(parameters):
	query_result = session_ul.execute(text(f"""--sql
														SELECT	  left(agr.Номер,10)  as agreement,
																		STRING_AGG(left(vd.[Оригинальное имя],250), ', ') as documents
																FROM	stack.[Внешние документы] vd,
																		stack.Документ as doc
																left join stack.[Договор] agr on agr.ROW_ID = doc.[Документы-Договор]
																WHERE   doc.[Тип документа] = 105 and
																		year(doc.[РасчМесяц]) = {parameters['year']} and  month(doc.[РасчМесяц])= {parameters['month']} and
																		vd.[Документ-Файл] = doc.ROW_ID
																group by left(agr.Номер,10);
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)



def Get_Data_For_Report_Heads_and_Submissives(parameters):
	cdate = f"{parameters['year']}-{parameters['month']}-1"
	query_result = session_ul.execute(text(f"""--sql
											SELECT 	parts.agreement_number as [Гол.Договор],
													parts.Номер as [Гол.ТУ],
													parts.Примечание as [Гол.Название ТУ],
													parts.АдресЛС as [Гол.Адрес ТУ],
													head_consuming.kvt as [Гол.Потребление за],
													head_folders.folder as  [Гол.Район],
													head_folders.area as [Гол.Отделение],
													head_stuff.fio1 as [Гол.ФИО],
													--
													points.agreement_number as [Суб.Договор],
													points.Номер as [Суб.ТУ],
													points.Примечание as [Суб.Название ТУ],
													points.АдресЛС as [Суб.Адрес ТУ],
													sub_consuming.kvt as [Суб.Потребление за],
													sub_folders.folder as  [Суб.Район],
													sub_folders.area as [Суб.Отделение],
													sub_stuff.fio1 as [Суб.ФИО]
											FROM 	stack.[Связи лицевого] shema
											inner join (select 		stack.[Договор].Номер as agreement_number,
																	stack.[Организации].Название, stack.[Организации].ИНН, stack.[Организации].КПП, stack.[Организации].Адрес,
																	stack.[Лицевые счета].row_id, stack.[Лицевые счета].Номер, stack.[Лицевые счета].Примечание, stack.[Лицевые счета].АдресЛС
														from 	stack.[Лицевые договора], stack.[Договор], stack.[Лицевые счета], stack.[Организации]
														where 	stack.[Договор].ROW_ID  = stack.[Лицевые договора].Договор and
															stack.[Лицевые счета].row_id = stack.[Лицевые договора].Лицевой and
															stack.[Организации].ROW_ID = stack.[Договор].Плательщик and
															EOMONTH('{cdate}')  between stack.[Лицевые договора].ДатНач and stack.[Лицевые договора].ДатКнц) parts
															on shema.[Главный лицевой] = parts.row_id
											inner join (select 		stack.[Договор].Номер as agreement_number,
																	stack.[Организации].Название, stack.[Организации].ИНН, stack.[Организации].КПП, stack.[Организации].Адрес,
																	stack.[Лицевые счета].row_id, stack.[Лицевые счета].Номер, stack.[Лицевые счета].Примечание, stack.[Лицевые счета].АдресЛС
														from 	stack.[Лицевые договора], stack.[Договор], stack.[Лицевые счета], stack.[Организации]
														where 	stack.[Договор].ROW_ID  = stack.[Лицевые договора].Договор and
															stack.[Лицевые счета].row_id = stack.[Лицевые договора].Лицевой and
															stack.[Организации].ROW_ID = stack.[Договор].Плательщик and
															EOMONTH('{cdate}')  between stack.[Лицевые договора].ДатНач and stack.[Лицевые договора].ДатКнц) points
																on shema.[Подчиненный лицевой] = points.row_id
											left join (select 	stack.[Лицевые счета].[Номер] as num_point,
																		sum(kvt) as kvt,
																		sum([СуммабезНДС]) as money_without_nds,
																		sum([Сумма]) as money
																from  stack.[Лицевые счета]
																inner join (
																	select dr.[Лицевой], dr.[Кол_во], dr.[СуммабезНДС], dr.[Сумма], tu.Наименование, tu.Наименование  as usl_name,
																	kvt =  CASE
																		when tu.[Номер услуги] < 1999 then dr.[Кол_во]
																		else 0
																	END
																	from stack.[Детализация расчета] dr
																	left join stack.[Типы услуг] as  tu on tu.[Номер услуги]  = dr.[Номер услуги]
																	where  (dr.[месяц] BETWEEN convert(datetime,'{cdate}',21) and EOMONTH('{cdate}')) AND
																	(dr.[замесяц] BETWEEN convert(datetime,'{cdate}',21) and EOMONTH('{cdate}'))
																	) as usl
																on usl.[Лицевой] = stack.[Лицевые счета].ROW_ID
																GROUP BY stack.[Лицевые счета].[Номер]) as sub_consuming
																	on  sub_consuming.num_point = points.Номер
											left join (select 	stack.[Лицевые счета].[Номер] as num_point,
																		sum(kvt) as kvt,
																		sum([СуммабезНДС]) as money_without_nds,
																		sum([Сумма]) as money
																from  stack.[Лицевые счета]
																inner join (
																	select dr.[Лицевой], dr.[Кол_во], dr.[СуммабезНДС], dr.[Сумма], tu.Наименование, tu.Наименование  as usl_name,
																	kvt =  CASE
																		when tu.[Номер услуги] < 1999 then dr.[Кол_во]
																		else 0
																	END
																	from stack.[Детализация расчета] dr
																	left join stack.[Типы услуг] as  tu on tu.[Номер услуги]  = dr.[Номер услуги]
																	where  (dr.[месяц] BETWEEN convert(datetime,'{cdate}',21) and EOMONTH('{cdate}')) AND
																	(dr.[замесяц] BETWEEN convert(datetime,'{cdate}',21) and EOMONTH('{cdate}'))
																	) as usl
																on usl.[Лицевой] = stack.[Лицевые счета].ROW_ID
																GROUP BY stack.[Лицевые счета].[Номер]) as head_consuming
																	on  head_consuming.num_point = parts.Номер
											left join (		select  stack.[Договор].[Номер] as nc, folders.[Примечание] as folder, folders.area
														from stack.[Договор]
														left join (select sp.row_id, sp.Папки, sp.Примечание, COALESCE (pp.[Примечание], sp.[Примечание]) as area
																		from stack.[Договор] sp
																		left join (select *
																						from stack.[Договор]
																						where [Папки] = 80540
																					) as pp on pp.row_id = sp.[Папки]
														where (sp.Папки_ADD=0 and sp.Заказчик>0) or sp.Папки=-10 ) as folders
														on folders.[row_id] = stack.[Договор].Иерархия2
														where len(stack.[Договор].[Номер])>=10) as head_folders on head_folders.nc = parts.agreement_number
											left join (		select  stack.[Договор].[Номер] as nc, folders.[Примечание] as folder, folders.area
														from stack.[Договор]
														left join (select sp.row_id, sp.Папки, sp.Примечание, COALESCE (pp.[Примечание], sp.[Примечание]) as area
																		from stack.[Договор] sp
																		left join (select *
																						from stack.[Договор]
																						where [Папки] = 80540
																					) as pp on pp.row_id = sp.[Папки]
														where (sp.Папки_ADD=0 and sp.Заказчик>0) or sp.Папки=-10 ) as folders
														on folders.[row_id] = stack.[Договор].Иерархия2
														where len(stack.[Договор].[Номер])>=10) as sub_folders on sub_folders.nc = points.agreement_number
											left join (	select
																	left(stack.[Договор].Номер,10) as agreement,
																	staff1.ФИО as fio1,
																	staff2.ФИО as fio2,
																	staff3.ФИО as fio3,
																	staff4.ФИО as fio4
														from
																stack.[Договор]
														left join stack.[Сотрудники] as staff1 on staff1.ROW_ID = stack.[Договор].Сотрудник1
														left join stack.[Сотрудники] as staff2 on staff2.ROW_ID = stack.[Договор].Сотрудник2
														left join stack.[Сотрудники] as staff3 on staff3.ROW_ID = stack.[Договор].Сотрудник3
														left join stack.[Сотрудники] as staff4 on staff4.ROW_ID = stack.[Договор].Сотрудник4) as head_stuff on head_stuff.agreement = parts.agreement_number
											left join (	select
																	left(stack.[Договор].Номер,10) as agreement,
																	staff1.ФИО as fio1,
																	staff2.ФИО as fio2,
																	staff3.ФИО as fio3,
																	staff4.ФИО as fio4
														from
																stack.[Договор]
														left join stack.[Сотрудники] as staff1 on staff1.ROW_ID = stack.[Договор].Сотрудник1
														left join stack.[Сотрудники] as staff2 on staff2.ROW_ID = stack.[Договор].Сотрудник2
														left join stack.[Сотрудники] as staff3 on staff3.ROW_ID = stack.[Договор].Сотрудник3
														left join stack.[Сотрудники] as staff4 on staff4.ROW_ID = stack.[Договор].Сотрудник4) as sub_stuff on sub_stuff.agreement = points.agreement_number
											WHERE 	(EOMONTH('{cdate}') between shema.ДатНач and shema.ДатКнц)
															;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Organization_Data(row_id:int):
	query_result = session_ul.execute(text(f"""--sql
																	select
										   								org.[Название] as short_name,
										   								org.[Наименование] as name,
										   								org.[ИНН] as inn,
										   								org.[КПП] as kpp,
										   								org.[ОГРН] as ogrn,
																		case 	when org.[Отрасль] = 0 then 'ЮЛ'
																				when org.[Отрасль] = 1 then 'Физ.лицо'
																				when org.[Отрасль] = 2 then 'ИП'
																				else ''
																		end as org_type,
										   								org.[Отрасль] as org_type_id,
																		org_vid = 	CASE
																							when org.[Бюджет] = 1 then 'Бюджет'
																							when org.[Бюджет] = 2 then 'Малый бизнес'
																							when org.[Бюджет] = 3 then 'Средний бизнес'
																							when org.[Бюджет] = 4 then 'Крупный бизнес'
																							when org.[Бюджет] = 5 then 'Микропредприятия'
																							else ''
																						END,
										   								org.[ОКОНХ] as okonh,
										   								org.[ОКПО] as okpo,
										   								org.[ОКВЭД] as OKVED,
										   								org.[Бюджет] as org_vid_id,
										   								org.[Вариант НДС] as nds_type,
										   								org.[Категория] as debtor_category,
										   								org.[Примечание] as note,
										   								org.[Адрес] as address,
										   								org.[ФактАдрес] as fact_address,
										   								org.[Телефон] as phone,
										   								org.[Факс] as faks,
										   								org.[Режим работы] as regime,
										   								org.[email] as email,
										   								convert(date, org.[ДатаРегистрации], 1) as date_begin,
										   								convert(date, org.[ДатаЛиквидации], 1) as date_end,
										   								org.www as www,
										   								org.[ИдентификаторЭДО] as EDO
																	from stack.[Организации] as org
																	where org.row_id={row_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Get_Invoice_Data(document_id:int):
	# Документ.Лицо2  - грузополучатель
	# select *	from stack.[Документ]	where row_id in ( select [Папки] from stack.[Документ]	where row_id = 30631054 ); и тут Лицо2 - Грузоотпра
	query_result = session_ul.execute(text(f"""--sql
										   """)).fetchall()
	return get_queryresult_header_and_data(query_result)





def Update_Statistic_UL_DB(user_id):
	models.Add_Message_for_User(
									user_id	=	user_id,
									icon = 'service',
									link='',
									style='',
									text='Начато обновление статистики'
	)

	result = session_ul.execute(text(	"""--sql
											EXEC sp_updatestats
										;"""))
	session_ul.commit()

	models.Add_Message_for_User(
									user_id	=	user_id,
									icon = 'service',
									link='',
									style='',
									text='Статистика обновлена'
	)
	return result

def Join_Pairs(list_of_dictionaries:list, key,value:str):
	result = {}
	for element in list_of_dictionaries:
		result[element[key]] = element[value]
	return result


print("=============================")
# print(Agreement_Payments_Schedule(113442))
# prnt( Get_Data_For_Report_Heads_and_Submissives({'year':2024, 'month':2}) )
#print("=============================")
#prnt(Organization_Data(48178))
#h, v = Get_Agreement_Folders()
#print(Join_Pairs(v, 'agreement', 'folder'))
#print()
#print(Join_Pairs(v, 'agreement', 'area'))
#print("=============================")




