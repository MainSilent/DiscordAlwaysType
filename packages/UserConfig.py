
from dataclasses import dataclass
from getpass import getpass

@dataclass
class UserConfig:
    """
    Class for keeping track of a user's configurations.
    """
    token: str = None
    channel_id: str = None

    def request_token(self) -> str:
        token: str = ''
        while token == '':
            token = getpass("Enter your token: ")

        self.token = token
        return token

    def request_channel_id(self) -> str:
        channel_id: str = ''
        while channel_id == '':
            channel_id = input("Enter desired channel id: ")
        self.channel_id = channel_id
        return channel_id
    