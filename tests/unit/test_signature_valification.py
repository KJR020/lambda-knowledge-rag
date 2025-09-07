from index import hash_event, verify_signature


def test_invalid_signature():
    event = {"headers": {"x-signature": "invalid_signature"}}
    secret = "dummy_secret"
    expected_signature = hash_event(event, secret)
    is_valid = verify_signature(event["headers"]["x-signature"], expected_signature)
    assert not is_valid


class TestLambdaHandler:
    pass
