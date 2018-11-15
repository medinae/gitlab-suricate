import requests

class SlackNotifier:
	def __init__(self, config):
		self.config = config

	def notify(self, message):
		response = requests.post(
			self.config['SLACK_WEBHOOK_URL'],
			json = {
				'text': message,
				'channel': self.config['SLACK_CHANNEL_NAME']
			}
		)

		if (200 != response.status_code):
			raise Exception('Error when trying to contact Slack API')
