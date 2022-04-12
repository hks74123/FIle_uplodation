class ChunkedUploadError(Exception):
    def __init__(self, status, **data):
        self.status_code = status
        self.data = data
