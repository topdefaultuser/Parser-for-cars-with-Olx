import sys
import os

from ui import ui

import utils



# Отображение результатов поиска
def render(index):
	configs = utils.load_config()

	if(configs):
		config = configs.get(index)

		if(config):
			filename = config['tmp_file']

			if(os.path.exists(filename)):
				if(utils.render_page(filename)):
					utils.show_page()
				else:
					ui.show_error('Критическая ошибка!', 'Не удалось отрендерить страницу.')
			else:
				ui.show_error('Критическая ошибка!', 'Не удалось найти временный файл парсера.\n'\
					'Обновите данные парсера и попробуйте снова.')

# Обновление парсера
def update_parser(index):
	# 	
	utils.start_parser_subprocess(index)
	# 
	configs = utils.load_config()

	if(configs):
		config = configs.get(str(index))

		if(config):
			filename = config['tmp_file']

			if(os.path.exists(filename)):
				data = utils.load_json(filename)
				# 
				config['last_hash'] = utils.create_hash(filename)
				# Обновления конфигурации 
				utils.dump_config(configs)

				if(data):
					return len(data) # Возвращает количество найденых автомобилей
	return 0

# 
def update_parsers():
	configs = utils.load_config()
	previewers = []

	if(configs):
		amount = 1
		for index in range(1, 8):
			index = str(index)

			config = configs.get(index)
			
			if(config):
				# 
				utils.start_parser_subprocess(index)

				filename = config['tmp_file']

				if(os.path.exists(filename)):
					# 
					new_hash = utils.create_hash(filename)
					# Сравнивание хешей файлов
					if(config['last_hash'] != new_hash):
						# 
						config['last_hash'] = new_hash
						# Обновления конфигурации 
						utils.dump_config(configs)
						
						# Загрузка списка найденых автомобилей 
						data = utils.load_json(filename)
						#
						if(data):
							previewer = ui.Preview(amount, config['parser_name'], len(data))
							previewer.set_show_function(render, index)

							previewers.append(previewer)
							amount += 1

		# После завершения парсинга отображет все окна
		for previewer in previewers:
			previewer.show()

		# Если у ключа play_sound значение True, после завершения парсинга и отображения всех окон 
		# программа воспроизведёт звуковой сигнал об окончании процесса парсинга
		if(configs['program']['play_sound']):
			utils.play_sound()
		
		# Устанавливает новый таймер для обновления 
		utils.timer(configs['program']['update_interval'], update_parsers)
	
	else:
		# Получаем базовый конфиг
		config = utils.base_config
		# Сохраняе новый конфиг
		utils.dump_config(config)

# 
def update_ui(ui):
	configs = utils.load_config()

	for index in range(1, 8):
		index = str(index)

		config = configs.get(index)

		if(config):
			filename = config['tmp_file']

			if(os.path.exists(filename)):
				# Загрузка списка найденых автомобилей 
				data = utils.load_json(filename)
				#
				if(data):
					ui.set_amount_caption(index, str(len(data)))
			# Если файл по катой-то причине отсутствует
			else:
				result = update_parser(index)
				ui.set_amount_caption(index, str(result))

# 
def main():
	# Это нужно только для меня, а точнее моего ПК
	os.chdir(utils.get_program_directory())
	# 
	app = ui.QApplication(sys.argv)
	# 
	config_file = utils.get_config_file()

	if(os.path.exists(config_file)):
		config = utils.load_config()
	else:
		ui.show_warning('Внимание', 'Файл конфигурации отсуцтвует!')
		config = utils.base_config
		# Сохранение базового конфига
		utils.dump_config(config)

	# Если программа запущена с реестра
	# Автоматически парсит данные с заданым интервалом
	if('--hiden' in sys.argv):
		utils.timer(config['program']['update_interval'], update_parsers)

	else:
		# 
		window = ui.Window()
		window.set_parsers_config(config)
		window.set_dump_function(utils.dump_config)
		window.set_show_function(render)
		window.set_parse_function(update_parser)
		window.create_ui()
		# 
		update_ui(window)
		# 
		if(config['program']['added_to_register'] == False):
			if(ui.show_question('Внимание', 'Добавьте приложение в реестр, или создайте ярлык приложения в папке автозагрузки.\n'\
																									'Добавить приложение в реестр?')):
				if(utils.add_programm_to_register()): # Вернет True если запись в реестр cделана успешно 
					config['program'].update({'added_to_register': True})
					utils.dump_config(config)
				else:
					ui.show_error('Ошибка записи в реестр', 'Не удалось зделать запись в реестр.\n'\
									'Запустите программу с правами администратора и попробуйте снова.')

	# 
	sys.exit(app.exec_())

# 
if(__name__ == '__main__'):
	main()
