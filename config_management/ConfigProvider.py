import configparser
from typing import Dict

class ConfigProvider:
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.config = config

	def getAppConfig(self) -> Dict[int, str]:
		return self.config['DEFAULT']