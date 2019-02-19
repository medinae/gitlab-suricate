import requests, json
from .MergeRequest import MergeRequest
from typing import Dict

class GitlabClient:
	def __init__(self, config):
		self.config = config

	def getNotReviewedMergeRequests(self, orderByUpdate: bool = False) -> Dict:
		mrs = self.getOpenedMergeRequests(orderByUpdate)

		pendingMrs = []
		for mr in mrs:
			if self.isMergeRequestNotReviewed(mr):
				title = mr['title']
				title = title[:40]
				title += "..."

				pendingMrs.append(MergeRequest(title, mr['web_url']))

		return pendingMrs

	def getOpenedMergeRequests(self, orderByUpdate: bool = False) -> Dict:
		urlPattern = self.config['GITLAB_API_BASE_URL']
		urlPattern += "projects/%s/merge_requests?state=opened"

		if (True == orderByUpdate):
			urlPattern += "&order_by=updated_at"

		mrEndpointUrl = urlPattern %(self.config['GITLAB_PROJECT_ID'])

		response = requests.get(mrEndpointUrl, headers = {
			'PRIVATE-TOKEN' : self.config['GITLAB_API_TOKEN']
		})

		response.raise_for_status()

		return json.loads(response.text)

	def isMergeRequestNotReviewed(self, mr: Dict[str, str]) -> bool:
		isNotReviewed = False == mr['work_in_progress'] and 0 == mr['user_notes_count']

		try:
			minReviewUpvotesThreshold = int(self.config['MR_MIN_REVIEWED_UPVOTES_CONDITION'])
		except:
			minReviewUpvotesThreshold = 1

		return isNotReviewed and (mr['upvotes'] < minReviewUpvotesThreshold)
