class ChainNotifier:
	def __int__(self, notifiers):
		self.notifiers = notifiers

	def notify(self, message):
		for notifier in notifiers:
			try:
				notifier.notify(message)
			except AttributeError:
				raise Exception('All given notifiers should implement a notify method')
