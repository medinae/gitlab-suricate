class AbstractLogger:
	def supports(self, type: str) -> bool:
		raise NotImplementedError("Should be implemented")

	def log(self, level: str, message: str) -> None:
		raise NotImplementedError("Should be implemented")
