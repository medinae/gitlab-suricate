import configparser

class ConfigProvider:
	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.config = config

	def get_app_config(self):
		return self.config['DEFAULT']