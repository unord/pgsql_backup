import datetime


class Logger:
    def __init__(self, log_file="backup_log.txt"):
        self.log_file = log_file

    def log(self, message: str, tag="INFO") -> None:
        # Logs a message with a given tag and the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} [{tag}]: {message}\n"
        with open(self.log_file, "a") as f:
            f.write(log_message)

    @staticmethod
    def get_timestamp() -> str:
        # Generates a formatted timestamp
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
