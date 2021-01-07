# -*- coding: utf-8 -*-

import os
import sys
import json
import webbrowser
import winsound
import subprocess
import winreg
import hashlib

from PyQt5 import QtCore
from jinja2 import Template



'''
https://pythonru.com/uroki/7-osnovy-shablonizatora-jinja
'''

# 
base_config = {
	'program': {
		'update_interval': 15,
		'play_sound': True,
		'added_to_register': False,
		'currency': 'USD',
	}
}

# 
def timer(timeout: int, target):
	timer_object = QtCore.QTimer()
	# Переменная timeout задает интервал в минутах
	timer_object.singleShot(timeout*1000*60, target)

# 
def start_parser_subprocess(index: str):
	subprocess.run(['python', 'parser.py', index], shell=False)

# 
def get_program_directory():
	return os.path.dirname(sys.argv[0])

# 
def get_config_file():
	return os.path.join(get_program_directory(), 'data', 'config.json') 

# 
def render_page(filename):
	cars = load_json(filename)
	if(cars):
		with open('templates\\index.html', 'r') as file:
			# Загрузка html шаблона 
			html = file.read()
			# Обработка шаблона
			data = Template(html).render(var={'cars': cars})
			# Сохранение обработаного файла
			with open(os.path.join(get_program_directory(), 'index.html'), mode='w') as handler:
				handler.write(data)

			return True
	return False

# 
def show_page():
	if(os.path.exists('index.html')):
		# Запуск брауреза для отображения результатов поиска
		webbrowser.open_new('index.html') 

#
def load_json(filename):
	if(os.stat(filename).st_size > 0):
		with open(filename, mode='r', errors='ignore') as file:
			return json.loads(file.read())

#
def load_config():
	config_file = get_config_file()
	return load_json(config_file)

#
def dump_config(data):
	config_file = get_config_file()
	if(not os.path.exists(config_file)):
		with open(config_file, mode='w') as file:
			file.write('')

	with open(config_file, mode='w') as file:
		return json.dump(data, file, indent=4)

# 
def play_sound():
	winsound.PlaySound('data\\sound.wav', winsound.SND_FILENAME)

# 
def add_programm_to_register():
    REG_PATH = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, 'OlxParser', 0, winreg.REG_SZ, '"%s" --hiden' % sys.argv[0])
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

# 
def create_hash(filename):
	with open(filename, mode='rb') as file:
		bytes_data = file.read()

		sha256 = hashlib.sha256()
		sha256.update(bytes_data)

		return sha256.hexdigest()


