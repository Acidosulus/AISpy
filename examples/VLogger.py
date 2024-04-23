from click import echo, style

class CircularTuple:
	def __init__(self, data):
		self.data = data

	def __getitem__(self, index):
		return self.data[index % len(self.data)]

class Argument():
	def __init__(self, name='', value=None):
		self.name = name
		self.value = value

class Arguments():
	colorPicker = CircularTuple(	(   
										{'name':'red',	    'value':'bright_yellow', },
										{'name':'yellow',   'value':'bright_blue'},
										{'name':'blue',	    'value':'bright_green'},
										{'name':'green',	'value':'bright_cyan'},
										{'name':'cyan',	    'value':'bright_magenta'},
										{'name':'magenta',  'value':'bright_white'},
										{'name':'white',	'value':'bright_red'}
									)
								)
	output_index = 0
	arguments = []
	
	def append(self, arg:Argument):
		self.arguments.append(arg)

	def __str__(self):
		result = ''
		for arg in self.arguments:
			self.output_index += 1
			colors = self.colorPicker[self.output_index]
			result += style(text = arg.name, fg=colors['name']) + ': ' + style(text = arg.value, fg=colors['value'])

def VLog(*args, **kwargs):
	aStore = Arguments()
	print(args, kwargs)
	import inspect
	frames = inspect.stack()
	local_vars = frames[1].frame.f_locals
	for arg in args:
		try:
			var_name = next(name for name, value in local_vars.items() if value is arg)
			print(f"Имя переменной: {var_name}, Значение: {arg}")
			aStore.append(Argument(var_name, arg))
		except StopIteration:
			print(f"Переменная с значением {arg} не найдена")
			aStore.append(Argument('', arg))
	print(aStore)

var1 = 'aaa'
var2 = 1


VLog(var1, var2, 2.2, dict_parameter={1:'tm'}, list_parameter=['g', 'f'])


