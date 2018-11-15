import requests, json

class GitlabClient:
	def __init__(self, config):
		self.config = config

	def get_not_reviewed_merge_requests(self, order_by_update = False):
		merge_requests = self.get_opened_merge_requests(order_by_update)

		pending_mrs = []
		for mr in merge_requests:
			if self.is_merge_request_not_reviewed(mr):
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

		response.raise_for_status()

		return json.loads(response.text)

	def is_merge_request_not_reviewed(self, mr):
		is_not_reviewed = False == mr['work_in_progress'] and 0 == mr['user_notes_count']

		try:
			min_reviewed_upvotes_condition = int(self.config['MR_MIN_REVIEWED_UPVOTES_CONDITION'])
		except:
			min_reviewed_upvotes_condition = 1

		return is_not_reviewed and (mr['upvotes'] < min_reviewed_upvotes_condition)
