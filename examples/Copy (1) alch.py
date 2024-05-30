from flask import Flask
from sqlalchemy import create_engine
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
import configparser
import pprint
import rich
from sqlalchemy.engine import URL

printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint

# import logging

config = configparser.ConfigParser()
config.read("settings.ini", encoding='UTF-8')



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


print(connection_url_ul)


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


engine_ul = create_engine(connection_url_ul, echo=False)
from sqlalchemy.orm import Session
session_ul = Session(engine_ul)
connection_ul = engine_ul.connect()


from sqlalchemy import create_engine, MetaData, Table, select, case, func
from sqlalchemy.sql import and_, or_


metadata = MetaData()
metadata.reflect(bind=engine_ul)

Договор = Table('Договор', metadata, schema='stack', autoload_with=engine_ul)

# rich.print([i for i in Договор.c])

# rich.print(
#     	select(Договор.columns['Номер']).
#         	where(Договор.columns['Номер'].like('%1300'))
#         )

# Отражение таблиц
договор = Table('Договор', metadata, schema='stack', autoload_with=engine_ul)
организации = Table('Организации', metadata, schema='stack', autoload_with=engine_ul)
классификаторы = Table('Классификаторы', metadata, schema='stack', autoload_with=engine_ul)
категории_договоров = Table('Категории договоров', metadata, schema='stack', autoload_with=engine_ul)

# Подзапросы
AgrTypes = select(
	классификаторы.c.ROW_ID,
	классификаторы.columns['Название']
).where(
	классификаторы.columns['Тип'] == 129
).alias('AgrTypes')

AgrOKVED = select(
	классификаторы.c.ROW_ID,
	классификаторы.columns['Название']
).alias('AgrOKVED')

budgets = select(
    классификаторы.c.ROW_ID,
	классификаторы.columns['Название'].label('name')
).where(
    or_(
        классификаторы.columns['Папки'] == 682,
        классификаторы.columns['Папки'].in_(
            select(
                классификаторы.c.ROW_ID
            ).where(
                классификаторы.columns['Папки'] == 682
            )
        )
    )
).subquery()

municipalformation = select(
	классификаторы.c.ROW_ID,
	классификаторы.c.Название.label('name')
).where(
	классификаторы.c.Папки == (
		select(классификаторы.c.ROW_ID).where(
			классификаторы.c.Тип == 128
		).order_by(классификаторы.c.ROW_ID).limit(1).scalar_subquery()
	)
).subquery()



query = select(
	договор.c.ROW_ID.label('agreement_id'),
	договор.c.Номер.label('number'),
	договор.c.Грузополучатель.label('gr_ROW_ID'),
	организации.c.Наименование.label('gr_name'),
	организации.c.Телефон.label('phone'),
	организации.c.Адрес.label('address'),
	договор.columns['Адрес доставки'].label('address_delivery'),
	договор.c.Плательщик.label('pl_ROW_ID'),
	организации.c.Наименование.label('pl_name'),
	договор.c.Примечание.label('note'),
	договор.columns['Тип договора'].label('agr_type'),
	case(
		(договор.columns['Тип договора'] == 1, 'договор энергоснабжения'),
		(договор.columns['Тип договора'] == 2, 'договор купли-продажи'),
		(договор.columns['Тип договора'] == 3, 'договор население (квитанции)'),
		(договор.columns['Тип договора'] == 4, 'договор хозяйственные нужды'),
		(договор.columns['Тип договора'] == 5, 'компенсация потерь сетевых компания'),
		(договор.columns['Тип договора'] == 6, 'договор оказания услуг по передаче электрической энергии'),
		(договор.columns['Тип договора'] == 7, 'договор купли-продажи в целях компенсации фактических потерь, возникающих в электрических сетях'),
		(договор.columns['Тип договора'] == 8, 'договор купли-продажи электричкой энергии в целях компенсации потерь электрической энергии в электрических сетях')
	, else_='').label('agr_type_name'),
	договор.columns['Начало договора'].label('agr_begin'),
	договор.c.Окончание.label('agr_end'),
	договор.columns['Дата подписания'].label('agr_sign_begin'),
	договор.columns['Дата расторжения'].label('agr_sign_end'),
	AgrTypes.c.Название.label('agr_VD_name'),
	договор.columns['СправочникВД-Договоры'].label('agr_VD_id'),
	категории_договоров.c.Название.label('agr_category_name'),
	договор.columns['Категория-Договоры'].label('agr_category_ROW_ID'),
	AgrOKVED.c.Название.label('agr_OKVED_name'),
	договор.columns['Бюджет-Договоры'].label('agr_budget_ROW_ID'),
	budgets.c.name.label('agr_budget_name'),
	municipalformation.c.name.label('municipalformation_name'),
	municipalformation.c.ROW_ID.label('municipalformation_ROW_ID')
).select_from(
	договор
	.join(организации, организации.c.ROW_ID == договор.c.Грузополучатель)
	.join(организации.alias('pl'), организации.c.ROW_ID == договор.c.Плательщик)
	.join(AgrTypes, AgrTypes.c.ROW_ID == договор.columns['СправочникВД-Договоры'])
	.join(категории_договоров, категории_договоров.c.ROW_ID == договор.columns['Категория-Договоры'])
	.join(AgrOKVED, AgrOKVED.c.ROW_ID == договор.columns['Отрасль-Договоры'])
	.join(budgets, budgets.c.ROW_ID == договор.columns['Бюджет-Договоры'])
	.join(municipalformation, municipalformation.c.ROW_ID == договор.columns['СправочникМО-Договоры'])
).where(
	договор.c.ROW_ID == 111495
)

print()
# rich.print(dir(query))
print()

with engine_ul.connect() as connection:
	result = connection.execute(query)
	for row in result:
		print(row)