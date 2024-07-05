from cap_validator.integrity import VerifySignature


def test_valid_alert_signature(valid_alert):
    assert VerifySignature(valid_alert)


def test_no_identifier_signature(no_identifier):
    assert VerifySignature(no_identifier)


def test_incorrect_digest_signature(incorrect_digest):
    assert VerifySignature(incorrect_digest)


def test_incorrect_signature(incorrect_signature):
    assert not VerifySignature(incorrect_signature)
