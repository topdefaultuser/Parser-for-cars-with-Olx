# -*- coding: utf-8 -*-

import os
import sys
import json
import ctypes
import random

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox, QComboBox,
	QLabel, QSlider, QCheckBox, QLineEdit, QGroupBox, QInputDialog, QMainWindow, QSizePolicy)
from PyQt5 import (QtCore, QtGui)



"""
https://www.tutorialkart.com/matplotlib-tutorial/
http://www.itmathrepetitor.ru/qt5-okna-dlya-vvoda-dannykh-polzovatelya/
https://python-scripts.com/pyqt5#qcombobox-in-qtablewidget
"""

# Это нужно только для меня, а точнее моего ПК
os.chdir(os.path.dirname(sys.argv[0]))

file = open('ui\\data.json')
data = json.loads(file.read())
file.close()

brands = data['brands']
models = data['models']

car_body = [
	'Кабриолет', 'Пикап', 'Купе', 'Универсал', 'Хэтчбек',
	'Минивэн', 'Внедорожник/Кроссовер', 'Седан',
	'Легковой фургон (до 1,5 т)', 'Лифтбек', 'Лимузин', 'Другой',
	]

fuel_type = ['Бензин', 'Дизель', 'Другой', 'Газ', 'Электро', 'Гибрид']

car_colors = [
	'Белый', 'Черный', 'Синий', 'Серый', 'Серебристый', 'Красный', 'Зеленый', 'Апельсин',
	'Асфальт', 'Бежевый', 'Бирюзовый', 'Бронзовый', 'Вишнёвый', 'Голубой', 'Желтый', 'Золотой',
	'Коричневый', 'Манголии', 'Матовый', 'Оливковый', 'Розовый', 'Сафари', 'Фиолетовый', 'Хамелеон'
	]

transmission_type = ['Механическая', 'Автоматическая', 'Вариатор', 'Адаптивная', 'Типтроник']

condition  = ['Требует ремонт', 'Гаражное хранение', 'Не бит', 'Не крашен', 'Первая регистрация', 
	'Сервисная книжка', 'После ДТП', 'Не на ходу', 'Взято в кредит', 'Первый владелец']

cleared_customs = ['Да', 'Нет']

# 
def show_info(title: str, message_text: str):
	QMessageBox.information(None, title, message_text, QMessageBox.Ok)

# 
def show_warning(title: str, message_text: str):
	QMessageBox.warning(None, title, message_text, QMessageBox.Ok)

# 
def show_error(title: str, message_text: str):
	QMessageBox.critical(None, title, message_text, QMessageBox.Ok)

# 
def show_question(title: str, message_text: str):
	result = QMessageBox.question(None, title, message_text, QMessageBox.Yes, QMessageBox.No)
	if(result == 16384):
		return True
	elif(result == 65536):
		return False

# 
def show_input_dialog(title: str, lable: str):
	return QInputDialog.getText(None, title, lable)

# 
class GifPlayer(QtCore.QObject):
    def __init__(self, widget):
        super().__init__()
        self.centralwidget = widget
        self.movie_screen = QLabel(self.centralwidget)
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_screen.setGeometry(QtCore.QRect(0, 0, 699, 305))
        self.movie_screen.setStyleSheet('background-color: rgba(255, 255, 255, 100);')
        self.movie = QtGui.QMovie('ui\\images\\loader.gif')
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie_screen.hide()

	# 
    def start_animation(self):
        self.movie.start()
        self.movie_screen.show()

	# 
    def stop_animation(self):
        self.movie.stop()
        self.movie_screen.hide()

# 
class MThread(QtCore.QThread):
	any_signal = QtCore.pyqtSignal(tuple)
	def __init__(self, widget=None,index=0):
		super(MThread, self).__init__(None)
		self.is_running = True
		self.function = None
		self.index = None
	
	def run(self):
		result = self.function(self.index)
		self.any_signal.emit((result, self.index))

	# 
	def set_params(self, function, index):
		self.function = function
		self.index = index

# 
class Filter(object):
	def __init__(self, config: dict=None):
		self.config = config
		self.form = QWidget()
		self.form.setWindowTitle('Настройка парсера: %s' % self.config['parser_name'])
		self.form.setObjectName('Filter')
		self.form.setFixedSize(600, 250)
		self.comboBox = QComboBox(self.form)
		self.comboBox.setObjectName(u"comboBox")
		self.comboBox.setGeometry(QtCore.QRect(10, 30, 181, 22))
		self.comboBox.activated[str].connect(self.change_models)

		self.comboBox.addItem("Все")
		for brand in brands:
			self.comboBox.addItem(brand)

		self.label = QLabel(self.form)
		self.label.setObjectName(u"label")
		self.label.setGeometry(QtCore.QRect(10, 10, 181, 16))

		self.comboBox_2 = QComboBox(self.form)
		self.comboBox_2.setObjectName(u"comboBox_2")
		self.comboBox_2.setGeometry(QtCore.QRect(210, 30, 181, 22))
		self.label_2 = QLabel(self.form)
		self.label_2.setObjectName(u"label_2")
		self.label_2.setGeometry(QtCore.QRect(210, 10, 181, 16))
		
		self.comboBox_3 = QComboBox(self.form)
		self.comboBox_3.setObjectName(u"comboBox_3")
		self.comboBox_3.setGeometry(QtCore.QRect(10, 80, 181, 22))
		
		self.comboBox_3.addItem("Все")
		for body in car_body:
			self.comboBox_3.addItem(body)

		self.label_6 = QLabel(self.form)
		self.label_6.setObjectName(u"label_6")
		self.label_6.setGeometry(QtCore.QRect(10, 60, 181, 16))
		self.comboBox_4 = QComboBox(self.form)
		self.comboBox_4.setObjectName(u"comboBox_4")
		self.comboBox_4.setGeometry(QtCore.QRect(210, 80, 181, 22))

		self.comboBox_4.addItem("Все")
		for color in car_colors:
			self.comboBox_4.addItem(color)

		self.label_7 = QLabel(self.form)
		self.label_7.setObjectName(u"label_7")
		self.label_7.setGeometry(QtCore.QRect(10, 110, 181, 16))
		self.label_8 = QLabel(self.form)
		self.label_8.setObjectName(u"label_8")
		self.label_8.setGeometry(QtCore.QRect(210, 60, 181, 16))
		self.comboBox_5 = QComboBox(self.form)
		self.comboBox_5.setObjectName(u"comboBox_5")
		self.comboBox_5.setGeometry(QtCore.QRect(10, 130, 181, 22))

		self.comboBox_5.addItem("Все")
		for fuel in fuel_type:
			self.comboBox_5.addItem(fuel)

		self.label_9 = QLabel(self.form)
		self.label_9.setObjectName(u"label_9")
		self.label_9.setGeometry(QtCore.QRect(210, 110, 181, 16))
		self.comboBox_6 = QComboBox(self.form)
		self.comboBox_6.setObjectName(u"comboBox_6")
		self.comboBox_6.setGeometry(QtCore.QRect(210, 130, 181, 22))

		self.comboBox_6.addItem("Все")
		for transmission in transmission_type:
			self.comboBox_6.addItem(transmission)

		self.comboBox_7 = QComboBox(self.form)
		self.comboBox_7.setObjectName(u"comboBox_7")
		self.comboBox_7.setGeometry(QtCore.QRect(10, 180, 181, 22))

		self.comboBox_7.addItem("Все")
		for con in condition:
			self.comboBox_7.addItem(con)

		self.label_10 = QLabel(self.form)
		self.label_10.setObjectName(u"label_10")
		self.label_10.setGeometry(QtCore.QRect(10, 160, 181, 16))
		self.comboBox_8 = QComboBox(self.form)
		self.comboBox_8.setObjectName(u"comboBox_8")
		self.comboBox_8.setGeometry(QtCore.QRect(210, 180, 181, 22))

		self.comboBox_8.addItem("Все")
		for customs in cleared_customs:
			self.comboBox_8.addItem(customs)

		self.label_11 = QLabel(self.form)
		self.label_11.setObjectName(u"label_11")
		self.label_11.setGeometry(QtCore.QRect(210, 160, 181, 16))

		self.base_css_lineEdit = u""

		self.active_css_lineEdit = u"QLineEdit {\n"\
		"	border-width: 1 px;\n"\
		"	border-style: solid;\n"\
		"	border-color: blue;\n"\
		"}"

		self.warning_css_lineEdit = u"QLineEdit {\n"\
		"	border-width: 1 px;\n"\
		"	border-style: solid;\n"\
		"	border-color: red;\n"\
		"}"

		self.lineEdit_2 = QLineEdit(self.form)
		self.lineEdit_2.setObjectName(u"lineEdit_3")
		self.lineEdit_2.setGeometry(QtCore.QRect(410, 30, 86, 21))
		self.lineEdit_2.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_2.setPlaceholderText('от')

		self.label_3 = QLabel(self.form)
		self.label_3.setObjectName(u"label_3")
		self.label_3.setGeometry(QtCore.QRect(410, 5, 181, 21))
		
		self.lineEdit_3 = QLineEdit(self.form)
		self.lineEdit_3.setObjectName(u"lineEdit_2")
		self.lineEdit_3.setGeometry(QtCore.QRect(500, 30, 86, 21))
		self.lineEdit_3.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_3.setPlaceholderText('до')
		
		self.lineEdit_4 = QLineEdit(self.form)
		self.lineEdit_4.setObjectName(u"lineEdit_4")
		self.lineEdit_4.setGeometry(QtCore.QRect(410, 80, 86, 21))
		self.lineEdit_4.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_4.setPlaceholderText('от')


		self.lineEdit_5 = QLineEdit(self.form)
		self.lineEdit_5.setObjectName(u"lineEdit_5")
		self.lineEdit_5.setGeometry(QtCore.QRect(500, 80, 86, 21))
		self.lineEdit_5.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_5.setPlaceholderText('до')

		self.label_4 = QLabel(self.form)
		self.label_4.setObjectName(u"label_4")
		self.label_4.setGeometry(QtCore.QRect(410, 55, 181, 21))
		
		self.label_5 = QLabel(self.form)
		self.label_5.setObjectName(u"label_5")
		self.label_5.setGeometry(QtCore.QRect(410, 105, 181, 21))
		
		self.lineEdit_6 = QLineEdit(self.form)
		self.lineEdit_6.setObjectName(u"lineEdit_6")
		self.lineEdit_6.setGeometry(QtCore.QRect(410, 130, 86, 21))
		self.lineEdit_6.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_6.setPlaceholderText('от')

		self.lineEdit_7 = QLineEdit(self.form)
		self.lineEdit_7.setObjectName(u"lineEdit_7")
		self.lineEdit_7.setGeometry(QtCore.QRect(500, 130, 86, 21))
		self.lineEdit_7.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_7.setPlaceholderText('от')

		self.label_12 = QLabel(self.form)
		self.label_12.setObjectName(u"label_12")
		self.label_12.setGeometry(QtCore.QRect(410, 155, 181, 21))
		
		self.lineEdit_8 = QLineEdit(self.form)
		self.lineEdit_8.setObjectName(u"lineEdit_8")
		self.lineEdit_8.setGeometry(QtCore.QRect(410, 180, 86, 21))
		self.lineEdit_8.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_8.setPlaceholderText('от')
		
		self.lineEdit_9 = QLineEdit(self.form)
		self.lineEdit_9.setObjectName(u"lineEdit_9")
		self.lineEdit_9.setGeometry(QtCore.QRect(500, 180, 86, 21))
		self.lineEdit_9.setStyleSheet(self.base_css_lineEdit)
		self.lineEdit_9.setPlaceholderText('до')

		self.pushButton_exit = QPushButton(self.form)
		self.pushButton_exit.setObjectName(u"pushButtonExit")
		self.pushButton_exit.setGeometry(QtCore.QRect(410, 215, 86, 23))
		self.pushButton_exit.clicked.connect(self.close)

		self.pushButton_ok = QPushButton(self.form)
		self.pushButton_ok.setObjectName(u"pushButtonOk")
		self.pushButton_ok.setGeometry(QtCore.QRect(500, 215, 86, 23))
		# self.pushButton_ok.clicked.connect(self.get_params)

		self.retranslateUi(self.form)

		QtCore.QMetaObject.connectSlotsByName(self.form)
		# Если передан существующий конфиг для перенастройки 
		if(len(self.config) > 2):
			self.set_config()
		self.form.show()

	# 
	def set_config(self):
		self.set_car_brand(self.config['brand'])
		self.set_car_model(self.config['model'])
		self.set_car_body_type(self.config['body_type'])
		self.set_car_body_color(self.config['color'])
		self.set_car_fuel_type(self.config['fuel_type'])
		self.set_car_transmission_type(self.config['transmission_type'])
		self.set_car_condition_type(self.config['condition_type'])
		self.set_car_custom_type(self.config['custom_type'])
		self.set_min_price(self.config['min_price'])
		self.set_max_price(self.config['max_price'])
		self.set_min_engine_size(self.config['min_engine_size'])
		self.set_max_engine_size(self.config['max_engine_size'])
		self.set_min_motor_year(self.config['min_motor_year'])
		self.set_max_motor_year(self.config['max_motor_year'])
		self.set_min_motor_mileage(self.config['min_motor_mileage'])
		self.set_max_motor_mileage(self.config['max_motor_mileage'])

	#	 
	def retranslateUi(self, Form):
		self.label.setText(QApplication.translate("Form", u"\u041c\u0430\u0440\u043a\u0430 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044f", None))
		self.label_2.setText(QApplication.translate("Form", u"\u041c\u043e\u0434\u0435\u043b\u044c", None))
		self.label_6.setText(QApplication.translate("Form", u"\u0422\u0438\u043f \u043a\u0443\u0437\u043e\u0432\u0430", None))
		self.label_7.setText(QApplication.translate("Form", u"\u0412\u0438\u0434 \u0442\u043e\u043f\u043b\u0438\u0432\u0430", None))
		self.label_8.setText(QApplication.translate("Form", u"\u0426\u0432\u0435\u0442", None))
		self.label_9.setText(QApplication.translate("Form", u"\u041a\u043e\u0440\u043e\u0431\u043a\u0430 \u043f\u0435\u0440\u0435\u0434\u0430\u0447", None))
		self.label_10.setText(QApplication.translate("Form", u"\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u043c\u0430\u0448\u0438\u043d\u044b", None))
		self.label_11.setText(QApplication.translate("Form", u"\u0420\u0430\u0441\u0442\u0430\u043c\u043e\u0436\u0435\u043d\u0430", None))
		self.label_3.setText(QApplication.translate("Form", u"\u0426\u0435\u043d\u0430\u0020\u0028\u0433\u0440\u043d\u0029", None))
		self.lineEdit_4.setText("")
		self.lineEdit_5.setText("")
		self.label_4.setText(QApplication.translate("Form", u"\u041e\u0431\u044a\u0435\u043c \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044f", None))
		self.label_4.setText(QApplication.translate("Form", 
		u"\u041e\u0431\u044a\u0435\u043c\u0020\u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044f\u0020\u0028\u0441\u043c\u0020\u043a\u0443\u0431\u002e\u0029", None))
		self.label_5.setText(QApplication.translate("Form", u"\u0413\u043e\u0434 \u0432\u044b\u043f\u0443\u0441\u043a\u0430", None))
		self.lineEdit_6.setText("")
		self.lineEdit_7.setText("")
		self.label_12.setText(QApplication.translate("Form", u"\u041f\u0440\u043e\u0431\u0435\u0433\u0020\u0028\u043a\u043c\u0029", None))
		self.lineEdit_8.setText("")
		self.lineEdit_9.setText("")
		self.pushButton_exit.setText(QApplication.translate("Form", "Отмена", None)) 
		self.pushButton_ok.setText(QApplication.translate("Form", "Применить", None)) 

	# 
	def change_models(self):
		car_barand = self.get_car_brand()

		self.comboBox_2.clear()
		self.comboBox_2.addItem("Все")
		for model in models[car_barand].keys():
			self.comboBox_2.addItem(model)
		
	# 
	def get_car_brand(self):
		return self.comboBox.currentText()

	# 
	def get_car_model(self):
		return self.comboBox_2.currentText()
	
	# 
	def get_car_body_type(self):
		return self.comboBox_3.currentText()

	# 
	def get_car_body_color(self):
		return self.comboBox_4.currentText()

	# 
	def get_car_fuel_type(self):
		return self.comboBox_5.currentText()

	# 
	def get_car_transmission_type(self):
		return self.comboBox_6.currentText()

	# 
	def get_car_condition_type(self):
		return self.comboBox_7.currentText()

	# 
	def get_car_custom_type(self):
		return self.comboBox_8.currentText()
	
	# 
	def get_min_price(self):
		value = self.lineEdit_2.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_2.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_2.setStyleSheet(self.warning_css_lineEdit)
			return None 

	# 
	def get_max_price(self):
		value = self.lineEdit_3.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_3.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_3.setStyleSheet(self.warning_css_lineEdit)
			return None

	# 
	def get_min_engine_size(self):
		value = self.lineEdit_4.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_4.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_4.setStyleSheet(self.warning_css_lineEdit)
			return None

	# 
	def get_max_engine_size(self):
		value = self.lineEdit_5.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_5.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_5.setStyleSheet(self.warning_css_lineEdit)
			return None 

	# 
	def get_min_motor_year(self):
		value = self.lineEdit_6.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_6.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_6.setStyleSheet(self.warning_css_lineEdit)
			return None 

	# 
	def get_max_motor_year(self):
		value = self.lineEdit_7.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_7.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_7.setStyleSheet(self.warning_css_lineEdit)
			return None

	# 
	def get_min_motor_mileage(self):
		value = self.lineEdit_8.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_8.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_8.setStyleSheet(self.warning_css_lineEdit)
			return None

	# 
	def get_max_motor_mileage(self):
		value = self.lineEdit_9.text()
		if(value == ''):
			return None
		elif(value.isdigit()):
			self.lineEdit_9.setStyleSheet(self.base_css_lineEdit)
			return int(value)
		else:
			self.lineEdit_9.setStyleSheet(self.warning_css_lineEdit)
			return None
		
	# 
	def set_car_brand(self, brand):
		self.comboBox.setCurrentText(brand.capitalize())
		self.change_models()

	# 
	def set_car_model(self, model):
		self.comboBox_2.setCurrentText(model)
	
	# 
	def set_car_body_type(self, body_type):
		self.comboBox_3.setCurrentText(body_type)

	# 
	def set_car_body_color(self, color):
		self.comboBox_4.setCurrentText(color)

	# 
	def set_car_fuel_type(self, fuel_type):
		self.comboBox_5.setCurrentText(fuel_type)

	# 
	def set_car_transmission_type(self, transmission_type):
		self.comboBox_6.setCurrentText(transmission_type)

	# 
	def set_car_condition_type(self, condition_type):
		self.comboBox_7.setCurrentText(condition_type)

	# 
	def set_car_custom_type(self, custom_type):
		self.comboBox_8.setCurrentText(custom_type)
	
	# 
	def set_min_price(self, min_price):
		if(min_price):
			self.lineEdit_2.setText(str(min_price)) 

	# 
	def set_max_price(self, max_price):
		if(max_price):
			self.lineEdit_3.setText(str(max_price))

	# 
	def set_min_engine_size(self, min_engine_size):
		if(min_engine_size):
			self.lineEdit_4.setText(str(min_engine_size))

	# 
	def set_max_engine_size(self, max_engine_size):
		if(max_engine_size):
			self.lineEdit_5.setText(str(max_engine_size))

	# 
	def set_min_motor_year(self, min_motor_year):
		if(min_motor_year):
			self.lineEdit_6.setText(str(min_motor_year)) 

	# 
	def set_max_motor_year(self, max_motor_year):
		if(max_motor_year):
			self.lineEdit_7.setText(str(max_motor_year))

	# 
	def set_min_motor_mileage(self, min_motor_mileage):
		if(min_motor_mileage):
			self.lineEdit_8.setText(str(min_motor_mileage))

	# 
	def set_max_motor_mileage(self, max_motor_mileage):
		if(max_motor_mileage):
			self.lineEdit_9.setText(str(max_motor_mileage))

	#
	def close(self):
		self.form.close()

	# 
	def get_params(self):
		brand = self.get_car_brand().lower()
		model = self.get_car_model()
		body_type = self.get_car_body_type()
		fuel_type = self.get_car_fuel_type()
		color = self.get_car_body_color()
		transmission_type = self.get_car_transmission_type()
		condition_type = self.get_car_condition_type()
		custom_type =  self.get_car_custom_type()

		min_price = self.get_min_price()
		max_price = self.get_max_price()

		min_engine_size = self.get_min_engine_size()
		max_engine_size = self.get_max_engine_size()

		min_motor_year = self.get_min_motor_year()
		max_motor_year = self.get_max_motor_year()

		min_motor_mileage = self.get_min_motor_mileage()
		max_motor_mileage = self.get_max_motor_mileage()

		self.config.update({
			'brand': brand,
			'model': model,
			'body_type': body_type,
			'fuel_type': fuel_type,
			'color': color,
			'transmission_type': transmission_type,
			'condition_type': condition_type,
			'custom_type': custom_type,
			'min_price': min_price,
			'max_price': max_price, 
			'min_engine_size': min_engine_size,
			'max_engine_size': max_engine_size,
			'min_motor_year': min_motor_year,
			'max_motor_year': max_motor_year,
			'min_motor_mileage': min_motor_mileage,
			'max_motor_mileage': max_motor_mileage,
		})

		return self.config.copy()

# 
class Preview(object):
	def __init__(self, index: int, caption: str, amount: int):
		self.w = 400
		self.h = 48
		self.form_index = index
		self.caption = caption
		self.amount = amount
		self.window_opacity = 1
		self.window_delay = 1000*20*1 # 
		self.show_function = None
		self.form = QWidget()
		self.form.setFixedSize(self.w, self.h)
		self.form.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)
		self.form.setWindowOpacity(0.8)

		self.title = QLabel(self.form)
		self.title.setObjectName(u"label_2")
		self.title.setGeometry(QtCore.QRect(10, 10, 121, 31))
		self.title.setText(self.caption)
		self.title.setStyleSheet('color: blue; font-size: 14px;')
		setattr(self.title, 'mousePressEvent', lambda event: self.exec_show_function())

		self.title = QLabel(self.form)
		self.title.setObjectName(u"label_2")
		self.title.setGeometry(QtCore.QRect(320, 10, 121, 31))
		self.title.setText(str(self.amount))
		self.title.setStyleSheet('color: red; font-size: 14px;')
		setattr(self.title, 'mousePressEvent', lambda event: self.exec_show_function())

		self.button = QLabel(self.form)
		self.button.setObjectName(u"label_3")
		self.button.setGeometry(QtCore.QRect(369, 15, 21, 21))
		self.button.setPixmap(QtGui.QPixmap(u"ui\\Images\\close.ico"))
		self.button.setText("")
		setattr(self.button, 'mousePressEvent', lambda event: self.close())
	
	# 
	def show(self):
		self.form.move(self.get_x_position(), self.get_y_position())
		self.title.show()
		self.button.show()
		self.form.show()
		self.timer(self.window_delay, self.update)

	# 
	def set_title(self, title):
		self.title.setText(title)

	#
	def get_screensize(self):
	    user32 = ctypes.windll.user32
	    screensize_x = user32.GetSystemMetrics(0)
	    screensize_y = user32.GetSystemMetrics(1)
	    return (screensize_x, screensize_y - 50)	 

	# 
	def get_x_position(self):
	    screensize_x, _ = self.get_screensize()
	    position_x = screensize_x - self.w - 5
	    return position_x

	# 
	def get_y_position(self):
	    _, screensize_y = self.get_screensize()
	    position_y = screensize_y - ((self.h + 2) * self.form_index)
	    return position_y

	# 
	def timer(self, timeout: int, target):
	    timer_object = QtCore.QTimer()
	    timer_object.singleShot(timeout, target)

	# 
	def update(self):
		#!
		self.window_opacity = ((self.window_opacity*10)-1)/10 
		self.form.setWindowOpacity(self.window_opacity)

		if(self.window_opacity == 0.0):
			self.close()
		else:
			self.timer(50, self.update)

	# 
	def set_show_function(self, function, *args):
		self.show_function = function
		self.args = args

	# 
	def exec_show_function(self):
		self.show_function(*self.args)

	# 
	def close(self):
		self.form.close()

# Главное окно программы
class Window(object):
	"""		
		Создание графического интерфейса:
			window = Window()
			window.create_ui() # Вызывает метод init_ui
		
		Добавление нового парсера:
			window.append_parser() # Вызывает мотод init_parser

		Изменение парсера:
			window.edit_parser() # Вызывает мотод repaint_parser

		Удаление парсера:
			window.delete_parser()
			# После удаление парсера вызывает мотод update_ui для обновление графического интерфейса

		Просмотр результатов поска парсера:
			window.show_parser_data()

		Обновление графического интерфейса:
			window.update_ui()

	"""
	def __init__(self):
		self.form = QWidget()
		self.form.setWindowTitle('Парсер легковых автомобилей с Olx')
		self.groupBox = QGroupBox(self.form)
		self.max_amount_parsers = 7
		self.indent = 30
		self.parsers = {}
		self.configs = {}
		self.parse_function = None
		self.show_function = None
		self.dump_function = None
		self.tmp_directory = None
		self.loader = GifPlayer(self.form)

	# 
	def init_ui(self):
		self.form.setObjectName('Form')
		self.form.setFixedSize(699, 305)
		self.groupBox.setObjectName(u"groupBox")
		self.groupBox.setGeometry(QtCore.QRect(10, 10, 675, 261))
		self.groupBox.setTitle('Парсеры')

		self.label = QLabel(self.groupBox)
		self.label.setObjectName(u"label")
		self.label.setGeometry(QtCore.QRect(20, 20, 147, 14))
		self.label.setText('Имя парсера')

		self.label_4 = QLabel(self.groupBox)
		self.label_4.setObjectName(u"label_3")
		self.label_4.setGeometry(QtCore.QRect(435, 20, 61, 16))
		self.label_4.setText('Найдено')

		QtCore.QMetaObject.connectSlotsByName(self.form)

	# Используется при включении программы для установки загруженых данных о парсерах  
	def set_parsers_config(self, parsers_config):
		self.configs = parsers_config

	# 
	def set_parse_function(self, function):
		self.parse_function = function

	# 
	def set_show_function(self, function):
		self.show_function = function

	#   
	def set_dump_function(self, function):
		self.dump_function = function

	# 
	def set_tmp_directory(self, directory):
		self.tmp_directory = directory

	#
	def set_amount_caption(self, index: str, amount: str):
		parser = self.parsers.get(index)
		if(parser):
			parser['amount'].setText(amount)

	# 
	def find_empty_key_from_new_parser(self):
		for index in range(1, self.max_amount_parsers+1):
			index = str(index)
			if(not self.parsers.get(index)):
				return index

	# 
	def move_append_button(self):
		if(len(self.parsers) < self.max_amount_parsers):
			self.AppendPushButton.setGeometry(QtCore.QRect(20, 15+self.indent*(len(self.parsers)+1), 101, 21))
			self.AppendPushButton.show()
		else:
			self.AppendPushButton.hide()

	#
	def create_append_button(self):
		self.AppendPushButton = QPushButton(self.groupBox)
		self.AppendPushButton.setObjectName(u"pushButton_4")
		self.AppendPushButton.setGeometry(QtCore.QRect(20, 50, 101, 21))
		icon = QtGui.QIcon()
		icon.addFile(u"ui\\Images\\add.ico",  QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.AppendPushButton.setIcon(icon)
		self.AppendPushButton.setIconSize(QtCore.QSize(12, 12))
		self.AppendPushButton.setText('Добавить')
		self.AppendPushButton.setToolTip('Добавить новый парсер')
		self.AppendPushButton.clicked.connect(self.append_parser)
	
	# 
	def create_sound_checkbox(self):
		self.sound_checkBox_1 = QCheckBox(self.form)
		self.sound_checkBox_1.setGeometry(QtCore.QRect(11, 280, 170, 17))
		self.sound_checkBox_1.setText('Звуковое оповищение ')

		if(self.configs['program']['play_sound']):
		    self.sound_checkBox_1.setChecked(True)

		self.sound_checkBox_1.setObjectName('checkBox_3')
		self.sound_checkBox_1.clicked.connect(self.change_sound_effect)
	
	# 
	def change_sound_effect(self):
		if(self.sound_checkBox_1.isChecked()):
			self.configs['program']['play_sound'] = True
		else:
			self.configs['program']['play_sound'] = False

		self.dump_parsers_config()

	# 
	def create_horizontal_slider(self):
		timeout = self.configs['program']['update_interval']

		self.horizontalSlider_label_1 = QLabel(self.form)
		self.horizontalSlider_label_1.setGeometry(QtCore.QRect(400, 280, 180, 16))
		self.horizontalSlider_label_1.setObjectName('label_1')
		self.horizontalSlider_label_1.setText('Интервал: %i (мин.)' % timeout)

		self.horizontalSlider = QSlider(self.form)
		self.horizontalSlider.setGeometry(QtCore.QRect(520, 280, 165, 22))
		self.horizontalSlider.setMinimum(1)
		self.horizontalSlider.setMaximum(120)

		self.horizontalSlider.setProperty('value', timeout)	 

		self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
		self.horizontalSlider.setObjectName('horizontalSlider')
		self.horizontalSlider.valueChanged.connect(self.update_timeout)

	# 
	def update_timeout(self):
		timeout = self.horizontalSlider.value()
		self.configs['program']['update_interval'] = timeout
		self.horizontalSlider_label_1.setText('Интервал: %i (мин.)' % timeout)
		self.dump_parsers_config()

	# 
	def create_currency_checkboxes(self):
		self.label_1 = QLabel(self.form)
		self.label_1.setGeometry(QtCore.QRect(180, 280, 170, 17))
		self.label_1.setText('Валюта:')
		# Гривны
		self.currency_checkBox_1 = QCheckBox(self.form)
		self.currency_checkBox_1.setGeometry(QtCore.QRect(230, 280, 170, 17))
		self.currency_checkBox_1.setText('UAH')

		if(self.configs['program']['currency'] == 'UAH'):
		    self.currency_checkBox_1.setChecked(True)

		self.currency_checkBox_1.setObjectName('currency_checkBox_1')
		self.currency_checkBox_1.clicked.connect(lambda: self.change_currency('UAH'))	

		# Доллары 
		self.currency_checkBox_2 = QCheckBox(self.form)
		self.currency_checkBox_2.setGeometry(QtCore.QRect(280, 280, 170, 17))
		self.currency_checkBox_2.setText('USD')

		if(self.configs['program']['currency'] == 'USD'):
		    self.currency_checkBox_2.setChecked(True)

		self.currency_checkBox_2.setObjectName('currency_checkBox_2')
		self.currency_checkBox_2.clicked.connect(lambda: self.change_currency('USD'))	

		# Евро
		self.currency_checkBox_3 = QCheckBox(self.form)
		self.currency_checkBox_3.setGeometry(QtCore.QRect(330, 280, 170, 17))
		self.currency_checkBox_3.setText('EUR')

		if(self.configs['program']['currency'] == 'EUR'):
		    self.currency_checkBox_3.setChecked(True)

		self.currency_checkBox_3.setObjectName('currency_checkBox_3')
		self.currency_checkBox_3.clicked.connect(lambda: self.change_currency('EUR'))	

	# 
	def change_currency(self, currency):
		if(currency == 'UAH'):
			self.currency_checkBox_1.setChecked(True)
			self.currency_checkBox_2.setChecked(False)
			self.currency_checkBox_3.setChecked(False)

		elif(currency == 'USD'):
			self.currency_checkBox_1.setChecked(False)
			self.currency_checkBox_2.setChecked(True)
			self.currency_checkBox_3.setChecked(False)

		elif(currency == 'EUR'):
			self.currency_checkBox_1.setChecked(False)
			self.currency_checkBox_2.setChecked(False)
			self.currency_checkBox_3.setChecked(True)

		self.configs['program']['currency'] = currency
		self.dump_parsers_config()


	# 
	def create_ui(self):
		self.init_ui()
		self.create_append_button()
		self.create_parsers()
		self.move_append_button()

		# 
		self.create_horizontal_slider()
		self.create_sound_checkbox()
		self.create_currency_checkboxes()
		# 
		self.form.show()

	# 
	def delete_parser(self, index: str):
		responce = show_question('Внимание!', 
			'Вы точно хотите удалить парсер %s?' % self.configs.get(index)['parser_name'])
		
		if(responce is True):
			parser = self.parsers.get(index)
			if(parser):
				# Удаляем графические елементы
				parser['title'].deleteLater()
				parser['amount'].deleteLater()
				parser['update_button'].deleteLater()
				parser['delete_button'].deleteLater()
				parser['edit_button'].deleteLater()
				parser['show_button'].deleteLater()
				# Удаляем остальные данные парсера
				del self.parsers[index]
				del self.configs[index]
				# Обновление графического интерфейса
				self.update_ui()
				self.dump_parsers_config()

	# Изменение парсера
	def edit_parser(self, index: str):
		# Вызывается окно настройки фильтра с текущими параметрами парсера
		self.Filter = Filter(self.configs[index])
		# Привязка собственного метода change_parser к кнопке применить формы фильтра 
		self.Filter.pushButton_ok.clicked.connect(lambda: self.repaint_parser(index))

	# 
	def show_results_update(self, t: tuple):
		result, index = t
		# Остановка анимации 
		self.loader.stop_animation()
		# Устанавливает новое число в пункте "найдено"
		self.set_amount_caption(index, str(result))
			
		if(result == 0):
			show_info('Упс...', 'К сожалению, ничего не найдено!')
		else:
			show_info('Успех!', 'Найдено %i вариантов' % result)

	# Обновление парсера
	def update_parser(self, index):
		parser = self.parsers.get(index)
		if(parser):
			self.loader.start_animation()
			self.thread = MThread(self.form, 1)
			self.thread.any_signal.connect(self.show_results_update)
			self.thread.set_params(self.parse_function, index)
			self.thread.start()

	# Продолжение изменение парсера
	def repaint_parser(self, index: str):
		parser = self.parsers.get(index)
		if(parser):
			# Удаляем графические елементы
			parser['title'].deleteLater()
			parser['amount'].deleteLater()
			parser['update_button'].deleteLater()
			parser['delete_button'].deleteLater()
			parser['edit_button'].deleteLater()
			parser['show_button'].deleteLater()
			
			self.init_parser(index)
			self.update_ui()
			self.dump_parsers_config()

	# Добавления нового парсера
	def append_parser(self):
		text, status = show_input_dialog('Окно ввода', 'Укажите имя нового парсера:')
		if(status == True):
			# Вызывается окно настройки фильтра
			self.Filter = Filter({'parser_name': text, 'tmp_file': 'temp\\%i.json' % random.randint(11111111, 99999999999)})
			# Привязка собственного метода init_parser к кнопке применить формы фильтра
			self.Filter.pushButton_ok.clicked.connect(self.init_parser) 

	# Продолжение добавления нового парсера
	def init_parser(self, parser_index: str=None):
		if(not parser_index):
			# Определение пустого индекса парсера для хранения в словаре self.parsers
			parser_index = self.find_empty_key_from_new_parser()
		# Получение данных фильтра
		parser_config = self.Filter.get_params()
		self.Filter.close()
		# Отрисовка графических елементов нового парсера
		self.create_parser(parser_index, parser_config)
		# Смещение кнопки "добавить"
		self.move_append_button()
		self.dump_parsers_config()
		self.update_parser(parser_index)

	# Формирует заголовок парсера
	def create_parser_caption(self, config):
		return config['parser_name']

	# Формирует подсказку для парсера
	def create_parser_tiptool(self, config):
		params = {'brand': 'Марка', 'model': 'Модель', 'body_type': 'Тип кузова', 'color': 'Цвет', 'fuel_type': 'Тип топлива', 
				'condition_type': 'Состояние', 'custom_type': 'Растаможена'}
		
		tiptool = ''

		for param in config:
			if(params.get(param)):
				tiptool += '%s: %s\n' % (params[param], config[param])

		if(config['min_price'] or config['max_price']):
			string = 'Цена ' 
			if(config['min_price']):
				string += 'от: %i ' % config['min_price']
			if(config['max_price']):
				string += 'до: %i ' % config['max_price']

			tiptool += string + 'грн. \n'

		if(config['min_engine_size'] or config['max_engine_size']):
			string = 'Объем двигателя ' 
			if(config['min_engine_size']):
				string += ' от: %i ' % config['min_engine_size']
			if(config['max_engine_size']):
				string += 'до: %i ' % config['max_engine_size']

			tiptool += string + 'см куб.\n'

		if(config['min_motor_year'] or config['max_motor_year']):
			string = 'Год выпуска ' 
			if(config['min_motor_year']):
				string += 'от: %i ' % config['min_motor_year']
			if(config['max_motor_year']):
				string += 'до: %i ' % config['max_motor_year']

			tiptool += string + ' рр. \n'

		if(config['min_motor_mileage'] or config['max_motor_mileage']):
			string = 'Пробег ' 
			if(config['min_motor_mileage']):
				string += 'от: %i ' % config['min_motor_mileage']
			if(config['max_motor_mileage']):
				string += 'до: %i ' % config['max_motor_mileage']

			tiptool += string + 'км. \n'

		return tiptool.rstrip('\n')

	# 
	def create_parser(self, index: str, config):
		position = len(self.parsers)+1
		label_2 = QLabel(self.groupBox)
		label_2.setObjectName(u"title_%i" % random.randint(99999, 9999999))
		label_2.setGeometry(QtCore.QRect(20, self.indent*position+15, 451, 16))

		tiptool = self.create_parser_tiptool(config)
		caption = self.create_parser_caption(config)

		label_2.setText(QApplication.translate("Form", caption, None))
		label_2.setToolTip(tiptool)
		label_2.show()

		label_3 = QLabel(self.groupBox)
		label_3.setObjectName(u"amount_%i" % random.randint(99999, 9999999))
		label_3.setGeometry(QtCore.QRect(450, self.indent*position+15, 41, 16))
		label_3.setText(QApplication.translate("Form", u"0", None))
		label_3.show()

		pushButton_0 = QPushButton(self.groupBox)
		pushButton_0.setObjectName(u"edit_push_button_%i" % random.randint(99999, 9999999))
		pushButton_0.setGeometry(QtCore.QRect(530, self.indent*position+15, 30, 21))
		icon = QtGui.QIcon()
		icon.addFile(u"ui\\Images\\update.ico",  QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		pushButton_0.setIcon(icon)
		pushButton_0.setToolTip('Обновить парсер')
		pushButton_0.clicked.connect(lambda: self.update_parser(index))
		pushButton_0.show()

		pushButton_1 = QPushButton(self.groupBox)
		pushButton_1.setObjectName(u"edit_push_button_%i" % random.randint(99999, 9999999))
		pushButton_1.setGeometry(QtCore.QRect(565, self.indent*position+15, 30, 21))
		icon = QtGui.QIcon()
		icon.addFile(u"ui\\Images\\edit.ico",  QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		pushButton_1.setIcon(icon)
		pushButton_1.setToolTip('Изменить парсер')
		pushButton_1.clicked.connect(lambda: self.edit_parser(index))
		pushButton_1.show()
		
		pushButton_2 = QPushButton(self.groupBox)
		pushButton_2.setObjectName(u"close_push_button_%i" % random.randint(99999, 9999999))
		pushButton_2.setGeometry(QtCore.QRect(600, self.indent*position+15, 30, 21))
		icon1 = QtGui.QIcon()
		icon1.addFile(u"ui\\Images\\close.ico",  QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		pushButton_2.setIcon(icon1)
		pushButton_2.setToolTip('Удалить парсер')
		pushButton_2.clicked.connect(lambda: self.delete_parser(index))
		pushButton_2.show()

		pushButton_3 = QPushButton(self.groupBox)
		pushButton_3.setObjectName(u"show_push_button_%i" % random.randint(99999, 9999999))
		pushButton_3.setGeometry(QtCore.QRect(635, self.indent*position+15, 30, 21))
		icon2 = QtGui.QIcon()
		icon2.addFile(u"ui\\Images\\show.ico", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		pushButton_3.setIcon(icon2)
		pushButton_3.setToolTip('Просмотреть результаты')
		pushButton_3.clicked.connect(lambda: self.show_function(index))
		pushButton_3.show()

		self.parsers[index] = {
				'parser': index,
				'title': label_2,
				'amount': label_3,
				'update_button': pushButton_0, 
				'edit_button': pushButton_1,
				'delete_button': pushButton_2,
				'show_button': pushButton_3,
			}

		self.configs[index] = config

	# Создание множества парсеров вызовом метода create_parser()
	def create_parsers(self):
		for index in range(1, len(self.configs)+1):
			index = str(index)

			if(self.configs.get(index)):
				if(int(index) > self.max_amount_parsers):
					break
				else:
					self.create_parser(index, self.configs[index])

	# 
	def update_ui(self):
		if(len(self.parsers) > 0):
			for index, key in enumerate(self.parsers, 1):
				elements = self.parsers.get(key)
				if(elements):
					elements['title'].move(20, self.indent*index+15)
					elements['amount'].move(450, self.indent*index+15)
					elements['update_button'].move(530, self.indent*index+15)
					elements['edit_button'].move(565, self.indent*index+15)
					elements['delete_button'].move(600, self.indent*index+15)
					elements['show_button'].move(635, self.indent*index+15)

		self.move_append_button()

	#
	def dump_parsers_config(self): 
		self.dump_function(self.configs)

