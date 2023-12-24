Procedure Select_Agreements_Folders
	local lc_str
	TEXT TO lc_str NOSHOW TEXTMERGE
		select  stack.[Договор].[Номер] as nc, folders.[Примечание] as folder, folders.area
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
	ENDTEXT
	MSexec(lc_str, 'Select_Agreements_Folders_temp')
	select left(nc,250) as nc, left(folder,250) as folder, left(area,250) as area from Select_Agreements_Folders_temp into cursor Select_Agreements_Folders_parametes readwrite
	update Select_Agreements_Folders_parametes where isnull(folder) set folder = ''
	update Select_Agreements_Folders_parametes where isnull(area) set area = ''
	Close_Alias('Select_Agreements_Folders_temp')
endproc       