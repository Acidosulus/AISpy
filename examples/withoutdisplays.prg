&& процедура возвращающая список точек, рассчитывающихся по ПУ, но не имеющих показаний на последню дату месяца
&& как основа контроля не забыли ли рассчитать кого либо в месяце
Procedure ReportPointsWithoutDisplays
parameters pn_year, pn_month
local lc_year, lc_month, lc_day, cwa
cwa = select()
lc_year = stra(pn_year)
lc_month = stra(pn_month)
lc_day = stra(day(gld(pn_year, pn_month)))
text to lc_str noshow textmerge
----------------------------------------------------------------------------------------------------------------------------------------------------
DECLARE @dateendofmonth datetime = '<<lc_year>>-<<lc_month>>-<<lc_day>>'
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
	statuses.status,
    lastdisplays.*
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
  where lastdisplays.[Показание] is  null;
  ----------------------------------------------------------------------------------------------------------------------------------------------------
  endtext
  StrToFile(lc_str, gc_temp_path+'GetPointsWithoutDisplays.sql')
  MSexec(lc_str, 'cursor_GetPointsWithoutDisplays')
 

  Select_Agreements_Folders() 
  
		select cursor_GetPointsWithoutDisplays.*, Select_Agreements_Folders_parametes.* ;
			from cursor_GetPointsWithoutDisplays ;
			left join Select_Agreements_Folders_parametes on alltrim(Select_Agreements_Folders_parametes.nc) == alltrim(cursor_GetPointsWithoutDisplays.Номер_договора) ;
			into cursor result readwrite

		update result set ЗаводскойНомер = [']+alltrim(ЗаводскойНомер)

  	lo_excel = create_excel_report_simple(	'ТУ без показаний',;
											'ТУ без показаний на конец месяца '+get_month_name(pn_month)+[ ]+stra(pn_year)+[ г. // ]+dtoc(date())+'  '+time(),;
											'result',;
											'alltrim(Номер_договора), alltrim(название), alltrim(номер_ту), alltrim(Название_ТУ), alltrim(Тип_ПУ), alltrim(ЗаводскойНомер), alltrim(status), alltrim(folder), alltrim(area), alltrim(ФИО)',;
  											'№, Название договора, ТУ, ТУ, Тип ПУ, № ПУ,Состояние ПУ, Участок, Отделение, ФИО')
	Set_Columns_Width_In_excel_object(lo_excel, '10,12,12,30,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20')
	lo_excel.Rows("2:2").AutoFilter

	


  CloseAlias('cursor_GetPointsWithoutDisplays, cursor_GetPointsWithoutDisplays, result, Select_Agreements_Folders_parametes')
 	echo()
  select(cwa)

endproc
