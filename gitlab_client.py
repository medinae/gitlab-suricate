import requests, json

class GitlabClient:
	def __init__(self, config):
		self.config = config

	def get_not_reviewed_merge_requests(self, order_by_update = False):
		merge_requests = self.get_opened_merge_requests(order_by_update)

		pending_mrs = [];
		for mr in merge_requests:
			if 0 == mr['upvotes'] and 0 == mr['downvotes'] and 0 == mr['user_notes_count'] and False == mr['work_in_progress'] :
				title = mr['title']
				title = title[:40]
				title += "..."


				pending_mrs.append({'url': mr['web_url'], 'label': title})

		return pending_mrs

	def get_opened_merge_requests(self, order_by_update = False):
		url_pattern = self.config['GITLAB_API_BASE_URL']
		url_pattern += "projects/%s/merge_requests?state=opened"

		if (True == order_by_update):
			url_pattern += "&order_by=updated_at"

		get_mr_url = url_pattern %(self.config['GITLAB_PROJECT_ID'])

		response = requests.get(get_mr_url, headers = {
			'PRIVATE-TOKEN' : self.config['GITLAB_API_TOKEN']
		})

		if (200 != response.status_code):
			raise Exception('Error when trying to contact Gitlab API')

		return json.loads(response.text)