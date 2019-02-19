from config_management import ConfigProvider
from gitlab import GitlabClient
from notifier import *
from typing import Dict

def buildChainNotifier(config: Dict[int, str]) -> ChainNotifier:
	notifiers = []
	slack_notifier = SlackNotifier(config)
	notifiers.append(slack_notifier)

	return ChainNotifier(notifiers)

def main() -> None:
	print("===== Gitlab Suricate =====")

	conf = ConfigProvider()
	config = conf.getAppConfig()

	gitlab = GitlabClient(config)

	print("Fetching MRs from Gitlab API...")
	pendingMrs = gitlab.getNotReviewedMergeRequests(orderByUpdate=True)

	chainNotifier = buildChainNotifier(config)

	pendingMrsCount = len(pendingMrs)
	if 0 == pendingMrsCount:
		message = "No pending MRs to review. I don't know if i have to congrats you or blame you guys..."
	else:
		message = "There is %s non wip MRs without any votes/actions : \n" %(pendingMrsCount)
		for mr in pendingMrs:
			message += "%s => %s \n" %(mr.label, mr.webUrl)

	print("Notify the slack channel...")
	chainNotifier.notify(message)

main()
