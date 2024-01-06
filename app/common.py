from collections.abc import Iterable

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
