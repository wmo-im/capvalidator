from cap_validator.integrity import CheckIntegrity


def test_valid_alert_integrity(valid_alert):
    assert CheckIntegrity(valid_alert)


def test_no_identifier_integrity(no_identifier):
    assert not CheckIntegrity(no_identifier)


def test_incorrect_digest_integrity(incorrect_digest):
    assert not CheckIntegrity(incorrect_digest)


def test_incorrect_signature_integrity(incorrect_signature):
    assert CheckIntegrity(incorrect_signature)
