


def Ref_Agreement_Types():
	return ['row_id', 'name'], [	{'row_id':0, 'name':''},
									{'row_id':1, 'name':'договор энергоснабжения'},
									{'row_id':2, 'name':'договор купли-продажи'},
									{'row_id':3, 'name':'договор население (квитанции)'},
									{'row_id':4, 'name':'договор хозяйственные нужды'},
									{'row_id':5, 'name':'компенсация потерь сетевых компания'},
									{'row_id':6, 'name':'договор оказания услуг по передаче электрической энергии'},
									{'row_id':7, 'name':'договор купли-продажи в целях компенсации фактических потерь, возникающих в электрических сетях'},
									{'row_id':8, 'name':'договор купли-продажи электричкой энергии в целях компенсации потерь электрической энергии в электрических сетях'}]



def generate_select_options_html( header_data:tuple, current_row_id=0):
	header = header_data[0]
	data =header_data[1]
	result = ''
	for row in data:
		result += f"""<option value="{row[header[0]]}" {( 'selected' if current_row_id == row[header[0]] else '')}>{''.join('{}{}'.format('  ', val) for key, val in row.items())}</option>\n"""
	return result




header,data = Ref_Agreement_Types()

print(generate_select_options_html(Ref_Agreement_Types(),5))