class MergeRequest:
    def __init__(self, label: str, webUrl: str):
        if not isinstance(label, str) or not isinstance(webUrl, str):
            raise Exception('Label and web url provided to MergeRequest class should be strings')

        self.label = label
        self.webUrl = webUrl
