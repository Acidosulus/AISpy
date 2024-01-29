from click import echo, style
import uuid
import datetime
import ujson

import pprint
printer = pprint.PrettyPrinter(indent=12, width=180)
prnt = printer.pprint


class DialogParameters():
	title = ''
	parameters = []
	backlink = ''
	def __init__(self, title, backlink):
		self.title = title
		self.parameters = []
		self.backlink = backlink

	def append(self, section):
		self.parameters.append(section)

	def get_answers(self, form_elements):
		result_dict = {}
		for element in  form_elements:
			result_dict[element[0]] = element[1]
		echo(style(text='get_answer:', fg='yellow')+' '+style(text=result_dict, fg='green'))
		print(str(self).replace("""`""",'"'))
		prnt(ujson.loads(str(self)))
		return result_dict

	def __str__(self) -> str:
		print(self.parameters)
		foo = ujson.dumps(dict(title=self.title, backlink=self.backlink, parameters= self.parameters), sort_keys=False, ensure_ascii=False)
		return foo

	def add_months(self, lable='Месяц', name=''):
		self.append(  
					dict(	lable	= 	lable,
		  					name	= 	(name if len(name)>0 else str(uuid.uuid4())),
							type	= 	'listbox',
							size	= 	12,
							data	= 	[dict(id=1,	value='Январь'),
				   						dict(id=2,	value='Февраль'),
										dict(id=3,	value='Март'),
										dict(id=4,	value='Апрель'),
										dict(id=5,	value='Май'),
										dict(id=6,	value='Июнь'),
										dict(id=7,	value='Июль'),
										dict(id=8,	value='Август'),
										dict(id=9,	value='Сентябрь'),
										dict(id=10,	value='Октябрь'),
										dict(id=11,	value='Ноябрь'),
										dict(id=12,	value='Декабрь')])
					)


	def add_years(self, lable='Год', name=''):
		years_list = []
		for year in range(datetime.date.today().year-6,datetime.date.today().year+3):
			years_list.append( dict(id= year, value=year) )
		self.append( dict(	lable	=	lable,
								name	=	(name if len(name)>0 else str(uuid.uuid4())),
								type	=	'listbox',
								default	=	datetime.date.today().year,
								size	=	6+3,
								data	=	years_list))
	

	def add_checkbox(self, lable='Флажок', name='', default=0):
			self.append( dict(lable	=	lable, 
						name	=	(name if len(name)>0 else str(uuid.uuid4())),
						type	=	'checkbox',
						default	=	default,
						size	=	0,
						data	=	[]))

	def add_date(self, lable = 'Дата', name = '', default=datetime.date.today().isoformat()):
			self.append( dict(lable	=	lable, 
						name	=	(name if len(name)>0 else str(uuid.uuid4())),
						type	=	'date',
						default	=	default, # .strftime('%Y-%m-%d'),
						size	=	0,
						data	=	[]))

"""
testdialog = DialogParameters(title='Заголовок тестового диалога', backlink='/RunReport/Points_WithOut_Displays')
testdialog.add_months('Месяц', 'Month')
testdialog.add_years('Год', 'Year')

print(testdialog)

"""
dialogtest = DialogParameters(title='Заголовок диалога с параметрами', backlink='/RunReport/TestDialog')

dialogtest.append( dict(name = 'Первый параметр ввода строки из диалога',
								lable = 'Первый параметр ввода строки из диалога',
								type='edit',
								default='строка по умолчанию',
								data=[],
								size=0) )


dialogtest.append( dict(name = 'Второй параметр ввода текста из диалога',
								lable = 'Второй параметр ввода текста из диалога',
								type='text',
								default='многострочный\nтекст\nпо\nумолчанию',
								data=[],
								size=0) )

dialogtest.append( dict(name = 'Третий параметр - флажок',
								lable = 'Третий параметр - флажок',
								type='checkbox',
								default='1',
								data=[],
								size=0) )
dialogtest.append( dict(name = 'Список значeний',
								lable = 'Список значeний',
								type='listbox',
								default='1',
								data=[dict(id=1, value='Первое значение'), dict(id=2,value='Второе значение')],
								size=0) )

dialogtest.append( dict(name = 'Список значeний 1',
								lable = 'Список значeний 1',
								type='listbox',
								default='1',
								data=[dict(id=1, value='Первое значение'), dict(id=2,value='Второе значение')],
								size=2) )


print(str(dialogtest))