import pytest

from nameko.testing.services import worker_factory

from chat.service import ChatService

import time
import json


def test_chat_validation():
    service = worker_factory(ChatService)

    assert service.validate_message("test_user", "Test Message") == "Test Message"
    assert service.validate_message("test_user", "") is None


def test_room_creation():
    service = worker_factory(ChatService)

    valid_users = ['userA', 'userB']
    service.player_rpc.get_player_by_username.side_effect = \
        lambda username: username if username in valid_users else None

    """
    Test that different rooms generate different codes for:
    - Different users
    - Different room names
    - Different creation time 
    """

    # different users
    room_user_a = json.loads(service.create_room("room", "userA"))["room"]
    room_user_b = json.loads(service.create_room("room", "userB"))["room"]

    assert room_user_a["code"] != room_user_b["code"]

    # different room names
    print(service.create_room("room A", "user"))
    room_a = json.loads(service.create_room("room A", "userA"))["room"]
    room_b = json.loads(service.create_room("room B", "userB"))["room"]

    assert room_a["code"] != room_b["code"]

    # different room creation time
    room_early = json.loads(service.create_room("room", "userA"))["room"]
    time.sleep(0.1)
    room_late = json.loads(service.create_room("room", "userB"))["room"]

    assert room_early["code"] != room_late["code"]

    """
    Don't create a room if creator username is not valid
    """

    assert service.create_room("room", "non_user") is None
