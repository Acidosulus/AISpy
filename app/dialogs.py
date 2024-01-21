from click import echo, style
import uuid
from datetime import datetime
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
		foo = ujson.dumps(dict(title=self.title, backlink=self.backlink, parameters= self.parameters), sort_keys=False, ensure_ascii=False)
		#print(foo)
		return foo
		cdata = ''
		for parameter in self.parameters:
			cdata += (', 'if len(cdata)>0 else '') + str(parameter) 
		return '{'+f"title:`{self.title}`, backlink:`{self.backlink}`, "+'parameters:[' + cdata + ']'+'};'

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
		for year in range(datetime.now().year-6,datetime.now().year+3):
			years_list.append( dict(id= year, value=year) )
		self.append( dict(	lable	=	lable,
								name	=	(name if len(name)>0 else str(uuid.uuid4())),
								type	=	'listbox',
								default	=	datetime.now().year,
								size	=	6+3,
								data	=	years_list))
	

	def add_checkbox(self, lable='Флажок', name='', default=0):
			self.append( dict(lable	=	lable, 
						name	=	(name if len(name)>0 else str(uuid.uuid4())),
						type	=	'checkbox',
						default	=	default,
						size	=	0,
						data	=	[]))

class DialogSection():
	lable = ''
	type = ''
	default =''
	name = str(uuid.uuid4())
	data = []
	size = '0'
	def __init__(self, lable, type, default, name, data, size,):
		self.lable = lable
		self.name = name
		self.type = type
		self. size = size
		self.default = default
		self.data = data

	def __str__(self) -> str:
		return ujson.dumps(self.data)
		cdata=''
		for element in self.data:
			cdata = cdata + '		'+'{'+f"""id:`{element['id']}`, value:`{element['value']}`"""+'}' #', ' if len(cdata)>0 else ''+
		cdata ='[' + cdata + ']'
		cdata = cdata.replace('}		{','},		{')
		return '{'+f"""lable:`{self.lable}`, name:`{self.name}`, type:`{self.type}`, default:`{self.default}`, size:`{self.size}`, data:{cdata}"""+'}'


"""
testdialog = DialogParameters(title='Заголовок тестового диалога', backlink='/RunReport/Points_WithOut_Displays')
testdialog.add_months('Месяц', 'Month')
testdialog.add_years('Год', 'Year')

print(testdialog)


dialog = DialogParameters(title='Заголовок диалога с параметрами', backlink='/RunReport/Points_WithOut_Displays')
dialog.append( DialogSection(name = 'Первый параметр ввода строки из диалога',
								lable = 'Первый параметр ввода строки из диалога',
								type='edit',
								default='строка по умолчанию',
								data=[],
								size=0) )

dialog.append( DialogSection(name = 'Второй параметр ввода текста из диалога',
								lable = 'Второй параметр ввода текста из диалога',
								type='text',
								default='многострочный\nтекст\nпо\nумолчанию',
								data=[],
								size=0) )

dialog.append( DialogSection(name = 'Третий параметр - флажок',
								lable = 'Третий параметр - флажок',
								type='checkbox',
								default='1',
								data=[],
								size=0) )
dialog.append( DialogSection(name = 'Список значний',
								lable = 'Список значний',
								type='listbox',
								default='1',
								data=[{'id':'1', 'value':'Первое значение'}, {'id':'2', 'value':'Второе значение'}],
								size=0) )
"""