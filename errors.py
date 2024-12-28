class StarshipError(Exception):
    def __init__(self, message, line):
        self.line = line
        self.message = message
        super().__init__(f"🚨 MISSION FAILURE at coordinate {line}: {message}")
