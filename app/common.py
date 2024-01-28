from collections.abc import Iterable
from dataclasses import dataclass


# return one row query result as dict
def RowToDict(row):
	result = {}
	for column in row.__table__.columns:
		result[column.name] = str(getattr(row, column.name))
	return result

# returl query result as dict list
def RowsToDictList(rows):
	if rows is None:
		return [{}]
	try:
		result = []
		for row in rows:
			dic = {}
			if isinstance(row, Iterable):
				for element in row:
					dic = {**dic, **RowToDict(element)}
				result.append(dic)
			else:
				result.append(RowToDict(row))
		return result
	except AttributeError:
		return [dict(r._mapping) for r in rows]

@dataclass
class Navbar_Button:
	href: str
	title: str
	src: str
	onclick: str

class Button_Home(Navbar_Button):
	href = '/'
	title = 'В начало'
	src = 'home.png'

class Button_Back(Navbar_Button):
	href = ''
	onclick = 'javascript:history.back(); return false;'
	title = 'Назад'
	src = 'home.png'

class Button_List(Navbar_Button):
	href = '',
	onclick = '',
	title = 'Список',
	src = 'list.png'

class Button_Excel(Navbar_Button):
	href = '',
	onclick = '',
	title = 'Скачать отчет Excel',
	src = 'excel.png'

