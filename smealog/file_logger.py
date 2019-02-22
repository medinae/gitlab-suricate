from .abstract_logger import AbstractLogger
import datetime

class FileLogger(AbstractLogger):
	def supports(self, type: str) -> bool:
		return type == "file"

	def log(self, level: str, message: str) -> None:
		current_date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

		with open('logs.txt', 'a+') as file:
			file.write("%s | %s | %s \n" % (level, current_date, message))
