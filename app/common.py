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
	def __init__(self, href='/', title='В начало', src='home.png', onclick=''):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick

		

class Button_Back(Navbar_Button):
	def __init__(self, href='', title='Назад', src='back.png', onclick='javascript:history.back(); return false;'):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick


class Button_List(Navbar_Button):
	def __init__(self, href='', title='Список ранее сформированных отчетов', src='list.png', onclick=''):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick


class Button_Excel(Navbar_Button):
	def __init__(self, href='', title='Скачать отчет Excel', src='excel.png', onclick=''):
		self.href = href
		self.title = title
		self.src = src
		self.onclick = onclick

