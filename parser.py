import sys

from spider import spider 
from utils import load_config

'''
Поскольку не удалось устранить ошибку twisted.internet.error.ReactorNotRestartable
перезагрузкой модуля spider, решил вынести функцию update_parser в отдельный файл 
и запускать отдельно от основной программы
'''

# Обновление парсера
def update_parser():
	if(len(sys.argv) > 1):
		index = sys.argv[1]

		configs = load_config()

		if(configs):
			config = configs.get(index)

			if(config):
				spider.parse_data(config, configs['program']['currency'])

# 
if(__name__ == '__main__'):
	update_parser()

