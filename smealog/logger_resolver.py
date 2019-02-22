from .abstract_logger import AbstractLogger
from .null_logger import NullLogger
from typing import Dict

class LoggerResolver:
	def __init__(self, loggers: Dict):
		self.loggers = loggers

	def resolve(self, type: str):
		for logger in self.loggers:
			if not isinstance(logger, AbstractLogger):
				raise ValueError("Only loggers should be injected here")

			if logger.supports(type):
				return logger

		return NullLogger()
