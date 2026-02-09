class Configuration:
    def __init__(
            self,
            host: str,
            headers: dict = None,
            disable_logs: bool = True
    ):
        self.host = host
        self.headers = headers
        self.disable_logs = disable_logs
