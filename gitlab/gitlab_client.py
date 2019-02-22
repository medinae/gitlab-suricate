import requests, json
from .merge_request import MergeRequest
from typing import Dict

class GitlabClient:
	def __init__(self, config, logger):
		self.config = config
		self.logger = logger

	def get_not_reviewed_merge_requests(self, order_by_update: bool = False) -> Dict:
		mrs = self.__get_opened_merge_requests(order_by_update)

		pending_mrs = []
		for mr in mrs:
			if self.__is_merge_request_not_reviewed(mr):
				title = mr['title']
				title = title[:40]
				title += "..."

				pending_mrs.append(MergeRequest(title, mr['web_url']))

		return pending_mrs

	def __get_opened_merge_requests(self, order_by_update: bool = False) -> Dict:
		url_pattern = self.config['GITLAB_API_BASE_URL']
		url_pattern += "projects/%s/merge_requests?state=opened"

		if (True == order_by_update):
			url_pattern += "&order_by=updated_at"

		mr_endpoint_url = url_pattern %(self.config['GITLAB_PROJECT_ID'])

		response = requests.get(mr_endpoint_url, headers = {
			'PRIVATE-TOKEN' : self.config['GITLAB_API_TOKEN']
		})

		jsonContent = response.text
		self.logger.log('DEBUG', "Gitlab GET Merge requests respone : %s" % (jsonContent))

		response.raise_for_status()

		return json.loads(jsonContent)

	def __is_merge_request_not_reviewed(self, mr: Dict[str, str]) -> bool:
		is_not_reviewed = False == mr['work_in_progress'] and 0 == mr['user_notes_count']

		try:
			min_upvotes_threshold = int(self.config['MR_MIN_REVIEWED_UPVOTES_CONDITION'])
		except:
			min_upvotes_threshold = 1

		return is_not_reviewed and (mr['upvotes'] < min_upvotes_threshold)
