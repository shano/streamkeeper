from abc import abstractmethod
from pushover import init, Client


class AbstractNotificationService:
    @abstractmethod
    def __init__(self, CLIENT_ID, TOKEN):
        self.client_id = CLIENT_ID
        self.token = TOKEN

    @abstractmethod
    def notify(self, video_id, video_name):
        pass


class PushoverNotificationService(AbstractNotificationService):
    def __init__(self, CLIENT_ID, TOKEN):
        super().__init__(CLIENT_ID, TOKEN)
        init(self.token)

    def notify(self, message, title=""):
        Client(self.client_id).send_message(message, title=title)
