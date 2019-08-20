import pytest

from nameko.testing.services import worker_factory

from chat.service import ChatService

import time
import json

def test_chat_validation():
    service = worker_factory(ChatService)

    service.player_rpc.get_player_by_username.side_effect = lambda username: username if username == 'test_user' else None

    assert service.validate_message("test_user", "Test Message") == "Test Message"
    assert service.validate_message("non_user", "Test Message") is None
    assert service.validate_message("test_user", "") is None


def test_room_creation():
    service = worker_factory(ChatService)

    valid_users = ['userA', 'userB']
    service.player_rpc.get_player_by_username.side_effect = \
        lambda username: username if username in valid_users else None

    assert service.create_room("Test Room", "userA") != service.create_room("Test Room", "userB")
    assert service.create_room("Test Room", "userA") != service.create_room("Test Room B", "userA")

    early_code = service.create_room("Test Room", "userA")
    time.sleep(0.1)
    late_code = service.create_room("Test Room", "userA")

    assert early_code != late_code

