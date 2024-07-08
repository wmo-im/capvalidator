from cap_validator.signature import CheckSignature


def test_valid_alert_signature(valid_alert):
    valid_signature = CheckSignature(valid_alert).validate()
    assert valid_signature


def test_no_identifier_signature(no_identifier):
    valid_signature = CheckSignature(no_identifier).validate()
    assert valid_signature


def test_incorrect_digest_signature(incorrect_digest):
    valid_signature = CheckSignature(incorrect_digest).validate()
    assert valid_signature


def test_incorrect_signature(incorrect_signature):
    valid_signature = CheckSignature(incorrect_signature).validate()
    assert not valid_signature
