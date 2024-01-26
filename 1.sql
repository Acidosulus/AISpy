--sql
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
;