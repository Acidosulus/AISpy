from click import echo, style
import sqlalchemy as sa
from app import common, connection_ul, connection_fl
from sqlalchemy import text

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


def get_queryresult_header_and_data(query_result):
	result = []
	for v in query_result:
		drow = {}
		for count, value in enumerate(v._fields):
			drow[value] = (v[count] if v[count]!=None else '')
		result.append(drow)
	headers = []
	if len(result)>0:
		headers = list(result[0].keys())
	return headers, result	


def Points_WithOut_Displays(year, month:int):
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


def Calc_Status_MKJD_Points(year, month:int):
	fl_points = connection_ul.execute(text(f"""--sql
			select Потомок as row_id, 
			   [0] as Район,[1] as Участок,[12] as НП,[2] as Улица,[3] as Дом,[4] as Квартира
			   from (
		select Потомок, (case ls.Тип when 0  then Фамилия 
										when 1  then org.Название
										when 2   then ( stack.atoa( city.Название ) )
	
										when 12   then (  stack.atoa( city.Название ) )
										when 3  then ( isnull(space( 5 - len(Номер) ),'') + CONVERT( VARCHAR(10), Номер) + stack.atoa( Фамилия ) )
										when 4  then ( isnull(space( 5 - len(Номер) ),'') + CONVERT( VARCHAR(10), Номер) + stack.atoa( Фамилия ) ) end ) as Адрес,
						ls.Тип
			from atom_khk_fl.stack.[Лицевые иерархия] lh
			join atom_khk_fl.stack.[Лицевые счета] ls on ls.row_id=lh.Родитель
			left join atom_khk_fl.stack.[Организации] org on org.row_id = [Счет-Линейный участок]
			left join atom_khk_fl.stack.Города city on city.row_id = [Улица-Лицевой счет]
			where Потомок in (select row_id from stack.[Лицевые счета] where Тип=5)
			) as Addr
			pivot (Max(Адрес) for Тип in ([0],[1],[2],[3],[4],[12])) as addrls)
	select v.Номер, s1.Сторонний ТУ_Схема2, s2.Сторонний ТУ_Схема3, 
		  stack.AddrLs(v.ROW_ID ,2)Адрес, adr.Район,	adr.Участок Участок2,	adr.НП, adr.Улица,	adr.Дом, adr.Квартира
	from atom_khk_fl.stack.[Лицевые счета]  v 
	inner join atom_khk_fl.stack.Свойства det4 on det4.[Счет-Параметры]=v.row_id and det4.[Виды-Параметры] =261 and sysdatetime() between det4.ДатНач and isnull(det4.ДатКнц,'20450509')
	left join atom_khk_fl.stack.[Соответствие лицевых] s1 on s1.Номер =v.Номер and s1.Тип =1002 
	left join atom_khk_fl.stack.[Соответствие лицевых] s2 on s2.Номер =v.Номер and s2.Тип =1003
	 left join cur_adres adr on adr.row_id=v.row_id
	;
		""")).fetchall()
	pass