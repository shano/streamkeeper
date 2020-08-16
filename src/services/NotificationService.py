from abc import abstractmethod

from pushover import Client, init


class AbstractNotificationService:
    @abstractmethod
    def __init__(self, CLIENT_ID, TOKEN):
        self.client_id = CLIENT_ID
        self.token = TOKEN

    @abstractmethod
    def notify(self, message, title=""):
        pass


class PushoverNotificationService(AbstractNotificationService):
    def __init__(self, CLIENT_ID, TOKEN):
        super().__init__(CLIENT_ID, TOKEN)
        init(self.token)

    def notify(self, message, title=""):
        print(f"Notification {message} - {title}")
        Client(self.client_id).send_message(message, title=title)


class PrintNotificationService(AbstractNotificationService):
    def __init__(self):
        pass

    def notify(self, message, title=""):
        print(f"Notification {message} - {title}")
