from cap_validator.integrity import CheckIntegrity


def test_valid_alert_integrity(valid_alert):
    hashes_match = CheckIntegrity(valid_alert).validate()
    assert hashes_match


def test_no_identifier_integrity(no_identifier):
    hashes_match = CheckIntegrity(no_identifier).validate()
    assert not hashes_match


def test_incorrect_digest_integrity(incorrect_digest):
    hashes_match = CheckIntegrity(incorrect_digest).validate()
    assert not hashes_match


def test_incorrect_signature_integrity(incorrect_signature):
    hashes_match = CheckIntegrity(incorrect_signature).validate()
    assert hashes_match
