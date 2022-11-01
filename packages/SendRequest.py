import logging
import requests

from time import sleep
from dataclasses import dataclass
from .UserConfig import UserConfig

@dataclass
class SendRequest:
    user: UserConfig = None
    url: str = None
    headers: dict = None
    count: int = 0
    SLEEP_TIME: int = 3

    def __post_init__(self) -> None:
        self.url = f"https://discord.com/api/v9/channels/{self.user.channel_id}/typing"
        self.headers = {
            'authorization': self.user.token
        }

    def run(self) -> None:
        logging.info(f"You can stop the program by pressing Ctrl+C")
        try:
            while True:
                response = requests.post(self.url, headers=self.headers)
                if response.status_code != 204:
                    logging.warning(f"Failed {response.text}")
                else:
                    self.count += 1
                    logging.verbose(f"Sent - {self.count}")
                    
                sleep(self.SLEEP_TIME)
        except KeyboardInterrupt:
            logging.info("Exiting...")