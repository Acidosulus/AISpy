from click import echo, style
import sqlalchemy as sa
from app import common, connection_ul, connection_fl, connection
from sqlalchemy import text
import datetime
import decimal

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint



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
		query_result = connection_ul.execute(text(f"""--sql
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
	query_result = connection_ul.execute(text(f"""--sql
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
	query_result = connection_ul.execute(text(f"""--sql
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
	query_result = connection_ul.execute(text(f"""--sql
	declare 	@datn date = '{year}-{month}-01' ,	@datk date = EOMONTH('{year}-{month}-01')
                     Select distinct * from (
                                       select 	left(dog.Номер,10) as [Номер договора],
									   			left(org.Название,250) as [Название договора],
                                              	ls.Номер as [ТУ], 
												left(ls.[Примечание],250) as [Название ТУ],
												"'"+left(nom.Наименование,250) as [ПУ],
											  	left(so.ЗаводскойНомер,50) as [Заводской номер],
											  	ps.Показание as [Показание],
                                              	--ld.Лицевой,
												left(d.Отделение,50) as [Отделение],
												left(d.Участок,50) as [Участок],
												--so.row_id,
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
	query_result = connection_ul.execute(text(f"""--sql
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
					(doc.Дата between convert(datetime,'{parameters["from"]}',21) and convert(datetime,'{parameters["to"]}',21)) and 
					(agr.Номер is not null)
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Agreement_Data(row_id:int):
	query_result = connection_ul.execute(text(f"""--sql
																	select
																			agr.[Номер] as number,
																			agr.[Грузополучатель] as gr_row_id,
																			gr.[Название] as gr_name,
																			agr.[Плательщик] as pl_row_id,
																			pl.[Название] as pl_name,
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
										   									AgrOKVED.[Название] as agr_OKVED_name
																	from stack.[Договор] as agr
																		left join stack.[Организации] as gr on gr.row_id = agr.[Грузополучатель]
																		left join stack.[Организации] as pl on pl.row_id = agr.[Плательщик]
										   								left join (select row_id, [Название] from stack.[Классификаторы] where [Тип]=129) as AgrTypes on AgrTypes.row_id = agr.[СправочникВД-Договоры]
										   								left join stack.[Категории договоров] as category on category.row_id = agr.[Категория-Договоры]
										   								left join (select row_id, [Название] from stack.[Классификаторы]) as AgrOKVED on AgrOKVED.row_id = agr.[Отрасль-Договоры]
																	where agr.row_id={row_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Agreement_Types_Data():
	query_result = connection_ul.execute(text(f"""--sql
																	select 	row_id,
										   									[Название] as name
										   								from stack.[Классификаторы]
										   								where [Тип]=129 and [Код]>0;
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


def Agreement_Parameters_Data(agreement_id:int):
	query_result = connection_ul.execute(text(f"""--sql
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
	query_result = connection_ul.execute(text(f"""--sql
													select  convert(date, [Месяц], 1 ) as date_begin,
															convert(date, [МесяцПо],1) as date_end,
															[День платежа] as day ,
															[процентДоговорнойВеличины] as procent,
															(case when GETDATE() between [Месяц] and [МесяцПо] then 1 else 0 end) as active
														from stack.[График оплаты договора] as gr 
														where [График-Договор]={agreement_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)




def Organization_Data(row_id:int):
	query_result = connection_ul.execute(text(f"""--sql
																	select
										   								org.[Название] as org_short_name,
										   								org.[Наименование] as org_name
																	from stack.[Организации] as org
																	where org.row_id={row_id};
			;""")).fetchall()
	return get_queryresult_header_and_data(query_result)


#print("=============================")
#print(Agreement_Payments_Schedule(113442))
#prnt(Agreement_Data(113442))
#print("=============================")
#prnt(Organization_Data(48178))
#print("=============================")