"""
	Параметры:
		Только с фото: search[photos]=1
		Искать в заголовке и описании: search[description]=1
		Товары с доставкой: search[courier]=1
		
		Марка: /volkswagen/

		Модель: /golf/

		Цена:
			от: search[filter_float_price%3Afrom]=1
			до: search[filter_float_price%3Ato]=2

		Год выпуска 
			от: search[filter_float_motor_year%3Afrom]=1900
			до: search[filter_float_motor_year%3Ato]=1930

		Пробег: (км)
			от: search[filter_float_motor_mileage%3Afrom]=125000 
			до: search[filter_float_motor_mileage%3Ato]=150000

		Объем двигателя:
			от: search[filter_float_motor_engine_size%3Afrom]=15
			до: earch[filter_float_motor_engine_size%3Ato]=500

		Тип кузова: search[filter_enum_car_body][0]=
			'Кабриолет': 'cabriolet',
			'Пикап': 'pickup',
			'Купе': 'coupe',
			'Универсал': 'estate-car',
			'Хэтчбек': 'hatchback',
			'Минивэн': 'minibus',
			'Внедорожник/Кроссовер': 'off-road-vehicle',
			'Седан': 'sedan',
			'Легковой фургон (до 1,5 т)': 'caravan',
			'Лифтбек': 'liftback',
			'Лимузин': 'limo',
			'Другой': 'other'

		Вид топлива: search[filter_enum_fuel_type][0]=
			'Бензин': '542',
			'Дизель': '543',
			'Другой': '544',
			'Газ': 'gas',
			'Электро': 'electro',
			'Гибрид': 'hybrid',

		Цвет: search[filter_enum_color][0]=
			'Белый': '1',
			'Черный': '2',
			'Синий': '3',
			'Серый': '4',
			'Серебристый': '5',
			'Красный': '6',
			'Зеленый': '7',
			'Апельсин': '8',
			'Асфальт': '9',
			'Бежевый': '10',
			'Бирюзовый': '11',
			'Бронзовый': '12',		
			'Вишнёвый': '13',
			'Голубой': '14',
			'Желтый': '15',
			'Золотой': '17 ',
			'Коричневый': '18',
			'Манголии': '19',
			'Матовый': '20',
			'Оливковый': '21',
			'Розовый': '22',
			'Сафари': '23',
			'Фиолетовый': '24',
			'Хамелеон': '25',

		Коробка передач
		search[filter_enum_transmission_type][0]=
			'Механическая': '545',
			'Автоматическая': '546',
			'Вариатор': '547',
			'Адаптивная': 'adaptive',
			'Типтроник': 'tip-tronic',

		Состояние машины: search[filter_enum_condition][0]=
			'Требует ремонт': 'needs_repairs'
			'Гаражное хранение': 'garage-storage'
			'Не бит': 'not-bit'
			'Не крашен': 'not-colored'
			'Первая регистрация': 'first-registration'
			'Сервисная книжка': 'service-book'
			'После ДТП': 'after-an-accident'
			'Не на ходу': 'not-on-the-move'
			'Взято в кредит: 'taken-on-credit'
			'Первый владелец': 'first-owner'

		Растаможена: search[filter_enum_cleared_customs][0]=
			'Да': 'yes',
			'Нет': 'no',

		Валюта &currency=
			EUR 
			USD


"""

# Формирует url адрес c маркой автомобиля и моделью. Указать модель не указав марку невозможно
# Марка и модель автомобиля должны быть нижнем регистре, пробелы в нужно заменить на -
def create_url(url: str, brand: str=None, model: str=None, currency: str=None):
	url += '/' + brand.lower()
	
	if(model):
		model = model.replace(' ', '-') # Crown victoria -> Crown-victoria

		url += '/' + model.lower()

	url += '/?'

	if(currency in ('EUR', 'USD')):
		url += '&currency=' + currency

	return url

# Добавляет к url адресу фильтр максимальной и минимальной цены
def append_price_filter(url: str, min_price: int=None, max_price: int=None):
	if(min_price):
		url += '&search[filter_float_price%%3Afrom]=%i' % min_price
	if(max_price):
		url += '&search[filter_float_price%%3Ato]=%i' % max_price

	return url

# Добавляет к url адресу фильтр года выпуска 
def append_motor_year(url: str, min_year: int=None, max_year: int=None):
	if(min_year):
		url += '&search[filter_float_motor_year%%3Afrom]=%i' % min_year
	if(max_year):
		url += '&search[filter_float_motor_year%%3Ato]=%i' % max_year

	return url

# Добавляет к url адресу фильтр пробега автомобиля (в км)
def append_motor_mileage(url: str, min_mileage: int=None, max_mileage: int=None):
	if(min_mileage):
		url += '&search[filter_float_motor_mileage%%3Afrom]=%i' % min_mileage
	if(max_mileage):
		url += '&search[filter_float_motor_mileage%%3Ato]=%i' % max_mileage

	return url

# Добавляет к url адресу фильтр объема двигателя
def append_motor_engine_size(url: str, min_motor_engine_size: int=None, max_motor_engine_size: int=None):
	if(min_motor_engine_size):
		url += '&search[filter_float_motor_engine_size%%3Afrom]=%i' % min_motor_engine_size
	if(max_motor_engine_size):
		url += '&search[filter_float_motor_engine_size%%3Ato]=%i' % max_motor_engine_size

	return url

# Добавляет к url адресу фильтр вида кузова
def append_car_body(url: str, type_car_body: str):
	param = '&search[filter_enum_car_body][0]=%s'

	values = {
		'Кабриолет': 'cabriolet',
		'Пикап': 'pickup',
		'Купе': 'coupe',
		'Универсал': 'estate-car',
		'Хэтчбек': 'hatchback',
		'Минивэн': 'minibus',
		'Внедорожник/Кроссовер': 'off-road-vehicle',
		'Седан': 'sedan',
		'Легковой фургон (до 1,5 т)': 'caravan',
		'Лифтбек': 'liftback',
		'Лимузин': 'limo',
		'Другой': 'other',
	}
	
	car_body = values.get(type_car_body)
	
	if (car_body):
		url += param % car_body

	return url

# Добавляет к url адресу фильтр вида топлива
def append_fuel_type(url: str, fuel_type: str):
	param = '&filter_enum_fuel_type][0]=%s'

	values = {
		'Бензин': '542',
		'Дизель': '543',
		'Другой': '544',
		'Газ': 'gas',
		'Электро': 'electro',
		'Гибрид': 'hybrid',
	}

	fuel_type_value = values.get(fuel_type)
	
	if(fuel_type_value):
		url += param % fuel_type_value

	return url

# Добавляет к url адресу фильтр цвета автомобиля
def append_car_color(url: str, car_color: str):
	param = '&search[filter_enum_color][0]=%s'

	values = {
		'Белый': '1',
		'Черный': '2',
		'Синий': '3',
		'Серый': '4',
		'Серебристый': '5',
		'Красный': '6',
		'Зеленый': '7',
		'Апельсин': '8',
		'Асфальт': '9',
		'Бежевый': '10',
		'Бирюзовый': '11',
		'Бронзовый': '12',		
		'Вишнёвый': '13',
		'Голубой': '14',
		'Желтый': '15',
		'Золотой': '17 ',
		'Коричневый': '18',
		'Манголии': '19',
		'Матовый': '20',
		'Оливковый': '21',
		'Розовый': '22',
		'Сафари': '23',
		'Фиолетовый': '24',
		'Хамелеон': '25',
	}

	car_color_value = values.get(car_color)
	
	if(car_color_value):
		url += param % car_color_value

	return url

# Добавляет к url адресу фильтр вида коробки передач
def append_transmission_type(url: str, transmission_type: str):
	param = '&search[filter_enum_transmission_type][0]=%s'

	values = {
		'Механическая': '545',
		'Автоматическая': '546',
		'Вариатор': '547',
		'Адаптивная': 'adaptive',
		'Типтроник': 'tip-tronic',
	}

	transmission_type_value = values.get(transmission_type)
	
	if(transmission_type_value):
		url += param % transmission_type_value

	return url	

# Добавляет к url адресу фильтр cостояния машины
def append_condition(url: str, condition_type: str):
	param = '&search[filter_enum_condition][0]=%s'

	values = {
		'Требует ремонт': 'needs_repairs',
		'Гаражное хранение': 'garage-storage',
		'Не бит': 'not-bit',
		'Не крашен': 'not-colored',
		'Первая регистрация': 'first-registration',
		'Сервисная книжка': 'service-book',
		'После ДТП': 'after-an-accident',
		'Не на ходу': 'not-on-the-move',
		'Взято в кредит': 'taken-on-credit',
		'Первый владелец': 'first-owner',
	}

	condition_type_value = values.get(condition_type)
	
	if(condition_type_value):
		url += param % condition_type_value

	return url

# Добавляет к url адресу фильтр pастаможки автомобиля
def append_cleared_customs(url: str, custom_state: str):
	param = '&search[filter_enum_cleared_customs][0]=%s'

	values = {
		'Да': 'yes',
		'Нет': 'no',
	}

	custom_state_value = values.get(custom_state)
	
	if(custom_state_value):
		url += param % custom_state_value

	return url

# Добавляет к url адресу фильтр валюты
def append_currency_type(url: str, currency: str):
	param = '&currency=%s'
	if(currency in ('USD', 'EUR')):
		url += param % currency

	return url

# 
def test_ctreating_url():
	url = 'https://www.olx.ua/transport/legkovye-avtomobili/'
	url = create_url(url, 'volkswagen', 'golf')
	url = append_price_filter(url, 1000, 2000)
	url = append_motor_year(url, 2001, 2020)
	url = append_motor_mileage(url, 1000, 5000)
	url = append_motor_engine_size(url, 1500, 2000)
	url = append_car_body(url, 'Седан')
	url = append_fuel_type(url, 'Бензин')
	url = append_car_color(url, 'Черный')
	url = append_transmission_type(url, 'Механическая')
	url = append_condition(url, 'Не бит')
	url = append_cleared_customs(url, 'Да')
	url = append_currency_type(url, 'EUR')

	print(url)

# 
if (__name__ == '__main__'):
	test_ctreating_url()

