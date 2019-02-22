from typing import List

class MessageFormatter:
	def format(self, mrs: List) -> str:
		mr_count = len(mrs)
		if 0 == mr_count:
			message = "No pending MRs to review..."
		else:
			message = "There is %s non wip MRs without any votes/actions : \n" %(mrCount)
			for mr in mrs:
				message += "%s => %s \n" %(mr.label, mr.web_url)

		return message