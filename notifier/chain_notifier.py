from typing import Dict

class ChainNotifier:
	def __init__(self, notifiers: Dict):
		self.notifiers = notifiers

	def notify(self, message: str) -> None:
		for notifier in self.notifiers:
			try:
				notifier.notify(message)
			except AttributeError:
				raise Exception('All given notifiers should implement a notify method')
