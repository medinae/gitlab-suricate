from .abstract_logger import AbstractLogger

class NullLogger(AbstractLogger):
	def supports(self, type: str) -> bool:
		return true

	def log(self, level: str, message: str) -> None:
		return None
