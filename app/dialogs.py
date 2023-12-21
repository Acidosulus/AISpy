import uuid
from datetime import datetime

class DialogParameters():
	title = ''
	parameters = []
	def __init__(self, title):
		self.title = title
		self.parameters = []

	def append(self, section):
		self.parameters.append(section)

	def get_answers(self, form_elements):
		result_list = []
		for element in  form_elements:
			result_list.append({element[0]:element[1]})
		return result_list

	def __str__(self) -> str:
		cdata = ''
		for parameter in self.parameters:
			cdata += (', 'if len(cdata)>0 else '') + str(parameter) 
		return '{'+f"title:`{self.title}`,"+'parameters:[' + cdata + ']'+'};'

	def add_months(self, lable='Месяц', name=''):
		self.append(  """{lable:`"""+lable+"""`, 
					name:`"""+(name if len(name)>0 else str(uuid.uuid4()))+"""`,
					type:`listbox`,
					default:`"""+f'{datetime.now().month}'+"""`,
					size:`12`,
					data:[{id:`1`, value:`Январь`},{id:`2`, value:`Февраль`},{id:`3`, value:`Март`},{id:`4`, value:`Апрель`},{id:`5`, value:`Май`},{id:`6`, value:`Июнь`},{id:`7`, value:`Июль`},{id:`8`, value:`Август`},{id:`9`, value:`Сентябрь`},{id:`10`, value:`Октярь`},{id:`11`, value:`Ноябрь`},{id:`12`, value:`Декабрь`}]}"""
					)


	def add_years(self, lable='Год', name=''):
			lc_years =''
			for year in range(datetime.now().year-6,datetime.now().year+3):
				lc_years = lc_years + (', ' if len(lc_years)>0 else '') + '{' + f'id:`{year}`, value:`{year}`' + '}'
			self.append( """{lable:`"""+lable+"""`, 
					name:`"""+(name if len(name)>0 else str(uuid.uuid4()))+"""`,
					type:`listbox`,
					default:`"""+f'{datetime.now().year}'+"""`,
					size:`0`,
					data:["""+lc_years+"""]}""")
			


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
		cdata=''
		for element in self.data:
			cdata = cdata + '		'+'{'+f"""id:`{element['id']}`, value:`{element['value']}`"""+'}' #', ' if len(cdata)>0 else ''+
		cdata ='[' + cdata + ']'
		cdata = cdata.replace('}		{','},		{')
		return '{'+f"""lable:`{self.lable}`, name:`{self.name}`, type:`{self.type}`, default:`{self.default}`, size:`{self.size}`, data:{cdata}"""+'}'

testdialog = DialogParameters(title='Заголовок тестового диалога')
testdialog.add_months('Месяц', 'Month')
testdialog.add_years('Год', 'Year')


dialog = DialogParameters(title='Заголовок диалога с параметрами')
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
