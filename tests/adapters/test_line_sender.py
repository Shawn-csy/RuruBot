"""
tests/adapters/test_line_sender.py

測試 LINE 發送邏輯（分批規則），不需要真實 LINE client。
"""
from contextlib import contextmanager
from unittest.mock import MagicMock, patch, call
from services.adapters.line_sender import send_messages, LINE_REPLY_LIMIT


def make_messages(n: int) -> list:
    return [MagicMock() for _ in range(n)]


@contextmanager
def mock_sender():
    """
    mock api client 和 Request 物件，避開 pydantic validation。
    yield (api, ReplyReq, PushReq)
    """
    api = MagicMock()
    with patch('services.adapters.line_sender._get_line_bot_api', return_value=api), \
         patch('services.adapters.line_sender.ReplyMessageRequest') as MockReply, \
         patch('services.adapters.line_sender.PushMessageRequest') as MockPush:
        yield api, MockReply, MockPush


class TestSendMessages:

    def test_empty_messages_does_nothing(self):
        with mock_sender() as (api, _, __):
            send_messages("token", "user1", [])
        api.reply_message.assert_not_called()
        api.push_message.assert_not_called()

    def test_single_message_uses_reply_only(self):
        msgs = make_messages(1)
        with mock_sender() as (api, _, __):
            send_messages("token", "user1", msgs)
        api.reply_message.assert_called_once()
        api.push_message.assert_not_called()

    def test_exactly_limit_uses_reply_only(self):
        msgs = make_messages(LINE_REPLY_LIMIT)
        with mock_sender() as (api, _, __):
            send_messages("token", "user1", msgs)
        api.reply_message.assert_called_once()
        api.push_message.assert_not_called()

    def test_over_limit_uses_reply_then_push(self):
        msgs = make_messages(LINE_REPLY_LIMIT + 1)
        with mock_sender() as (api, _, __):
            send_messages("token", "user1", msgs)
        api.reply_message.assert_called_once()
        api.push_message.assert_called_once()

    def test_reply_gets_first_five(self):
        msgs = make_messages(7)
        with mock_sender() as (api, MockReply, _):
            send_messages("token", "user1", msgs)
        MockReply.assert_called_once_with(reply_token="token", messages=msgs[:LINE_REPLY_LIMIT])

    def test_push_gets_remaining_in_batches(self):
        """11 則 → reply 前 5，push 次 5，push 最後 1"""
        msgs = make_messages(11)
        with mock_sender() as (api, _, MockPush):
            send_messages("token", "user1", msgs)
        assert api.push_message.call_count == 2
        MockPush.assert_any_call(to="user1", messages=msgs[5:10])
        MockPush.assert_any_call(to="user1", messages=msgs[10:])

    def test_reply_token_passed_correctly(self):
        msgs = make_messages(1)
        with mock_sender() as (api, MockReply, _):
            send_messages("my-reply-token", "user1", msgs)
        MockReply.assert_called_once_with(reply_token="my-reply-token", messages=msgs)

    def test_push_user_id_passed_correctly(self):
        msgs = make_messages(6)
        with mock_sender() as (api, _, MockPush):
            send_messages("token", "uid-123", msgs)
        MockPush.assert_called_once_with(to="uid-123", messages=msgs[5:])

    def test_api_receives_request_objects(self):
        """api.reply_message / push_message 收到的是 Request 物件，不是 raw messages list"""
        msgs = make_messages(6)
        with mock_sender() as (api, MockReply, MockPush):
            send_messages("token", "user1", msgs)
        api.reply_message.assert_called_once_with(MockReply.return_value)
        api.push_message.assert_called_once_with(MockPush.return_value)
