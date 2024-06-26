import data_sourses
import os
import datetime
import decimal
import pandas
import json
from click import echo, style
import logging
from common import app
import models
logging.basicConfig(level=logging.INFO) 

print(f'designerUL imported to {__name__}')

from common import celery



def Append_Data(source:list, get_data_func, key,value,parameter_name:str,parameters={}):
	if len(parameters)>0:
		header, data = get_data_func(parameters)
	else:
		header, data = get_data_func()
	paired_data = data_sourses.Join_Pairs(data, key, value)
	for row in source:
		value = paired_data.get(row[key], '')
		row[parameter_name] = value
	return source



@celery.task(name='designerUL.Data_Construct')
def Data_Construct(current_user_id, csource:str, cparameters:str):
	# Создаем новый логгер для каждого пользователя
	logger = logging.getLogger(f'{current_user_id}')
	# Настраиваем файловый обработчик для логгера
	file_handler = logging.FileHandler(f"{current_user_id}_data.log")
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	# Логируем переданные параметры
	# logger.info(f"Source: {csource}")
	# logger.info(f"Parameters: {cparameters}")

	current_datetime = datetime.datetime.now()
	safe_part_of_filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
	file_name = os.path.join(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tmp'), f'report_id_{current_user_id}_{safe_part_of_filename}_designer_UL.xlsx')
	print(f'file_path: {file_name}')
	source = json.loads(csource)

	parameters = json.loads(cparameters)
	for parameter in parameters:
		
		if parameter['type']=='agreement_names':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Names, key='agreement', value='name', parameter_name=parameter['name'])

		if parameter['type']=='agreement_id':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Id, key='agreement', value='agreement_row_id', parameter_name=parameter['name'])

		if parameter['type']=='agreement_fsk':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_FSK, key='agreement', value='agreement_fsk', parameter_name=parameter['name'])

		if parameter['type']=='agreement_date_begin':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Date_Begin, key='agreement', value='date_begin', parameter_name=parameter['name'])

		if parameter['type']=='agreement_date_begin_sign':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Date_Begin_Sign, key='agreement', value='date_begin_sign', parameter_name=parameter['name'])

		if parameter['type']=='agreement_date_end':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Date_End, key='agreement', value='date_end', parameter_name=parameter['name'])

		if parameter['type']=='agreement_date_end_sign':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Date_End_Sign, key='agreement', value='date_end_sign', parameter_name=parameter['name'])

		if parameter['type']=='agreement_address_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Address_gr, key='agreement', value='address_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_address_fact_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Address_Fact_gr, key='agreement', value='address_fact_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_address_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Address_pl, key='agreement', value='address_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_phone_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Phone_gr, key='agreement', value='phone_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_phone_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Phone_pl, key='agreement', value='phone_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_inn_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_INN_pl, key='agreement', value='inn_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_kpp_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_KPP_pl, key='agreement', value='kpp_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_inn_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_INN_gr, key='agreement', value='inn_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_kpp_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_KPP_gr, key='agreement', value='kpp_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_orul':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_FIO, key='agreement', value='fio1', parameter_name=parameter['name'])

		if parameter['type']=='agreement_odrul':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_FIO, key='agreement', value='fio2', parameter_name=parameter['name'])

		if parameter['type']=='agreement_manager':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_FIO, key='agreement', value='fio3', parameter_name=parameter['name'])

		if parameter['type']=='agreement_ogrn_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_ORGN_pl, key='agreement', value='ogrn_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_ogrn_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_ORGN_gr, key='agreement', value='ogrn_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_folder':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Folders, key='agreement', value='folder', parameter_name=parameter['name'])

		if parameter['type']=='agreement_department':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Folders, key='agreement', value='area', parameter_name=parameter['name'])

		if parameter['type']=='agreement_organizaion_type_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Organization_Type, key='agreement', value='org_type_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_organizaion_type_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Organization_Type, key='agreement', value='org_type_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_budget':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Budget, key='agreement', value='kod_budget', parameter_name=parameter['name'] + ' - Код')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Budget, key='agreement', value='name_budget', parameter_name=parameter['name'] + ' - Название')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Budget, key='agreement', value='name_budget_head', parameter_name=parameter['name'] + ' - Название бюджета верхнего уровня')

		if parameter['type']=='agreement_vd':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Vid, key='agreement', value='vd_kod', parameter_name=parameter['name'] + ' - Код')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Vid, key='agreement', value='vd_name', parameter_name=parameter['name'] + ' - Название')

		if parameter['type']=='agreement_ot':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Otrasl, key='agreement', value='ot_kod', parameter_name=parameter['name'] + ' - Код')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Otrasl, key='agreement', value='ot_name', parameter_name=parameter['name'] + ' - Название')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Otrasl, key='agreement', value='ot_kod10112', parameter_name=parameter['name'] + ' - Код макета 10112')

		if parameter['type']=='agreement_category':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Category, key='agreement', value='category_kod', parameter_name=parameter['name'] + ' - Код')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Category, key='agreement', value='category_name', parameter_name=parameter['name'] + ' - Название')

		if parameter['type']=='agreement_organizaion_vid_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Organization_Vid_gr, key='agreement', value='vid_org_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_organizaion_vid_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Organization_Vid_pl, key='agreement', value='vid_org_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_organizaion_email_gr':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Organization_email, key='agreement', value='email_gr', parameter_name=parameter['name'])

		if parameter['type']=='agreement_organizaion_email_pl':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Organization_email, key='agreement', value='email_pl', parameter_name=parameter['name'])

		if parameter['type']=='agreement_lk':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_LK, key='agreement', value='lk', parameter_name=parameter['name'])

		if parameter['type']=='agreement_avans_schedule':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Payments_Shedule, value='day1', key='agreement', parameter_name=parameter['name'] + '1е число')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Payments_Shedule, value='procent1', key='agreement', parameter_name=parameter['name'] + '% 1е число')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Payments_Shedule, value='day10', key='agreement', parameter_name=parameter['name'] + '10е число')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Payments_Shedule, value='procent10', key='agreement', parameter_name=parameter['name'] + '% 10е число')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Payments_Shedule, value='day25', key='agreement', parameter_name=parameter['name'] + '25е число')
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Payments_Shedule, value='procent25', key='agreement', parameter_name=parameter['name'] + '% 25е число')

		if parameter['type']=='agreement_return_of_reconcilation_act':
			Append_Data(source=source, get_data_func=data_sourses.Get_Agreement_Reconcilation_Acts, value='documents', key='agreement', parameter_name=parameter['name'], parameters={'year':parameter['year'], 'month':parameter['month']})

	file_name =  download_excel(source, file_name)

	with app.app_context():
		models.Add_Message_for_User(	user_id=current_user_id,
							  			text='Конструктор отчетов',
										link=f'/download_report_from_file_store?file_name={file_name.replace("/","%2F")}',
										icon='excel',
										style='message_log_designer_ul_name'	)
	
	return file_name


def download_excel(source_data, file_name):
	report_humanread_name = 'Конструктор отчетов ЮЛ'

	df = pandas.DataFrame(source_data)

	writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
	
	df.to_excel(writer, index=False, float_format="%.2f", startrow=4, freeze_panes=(5,0), sheet_name='report')

	writer.sheets['report'].autofilter('A5:WW5')

	writer.sheets['report'].write(0,0,report_humanread_name)

	for column in df:
		writer.sheets['report'].set_column(
											df.columns.get_loc(column),
											df.columns.get_loc(column),
											max(df[column].astype(str).map(len).max(), len(column))
										)
	writer.close()
	return (file_name)

