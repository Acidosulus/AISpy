from click import echo, style
import sqlalchemy as sa
import datetime
from sqlalchemy import text
import datetime
import decimal
import json
import pandas
import os


#from celery import Celery
import time
import asyncio

import logging
logging.basicConfig(level=logging.INFO) 

celery_tasks = {}


import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint



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

#@celery.task
def Data_Construct(current_user_id, csource:str, cparameters:str):
	# Создаем новый логгер для каждого пользователя
	logger = logging.getLogger(f'{current_user_id}')
	# Настраиваем файловый обработчик для логгера
	file_handler = logging.FileHandler(f"{current_user_id}_data.log")
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	# Логируем переданные параметры
	logger.info(f"Source: {csource}")
	logger.info(f"Parameters: {cparameters}")

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


	print(source)
	return download_excel(source, file_name)


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








if __name__ == '__main__':
	import data_sourses
	data_sourses.init()
	result = Data_Construct(current_user_id= 2,
					csource="""[{"agreement": "1910210030", "point": "2003701002"}, {"agreement": "1910210030", "point": "2003701009"}, {"agreement": "1910210030", "point": "3756001001"}, {"agreement": "1910210030", "point": "6093001001"}, {"agreement": "1910210033", "point": "1003301002"}, {"agreement": "1910210033", "point": "1003301001"}, {"agreement": "1910210097", "point": "1009701001"}, {"agreement": "1910210127", "point": "1012701001"}, {"agreement": "1910210145", "point": "1014501003"}, {"agreement": "1910210145", "point": "1014501004"}, {"agreement": "1910210145", "point": "1014501001"}, {"agreement": "1910210145", "point": "1014501002"}, {"agreement": "1910210237", "point": "1023701001"}, {"agreement": "1910210257", "point": "1025701001"}, {"agreement": "1910210257", "point": "1025701002"}, {"agreement": "1910210280", "point": "1028001001"}, {"agreement": "1910210300", "point": "1030001001"}, {"agreement": "1910210317", "point": "1031701001"}, {"agreement": "1910210317", "point": "1031701002"}, {"agreement": "1910210330", "point": "1033001001"}, {"agreement": "1910210410", "point": "9999501065"}, {"agreement": "1910210417", "point": "1041701001"}, {"agreement": "1910210557", "point": "1055701001"}, {"agreement": "1910210557", "point": "1055701002"}, {"agreement": "1910210790", "point": "1079001001"}, {"agreement": "1910210790", "point": "1079001003"}, {"agreement": "1910210820", "point": "1082001001"}, {"agreement": "1910210857", "point": "1085701001"}, {"agreement": "1910210860", "point": "1086001001"}, {"agreement": "1910210890", "point": "1089001003"}, {"agreement": "1910210890", "point": "1089001001"}, {"agreement": "1910210905", "point": "9999501260"}, {"agreement": "1910210910", "point": "1091001005"}, {"agreement": "1910210910", "point": "1091001001"}, {"agreement": "1910210910", "point": "1091001003"}, {"agreement": "1910211027", "point": "1102701001"}, {"agreement": "1910211027", "point": "1102701002"}, {"agreement": "1910211040", "point": "1104001001"}, {"agreement": "1910211047", "point": "1104701001"}, {"agreement": "1910211067", "point": "1106701001"}, {"agreement": "1910211087", "point": "9563001001"}, {"agreement": "1910211087", "point": "1108701002"}, {"agreement": "1910211087", "point": "1108701001"}, {"agreement": "1910211147", "point": "1114701001"}, {"agreement": "1910211160", "point": "1116001002"}, {"agreement": "1910211200", "point": "1120701001"}, {"agreement": "1910211200", "point": "1120701002"}, {"agreement": "1910211200", "point": "1120701004"}, {"agreement": "1910211217", "point": "1121701001"}, {"agreement": "1910211227", "point": "1122701001"}, {"agreement": "1910211320", "point": "1132001003"}, {"agreement": "1910211370", "point": "1137001001"}, {"agreement": "1910211410", "point": "1141001001"}, {"agreement": "1910211470", "point": "1147001001"}, {"agreement": "1910211470", "point": "1147001003"}, {"agreement": "1910211480", "point": "1148001001"}, {"agreement": "1910211520", "point": "1152001002"}, {"agreement": "1910211520", "point": "1152001001"}, {"agreement": "1910211527", "point": "1152701001"}, {"agreement": "1910211540", "point": "1153701001"}, {"agreement": "1910211557", "point": "1155701001"}, {"agreement": "1910211557", "point": "1155701002"}, {"agreement": "1910211560", "point": "1156001001"}, {"agreement": "1910211620", "point": "1162001001"}, {"agreement": "1910211660", "point": "1166001003"}, {"agreement": "1910211660", "point": "1166001004"}, {"agreement": "1910211660", "point": "1166001001"}, {"agreement": "1910211660", "point": "1166001002"}, {"agreement": "1910211667", "point": "1166701001"}, {"agreement": "1910211690", "point": "1169001007"}, {"agreement": "1910211690", "point": "1169001001"}, {"agreement": "1910211690", "point": "1169001003"}, {"agreement": "1910211800", "point": "1180001001"}, {"agreement": "1910211807", "point": "1180701010"}, {"agreement": "1910211807", "point": "1180701004"}, {"agreement": "1910211807", "point": "1180701007"}, {"agreement": "1910211807", "point": "1180701009"}, {"agreement": "1910211807", "point": "1180701008"}, {"agreement": "1910211807", "point": "6054001003"}, {"agreement": "1910211807", "point": "6054001005"}, {"agreement": "1910211807", "point": "6054001006"}, {"agreement": "1910211807", "point": "6054001007"}, {"agreement": "1910211807", "point": "6054001008"}, {"agreement": "1910211807", "point": "9164001001"}, {"agreement": "1910211807", "point": "6054001009"}, {"agreement": "1910211807", "point": "6054001001"}, {"agreement": "1910211807", "point": "6054001002"}, {"agreement": "1910211855", "point": "1185501004"}, {"agreement": "1910211855", "point": "1185501006"}, {"agreement": "1910211937", "point": "1193701001"}, {"agreement": "1910212030", "point": "1203001001"}, {"agreement": "1910212107", "point": "1210701003"}, {"agreement": "1910212107", "point": "1210701001"}, {"agreement": "1910212107", "point": "1210701002"}, {"agreement": "1910212337", "point": "1233701001"}, {"agreement": "1910212367", "point": "1236701001"}, {"agreement": "1910212377", "point": "1237701001"}, {"agreement": "1910212430", "point": "1243001001"}, {"agreement": "1910212640", "point": "1264001001"}, {"agreement": "1910212690", "point": "1269001001"}, {"agreement": "1910212700", "point": "6630001001"}, {"agreement": "1910212700", "point": "1270001005"}, {"agreement": "1910212700", "point": "1270001001"}, {"agreement": "1910212700", "point": "1270001003"}, {"agreement": "1910212700", "point": "1270001006"}, {"agreement": "1910212700", "point": "9999501099"}, {"agreement": "1910212727", "point": "4974001002"}, {"agreement": "1910212727", "point": "1272001001"}, {"agreement": "1910212727", "point": "1272001002"}, {"agreement": "1910212860", "point": "1286001001"}, {"agreement": "1910225060", "point": "1295001001"}, {"agreement": "1910212967", "point": "1296001001"}, {"agreement": "1910212990", "point": "1299001001"}, {"agreement": "1910213190", "point": "1316001001"}, {"agreement": "1910213720", "point": "1372001001"}, {"agreement": "1910214380", "point": "9999501158"}, {"agreement": "1910214380", "point": "9999501156"}, {"agreement": "1910214380", "point": "9999501159"}, {"agreement": "1910214380", "point": "9999501157"}, {"agreement": "1910214380", "point": "9999501162"}, {"agreement": "1910214380", "point": "9999501160"}, {"agreement": "1910214380", "point": "9999501163"}, {"agreement": "1910214380", "point": "9999501161"}, {"agreement": "1910214380", "point": "9999501201"}, {"agreement": "1910214380", "point": "9999501331"}, {"agreement": "          ", "point": "1531001126"}, {"agreement": "1910214430", "point": "1443001001"}, {"agreement": "1910214777", "point": "1447001001"}, {"agreement": "1910214777", "point": "4210001002"}, {"agreement": "1910214980", "point": "1498001001"}, {"agreement": "1910214980", "point": "1498001002"}, {"agreement": "1910214980", "point": "1498001003"}, {"agreement": "1910215085", "point": "1508501029"}, {"agreement": "1910215085", "point": "1508501001"}, {"agreement": "1910215085", "point": "1508501002"}, {"agreement": "1910215085", "point": "1508501025"}, {"agreement": "1910215085", "point": "9999501055"}, {"agreement": "1910215085", "point": "9999501056"}, {"agreement": "1910215085", "point": "9999501054"}, {"agreement": "1910215085", "point": "1508501019"}, {"agreement": "1910215085", "point": "1508501033"}, {"agreement": "1910215085", "point": "1508501023"}, {"agreement": "1910215085", "point": "1508501024"}, {"agreement": "1910215085", "point": "1508501031"}, {"agreement": "1910215247", "point": "1524701004"}, {"agreement": "1910215247", "point": "1524701001"}, {"agreement": "1910215247", "point": "1524701002"}, {"agreement": "1910215247", "point": "1524701003"}, {"agreement": "1910215250", "point": "1525001020"}, {"agreement": "1910215250", "point": "1525001021"}, {"agreement": "1910215250", "point": "1525001023"}, {"agreement": "1910215250", "point": "1525001024"}, {"agreement": "1910215270", "point": "1527001002"}, {"agreement": "1910215270", "point": "1527001001"}, {"agreement": "1910215270", "point": "1527001022"}, {"agreement": "1910215270", "point": "1527001023"}, {"agreement": "1910215270", "point": "1527001024"}, {"agreement": "1910215290", "point": "4249001001"}, {"agreement": "1910215290", "point": "1529001001"}, {"agreement": "1910215420", "point": "1542001008"}, {"agreement": "1910215420", "point": "1542001009"}, {"agreement": "1910215420", "point": "1542001007"}, {"agreement": "1910215420", "point": "1542001006"}, {"agreement": "1910215570", "point": "1557001019"}, {"agreement": "1910215570", "point": "1557001022"}, {"agreement": "1910215570", "point": "1557001017"}, {"agreement": "1910215570", "point": "1557001018"}, {"agreement": "1910215570", "point": "1557001023"}, {"agreement": "1910215610", "point": "1561001001"}, {"agreement": "1910215700", "point": "1570001001"}]""",
					cparameters="""[{"type": "agreement_names", "name": "Название договора"}, {"type": "agreement_folder", "name": "Отделение договора"}, {"type": "agreement_date_begin", "name": "Дата начала договора"}, {"type": "agreement_department", "name": "Участок договора"}, {"type": "agreement_organizaion_type_gr", "name": "Тип Организации Грузополучателя"}, {"type": "agreement_organizaion_type_pl", "name": "Тип Организации Плательщика"}, {"type": "agreement_budget", "name": "Бюджет договора"}, {"type": "agreement_vd", "name": "Вид договора"}, {"type": "agreement_ot", "name": "Отрасль договора"}, {"type": "agreement_category", "name": "Категория договора"}, {"type": "agreement_organizaion_vid_gr", "name": "Вид Организации Грузополучателя"}, {"type": "agreement_organizaion_vid_pl", "name": "Вид Организации Плательщика"}, {"type": "agreement_organizaion_email_gr", "name": "E-mail Грузополучателя"}, {"type": "agreement_organizaion_email_pl", "name": "E-mail Плательщика"}, {"type": "agreement_lk", "name": "Наличие у договора ЛК"}, {"type": "agreement_avans_schedule", "name": "График авансовых платежей"}, {"type": "agreement_id", "name": "Идентификатор договора"}, {"type": "agreement_fsk", "name": "Наличие точек с тарифами ФСК"}, {"type": "agreement_return_of_reconcilation_act", "name": "Возврат акт сверки за Март 2024 г.", "year": "2024", "month": "3"}, {"type": "agreement_return_of_reconcilation_act", "name": "Возврат акта сверки за Декабрь 2023 г.", "year": "2023", "month": "12"}]"""
				 )
	print(result)


#	celery = Celery('tasks',
#				broker='amqp://guest:guest@localhost',
#				task_always_eager=True)
else:

	

	from app import common, connection_ul, connection_fl, connection,data_sourses #,celery
	from app import app