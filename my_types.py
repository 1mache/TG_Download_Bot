class Download():
    def __init__(self, chat_id, stream, info_message = None) -> None:
        self.chat_id = chat_id
        self.stream = stream
        self.info_message = info_message

        