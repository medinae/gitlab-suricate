from config_management.config_provider import ConfigProvider
from gitlab.gitlab_client import GitlabClient
from notifier.chain_notifier import ChainNotifier
from notifier.slack_notifier import SlackNotifier

def main():
	print("===== Gitlab Suricate =====")

	config_provider = ConfigProvider()
	config = config_provider.get_app_config()

	gitlab_client = GitlabClient(config)

	print("Fetching MRs from Gitlab API...")
	pending_merge_requests = gitlab_client.get_not_reviewed_merge_requests(order_by_update=True)

	#notifiers = []
	slack_notifier = SlackNotifier(config)
	#notifiers.append(slack_notifier)

	if 0 == len(pending_merge_requests):
		message = "No pending MRs to review. I don't know if i have to congrats you or blame you guys..."
	else:
		message = "There is %s non wip MRs without any votes/actions : \n" %(len(pending_merge_requests))
		for mr in pending_merge_requests:
			message += "%s => %s \n" %(mr['label'], mr['url'])

	print("Notify the slack channel...")
	slack_notifier.notify(message)
	#chain_notifier = ChainNotifier(notifiers)

main()
