class User:
    """Represents a chat participant with a username and display name."""

    def __init__(self, username, display_name):
        self.username = username
        self.display_name = display_name

    def tag(self):
        return f"@{self.username}"


class Message:
    """Base message class defining the shared structure for all message types."""

    def __init__(self, author):
        self.author = author
        self.id = -1
        self._created_seq = None

    def display_body(self):
        raise NotImplementedError("Subclasses must implement display_body()")

    def display(self):
        header = f"{self.author.display_name} {self.author.tag()}"
        return f"{header}\n{self.display_body()}"


class TextMessage(Message):
    """Represents a plain text message."""

    def __init__(self, author, text=""):
        super().__init__(author)
        self.text = text

    def display_body(self):
        return self.text


class ImageMessage(Message):
    """Represents an image message."""

    def __init__(self, author, url=""):
        super().__init__(author)
        self.url = url

    def display_body(self):
        return f"<image: {self.url}>"

    def display(self):
        return f"{super().display()}\n{'-' * 40}"


class ReactionMessage(Message):
    """Represents a reaction (emoji) to another message."""

    def __init__(self, author, emoji='👍', target_message_id=-1):
        super().__init__(author)
        self.emoji = emoji
        self.target_message_id = target_message_id

    def display_body(self):
        return f"reacted {self.emoji} to message #{self.target_message_id}"


class ChatRoom:
    """A container managing users and messages in a chat session."""

    def __init__(self, name):
        self.name = name
        self._users = {}
        self._messages = []
        self._next_id = 1
        self._seq_counter = 0

    def join(self, user):
        self._users[user.username] = user

    def leave(self, username):
        if username in self._users:
            del self._users[username]

    def users(self):
        return list(self._users.values())

    def post(self, message):
        if isinstance(message, ReactionMessage):
            if self.find_message(message.target_message_id) is None:
                raise ValueError(f'No message with id={message.target_message_id} to react to.')

        message.id = self._next_id
        self._next_id += 1
        self._seq_counter += 1
        message._created_seq = self._seq_counter
        self._messages.append(message)
        return message.id

    def history(self, limit=None):
        if limit is None:
            return list(self._messages)
        return list(self._messages[-limit:])

    def _indent(self, text, prefix):
        lines = text.splitlines() or ['']
        return '\n'.join(prefix + line for line in lines)

    def render_history(self, limit=None):
        parts = [f"# Room: {self.name}"]
        participants = ', '.join(u.display_name for u in self.users())
        parts.append(f"Participants: {participants}\n")
        for m in self.history(limit):
            parts.append(f"#{m.id}")
            parts.append(self._indent(m.display(), ' '))
            parts.append('')
        return '\n'.join(parts).rstrip()

    def find_message(self, msg_id):
        for m in self._messages:
            if m.id == msg_id:
                return m
        return None

