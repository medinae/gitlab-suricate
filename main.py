from config_management import ConfigProvider
import gitlab
from notifier import *
from smealog import *
from typing import Dict

def build_chain_notifier(config: Dict) -> ChainNotifier:
	notifiers = []
	notifiers.append(SlackNotifier(config))

	return ChainNotifier(notifiers)

def resolve_logger(typ: str) -> AbstractLogger:
	loggers = []
	loggers.append(FileLogger())

	resolver = LoggerResolver(loggers)

	return resolver.resolve(typ)

def main() -> None:
	print("===== Gitlab Suricate =====")

	conf = ConfigProvider()
	config = conf.getAppConfig()

	logger = resolve_logger("file") # use conf here
	gitlab_client = gitlab.GitlabClient(config, logger)

	print("Fetching MRs from Gitlab API...")
	pending_mrs = gitlab_client.get_not_reviewed_merge_requests(order_by_update=True)

	formatter = gitlab.MessageFormatter()
	msg = formatter.format(pending_mrs)

	chainNotifier = build_chain_notifier(config)
	print("Notify the slack channel...")
	chainNotifier.notify(msg)

main()
