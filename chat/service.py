"""Chat Service"""

from nameko.rpc import RpcProxy, rpc
from nameko.dependency_providers import Config

import json
import time
import hashlib
import html


class ChatService:
    name = "chat"

    player_rpc = RpcProxy("player")
    config = Config()

    @rpc
    def validate_message(self, sender, content):
        content_empty = len(content) == 0

        if content_empty:
            return None

        cleaned_content = html.escape(content)
        return cleaned_content

    @rpc
    def create_room(self, room_name: str, creator: str):
        creator_exists = self.player_rpc.get_player_by_username(creator) is not None

        secret = self.config.get("SECRET", "secret")
        hash_string = f"{secret};{str(time.time())};{creator};{room_name}"
        signature = hashlib.sha256(hash_string.encode()).hexdigest()

        if not creator_exists:
            return None

        return json.dumps({
            "room": {
                "code": signature,
                "name": room_name
            }
        })
