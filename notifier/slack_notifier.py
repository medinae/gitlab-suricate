import requests
from typing import Dict

class SlackNotifier:
	def __init__(self, config: Dict):
		self.config = config

	def notify(self, message: str):
		response = requests.post(
			self.config['SLACK_WEBHOOK_URL'],
			json = {
				'text': message,
				'channel': self.config['SLACK_CHANNEL_NAME']
			}
		)

		response.raise_for_status()
