class MergeRequest:
    def __init__(self, label: str, web_url: str):
        if not isinstance(label, str) or not isinstance(web_url, str):
            raise Exception('Label and web url provided to MergeRequest class should be strings')

        self.label = label
        self.web_url = web_url
